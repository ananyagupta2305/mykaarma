from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List
from .catalog import find_by_id, filter_catalog, CATALOG
from .intent_parser import parse_intent
from .llm_adapter import ask_llm
from .safety import check_adversarial

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str | None = None
    message: str

class CompareRequest(BaseModel):
    ids: List[str]

@router.get("/phones")
def list_phones(max_price: int | None = None, brand: str | None = None, tag: str | None = None):
    tags = [tag] if tag else None
    results = filter_catalog(max_price=max_price, brand=brand, tags=tags)
    return {"count": len(results), "items": results}

@router.get("/phones/{phone_id}")
def phone_detail(phone_id: str):
    p = find_by_id(phone_id)
    if not p:
        raise HTTPException(status_code=404, detail="Phone not found")
    return p

@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    # 1️⃣ Safety check
    adv, msg = check_adversarial(req.message)
    if adv:
        return {"text": msg}

    # 2️⃣ Parse intent
    intent = parse_intent(req.message)
    max_price = intent.get("budget_in_inr")
    brand = intent.get("brands")[0] if intent.get("brands") else None
    tags = intent.get("features")

    # 3️⃣ Filter catalog for matches
    candidates = filter_catalog(max_price=max_price, brand=brand, tags=tags)

    # 4️⃣ If no direct match, fallback gracefully — but stay relevant
    if not candidates:
        user_prompt = f"""
        The user asked: "{req.message}".
        Suggest 2–3 current phones that realistically fit this request (based on Indian market).
        The answer must directly address the user's question (e.g., camera, gaming, battery).
        Be confident and concise — avoid apologies or vague language.
        """
        system_prompt = (
            "You are a professional phone recommender AI specializing in Indian market phones. "
            "You always provide clear, short recommendations that strongly match the user's intent."
        )
        reply_text = ask_llm(user_prompt, system_prompt)
        return {"text": reply_text, "cards": []}

    # 5️⃣ Build rich phone context for the LLM
    phone_context = "\n".join([
        f"- {p['brand']} {p['model']} — ₹{p.get('price_in_inr', 'N/A')}, Tags: {', '.join(p.get('tags', []))}, Why: {p.get('why_recommended', '')}"
        for p in candidates[:5]
    ])

    # 6️⃣ Strong system prompt: tie features to user query
    system_prompt = (
        "You are a helpful and concise AI phone recommender for Indian users.\n"
        "Use the provided phone list only. Choose 2–3 top matches that BEST fit the user's request "
        "(e.g., if user mentions 'camera', prefer phones with 'camera' or 'camera-ois' tags). "
        "Never mention unavailable data or apologize. Respond in 1–2 crisp sentences."
    )

    # 7️⃣ Focused user prompt for Groq model
    user_prompt = f"""
    User query: "{req.message}"
    Available phones (with tags & rationales):
    {phone_context}

    Generate a short, confident, helpful response recommending the best phones
    that truly match the user's request.
    """

    # 8️⃣ Ask Groq model
    reply_text = ask_llm(user_prompt, system_prompt)

    # 9️⃣ Prepare cards for UI
    cards = [
        {
            "id": p["id"],
            "name": f"{p['brand']} {p['model']}",
            "price": f"₹{p.get('price_in_inr', 'N/A'):,}" if isinstance(p.get("price_in_inr"), int) else p.get("price_in_inr"),
            "why_recommended": p.get("why_recommended", "")
        }
        for p in candidates[:5]
    ]

    return {"text": reply_text, "cards": cards}


@router.post("/compare")
def compare(req: CompareRequest):
    items = [find_by_id(i) for i in req.ids]
    items = [it for it in items if it]
    if not items:
        raise HTTPException(status_code=404, detail="No phones found for the provided ids")
    # create a small comparison table
    fields = ["price_in_inr","camera","battery","ram_gb","storage_gb","tags"]
    table = {f: [it.get(f, 'n/a') for it in items] for f in fields}
    diffs = {f: len(set(str(x) for x in table[f])) > 1 for f in table}
    return {"items": items, "table": table, "diffs": diffs}
