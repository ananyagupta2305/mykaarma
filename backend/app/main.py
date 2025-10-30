# # from fastapi import FastAPI, Request
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import JSONResponse
# # from pydantic import BaseModel
# # from requests import request

# # app = FastAPI()

# # # ✅ Allow requests from frontend (localhost:5173)
# # origins = [
# #     "http://localhost:5173",
# #     "http://127.0.0.1:5173"
# # ]

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=origins,
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # ---------- Models ----------
# # class ChatRequest(BaseModel):
# #     user_id: str | None = None
# #     message: str

# # class CompareRequest(BaseModel):
# #     ids: list[str]

# # # ---------- Routes ----------
# # @app.post("/chat")
# # def chat_endpoint(req: ChatRequest):
# #     return {
# #         "text": f"Got your query: '{req.message}' — backend connected successfully!",
# #         "cards": [
# #             {"id": "p1", "name": "Redmi Note 13 Pro", "price": "₹24,999"},
# #             {"id": "p2", "name": "iQOO Z9 5G", "price": "₹18,999"},
# #         ]
# #     }

# # def jsonify(*args, **kwargs):
# #     raise NotImplementedError

# # @app.post("/compare")
# # async def compare(request: Request):
# #     data = await request.json()
# #     phones = data.get("phones", [])

# #     comparison_data = {
# #         "title": "Comparison Table",
# #         "phones": phones,
# #         "specs": {
# #             "Camera": ["108MP", "64MP"],
# #             "Battery": ["5000mAh", "4500mAh"],
# #             "Display": ["AMOLED", "LCD"],
# #         },
# #     }

# #     return JSONResponse(content={"comparison": comparison_data})


# # @app.get("/")
# # def root():
# #     return {"message": "Backend is live!"}













# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from app.catalog import search_phones, compare_phones

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # ⚠️ change in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/chat")
# async def chat(request: Request):
#     data = await request.json()
#     query = data.get("message", "")
#     results = search_phones(query, max_results=6)

#     if not results:
#         return {"text": f"Sorry, no phones matched your query: '{query}'.", "cards": []}

#     text = f"Got your query: '{query}' — here are some matches!" 
#     cards = [
#         {
#             "id": p["id"],
#             "name": p["name"],
#             "price": f"₹{p['price']:,}" if isinstance(p.get("price"), int) else p.get("price"),
#             "why_recommended": p.get("why_recommended", "")
#         } for p in results
#     ]

#     return {"text": text, "cards": cards}


# @app.post("/compare")
# async def compare(request: Request):
#     data = await request.json()
#     ids = data.get("phones") or data.get("ids") or []
#     comparison = compare_phones(ids)

#     # ✅ Flatten response for frontend
#     if comparison:
#         return comparison
#     else:
#         return {"error": "Phones not found for comparison"}









from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.catalog import search_phones, compare_phones
from app.llm_adapter import ask_llm  # ✅ Import Groq LLM helper

app = FastAPI(title="Phone Recommender Chatbot")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Update with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- /chat endpoint ---
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    query = data.get("message", "").strip()

    if not query:
        return {"text": "Please enter a query like 'Best phone under ₹20,000'."}

    # 🔍 Search for phones from catalog
    results = search_phones(query, max_results=6)

    if not results:
        return {"text": f"Sorry, no phones matched your query: '{query}'.", "cards": []}

    # 🧠 Ask LLM to generate natural response
    context = "\n".join(
        [f"{p['name']} — ₹{p['price']:,}, {p.get('why_recommended', '')}" for p in results]
    )
    system_prompt = (
        "You are a helpful and concise phone recommender assistant. "
        "Summarize recommendations conversationally using the following catalog info."
    )
    user_prompt = f"User query: {query}\nAvailable phones:\n{context}\n\nGenerate a 1-2 sentence helpful response."

    llm_reply = ask_llm(user_prompt, system_prompt=system_prompt)

    # 🧩 Build cards for frontend
    cards = [
        {
            "id": p["id"],
            "name": p["name"],
            "price": f"₹{p['price']:,}" if isinstance(p.get('price'), int) else p.get('price'),
            "why_recommended": p.get("why_recommended", "")
        }
        for p in results
    ]

    return {
        "text": llm_reply,
        "cards": cards
    }

# --- /compare endpoint ---
@app.post("/compare")
async def compare(request: Request):
    data = await request.json()
    ids = data.get("phones") or data.get("ids") or []
    comparison = compare_phones(ids)

    if comparison:
        return comparison
    else:
        return {"error": "Phones not found for comparison"}
