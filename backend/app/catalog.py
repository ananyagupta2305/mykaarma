# import json
# from pathlib import Path
# from typing import List, Dict, Any


# DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "mock_catalog_v1.json"


# def load_catalog() -> List[Dict[str, Any]]:
#     with open(DATA_PATH, "r", encoding="utf-8") as f:
#         return json.load(f)


# CATALOG = load_catalog()


# def find_by_id(phone_id: str) -> Dict[str, Any] | None:
#     for p in CATALOG:
#         if p["id"] == phone_id:
#             return p
#     return None


# def filter_catalog(max_price: int = None, brand: str = None, tags: List[str] = None) -> List[Dict[str, Any]]:
#     results = CATALOG
#     if max_price is not None:
#         results = [p for p in results if p.get("price_in_inr") is not None and p["price_in_inr"] <= max_price]
#     if brand:
#         results = [p for p in results if p.get("brand","").lower() == brand.lower()]
#     if tags:
#         tags_lower = [t.lower() for t in tags]
#         results = [p for p in results if any(t.lower() in tags_lower for t in p.get("tags", []))]
#     return results




# import json
# import os
# from pathlib import Path
# import re
# from typing import List, Dict, Any



# THIS_DIR = os.path.dirname(__file__)
# CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "mock_catalog_v1.json"

# # Tag -> short phrase mapping used to build rationale
# TAG_PHRASES = {
#     "camera": "strong camera hardware for photos and videos",
#     "camera-ois": "OIS for stabilized shots",
#     "battery": "excellent battery life",
#     "charging": "fast charging support",
#     "display": "vibrant high-refresh display",
#     "performance": "solid performance for daily tasks and gaming",
#     "premium": "premium build and materials",
#     "budget": "great value for money",
#     "selfie": "good front camera for selfies",
#     "design": "attractive design",
#     "gaming": "tuned for gaming with good thermals",
#     "value": "excellent price-to-performance ratio",
#     "ai": "AI-driven camera/software features",
#     "onehand": "compact and easy one-hand use",
#     "storage": "generous storage option",
#     "ram": "ample RAM for multitasking",
#     "oled": "OLED display for deep blacks",
#     "amoled": "AMOLED screen for vivid colors",
#     "midrange": "solid mid-range contender",
#     "flagship": "flagship-level specs",
#     "durable": "robust build / IP rating",
# }

# DEFAULT_PHRASES = [
#     "a balanced set of features for everyday use",
#     "good overall value",
# ]

# def _phrase_for_tags(tags: List[str]) -> str:
#     """Create a short natural-language rationale from tags."""
#     phrases = []
#     # canonicalize tags: lowercase, replace spaces/hyphens
#     clean_tags = [t.lower().replace(" ", "-") for t in tags]
#     # pick highest-priority phrases: camera, battery, performance, display, charging, budget, premium
#     priority = ["camera", "camera-ois", "battery", "charging", "performance", "display",
#                 "amoled", "oled", "ai", "gaming", "budget", "premium", "value", "design", "selfie", "onehand"]
#     for p in priority:
#         if p in clean_tags and p in TAG_PHRASES:
#             phrases.append(TAG_PHRASES[p])
#     # add any other relevant tags not in priority
#     for t in clean_tags:
#         if t in TAG_PHRASES and TAG_PHRASES[t] not in phrases:
#             phrases.append(TAG_PHRASES[t])
#     if not phrases:
#         phrases = DEFAULT_PHRASES.copy()
#     # combine into 1-2 sentence phrase
#     if len(phrases) == 1:
#         return f"Recommended for {phrases[0]}."
#     # join first two with comma
#     return f"Recommended for {phrases[0]} and {phrases[1]}."

# def load_catalog() -> List[Dict[str, Any]]:
#     """Load catalog.json and enrich each phone with 'why_recommended'."""
#     with open(CATALOG_PATH, "r", encoding="utf-8") as f:
#         phones = json.load(f)

#     # Ensure consistency and enrich
#     for p in phones:
#         # ensure required fields exist
#         p.setdefault("tags", [])
#         p.setdefault("rating", p.get("rating", 4.0))

#         # normalize price field
#         if "price" not in p and "price_in_inr" in p:
#             p["price"] = p["price_in_inr"]

#         # normalize phone name
#         if "name" not in p:
#             brand = p.get("brand", "")
#             model = p.get("model", "")
#             p["name"] = f"{brand} {model}".strip() or f"Phone {p.get('id', '')}"

#         # generate why_recommended if not present
#         if not p.get("why_recommended"):
#             p["why_recommended"] = _phrase_for_tags(p.get("tags", []))

#         # normalize price as int if string
#         if isinstance(p.get("price"), str):
#             digits = re.findall(r"\d+", p["price"].replace(",", ""))
#             if digits:
#                 p["price"] = int(digits[0])

#         # ensure id exists
#         if "id" not in p:
#             p["id"] = f"p_{phones.index(p)+1}"

#     return phones


# # load once (module import)
# PHONES = load_catalog()


# def _extract_budget(query: str) -> int | None:
#     """Try to extract numeric budget from user query like '₹30k' or '30000' or '30,000'."""
#     if not query:
#         return None
#     q = query.lower().replace("₹", " ").replace(",", " ")
#     # look for patterns like 30k, 30000, 30 000
#     m = re.search(r"(\d{1,3}(?:[,\s]\d{3})+|\d+k|\d+)", q)
#     if not m:
#         return None
#     token = m.group(1)
#     if token.endswith("k"):
#         try:
#             return int(float(token[:-1]) * 1000)
#         except:
#             return None
#     # strip non-digits
#     digits = re.findall(r"\d+", token)
#     return int("".join(digits)) if digits else None


# def search_phones(query: str, max_results: int = 6) -> List[Dict[str, Any]]:
#     """Search phones by keywords and budget. Returns enriched phone objects."""
#     if not query:
#         # return top rated phones if empty query
#         results = sorted(PHONES, key=lambda x: (-x["rating"], x.get("price", 10**9)))
#         return results[:max_results]

#     q = query.lower()
#     budget = _extract_budget(q)

#     tokens = re.findall(r"\w+", q)
#     results = []
#     for p in PHONES:
#         hay = " ".join([
#             str(p.get("brand", "")).lower(),
#             str(p.get("name", "")).lower(),
#             " ".join([t.lower() for t in p.get("tags", [])])
#         ])
#         matched = False
#         # if budget mentioned and phone.price <= budget -> include
#         if budget and isinstance(p.get("price"), int) and p["price"] <= budget:
#             matched = True
#         # token match
#         for t in tokens:
#             if t and t in hay:
#                 matched = True
#                 break
#         if matched:
#             results.append(p)

#     # sort by rating desc, price asc
#     results = sorted(results, key=lambda x: (-x.get("rating", 0), x.get("price", 10**9)))
#     return results[:max_results]

# def compare_phones(ids):
#     selected = [p for p in PHONES if p["id"] in ids]

#     if not selected:
#         return None

#     specs = {}
#     for key in ["display", "processor", "camera", "battery", "ram", "storage", "os"]:
#         specs[key.capitalize()] = [p.get(key, "N/A") for p in selected]

#     rationales = [p.get("why_recommended", "") for p in selected]

#     return {
#         "title": "Comparison Table",
#         "names": [p["name"] for p in selected],
#         "specs": specs,
#         "rationales": rationales,
#     }
import json
import os
from pathlib import Path
import re
from typing import List, Dict, Any

THIS_DIR = os.path.dirname(__file__)
CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "mock_catalog_v1.json"

# Tag -> short phrase mapping used to build rationale
TAG_PHRASES = {
    "camera": "strong camera hardware for photos and videos",
    "camera-ois": "OIS for stabilized shots",
    "battery": "excellent battery life",
    "charging": "fast charging support",
    "display": "vibrant high-refresh display",
    "performance": "solid performance for daily tasks and gaming",
    "premium": "premium build and materials",
    "budget": "great value for money",
    "selfie": "good front camera for selfies",
    "design": "attractive design",
    "gaming": "tuned for gaming with good thermals",
    "value": "excellent price-to-performance ratio",
    "ai": "AI-driven camera/software features",
    "onehand": "compact and easy one-hand use",
    "storage": "generous storage option",
    "ram": "ample RAM for multitasking",
    "oled": "OLED display for deep blacks",
    "amoled": "AMOLED screen for vivid colors",
    "midrange": "solid mid-range contender",
    "flagship": "flagship-level specs",
    "durable": "robust build / IP rating",
}

DEFAULT_PHRASES = [
    "a balanced set of features for everyday use",
    "good overall value",
]

def _phrase_for_tags(tags: List[str]) -> str:
    """Create a short natural-language rationale from tags."""
    phrases = []
    clean_tags = [t.lower().replace(" ", "-") for t in tags]
    priority = ["camera", "camera-ois", "battery", "charging", "performance", "display",
                "amoled", "oled", "ai", "gaming", "budget", "premium", "value", "design", "selfie", "onehand"]
    for p in priority:
        if p in clean_tags and p in TAG_PHRASES:
            phrases.append(TAG_PHRASES[p])
    for t in clean_tags:
        if t in TAG_PHRASES and TAG_PHRASES[t] not in phrases:
            phrases.append(TAG_PHRASES[t])
    if not phrases:
        phrases = DEFAULT_PHRASES.copy()
    if len(phrases) == 1:
        return f"Recommended for {phrases[0]}."
    return f"Recommended for {phrases[0]} and {phrases[1]}."

def load_catalog() -> List[Dict[str, Any]]:
    """Load catalog.json and enrich each phone with 'why_recommended'."""
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        phones = json.load(f)

    for p in phones:
        p.setdefault("tags", [])
        p.setdefault("rating", p.get("rating", 4.0))

        # Normalize price
        if "price" not in p and "price_in_inr" in p:
            p["price"] = p["price_in_inr"]

        # Normalize phone name
        if "name" not in p:
            brand = p.get("brand", "")
            model = p.get("model", "")
            p["name"] = f"{brand} {model}".strip() or f"Phone {p.get('id', '')}"

        # Generate why_recommended if missing
        if not p.get("why_recommended"):
            p["why_recommended"] = _phrase_for_tags(p.get("tags", []))

        # Parse string price into int
        if isinstance(p.get("price"), str):
            digits = re.findall(r"\d+", p["price"].replace(",", ""))
            if digits:
                p["price"] = int(digits[0])

        # Normalize RAM and Storage fields
        if "ram" not in p and "ram_gb" in p:
            p["ram"] = f"{p['ram_gb']} GB"
        if "storage" not in p and "storage_gb" in p:
            p["storage"] = f"{p['storage_gb']} GB"

        if "id" not in p:
            p["id"] = f"p_{phones.index(p)+1}"

    return phones

PHONES = load_catalog()

def _extract_budget(query: str) -> int | None:
    """Extract numeric budget from query like '₹30k' or 'under 25k'."""
    if not query:
        return None
    q = query.lower().replace("₹", " ").replace(",", " ")
    m = re.search(r"(\d{1,3}(?:[,\s]\d{3})+|\d+k|\d+)", q)
    if not m:
        return None
    token = m.group(1)
    if token.endswith("k"):
        try:
            return int(float(token[:-1]) * 1000)
        except:
            return None
    digits = re.findall(r"\d+", token)
    return int("".join(digits)) if digits else None

def _extract_brand(query: str) -> str | None:
    """Try to extract a brand name from the query."""
    known_brands = [p["brand"].lower() for p in PHONES]
    for brand in set(known_brands):
        if brand in query.lower():
            return brand
    return None

def search_phones(query: str, max_results: int = 6) -> List[Dict[str, Any]]:
    """Search phones by keywords, brand, budget, or comparison query."""
    if not query:
        # Return top rated phones if no query
        results = sorted(PHONES, key=lambda x: (-x["rating"], x.get("price", 10**9)))
        return results[:max_results]

    q = query.lower().strip()
    budget = _extract_budget(q)
    brand_filter = _extract_brand(q)
    tokens = re.findall(r"\w+", q)

    # --- 🔍 Detect explicit comparison queries like "compare oneplus_12r vs pixel 8a"
    if "compare" in q and (" vs " in q or "versus" in q):
        parts = re.split(r"\bvs\b|\bversus\b", q)
        if len(parts) == 2:
            left, right = parts[0], parts[1]
            left = left.replace("compare", "").strip()
            right = right.strip()
            matches = []
            for p in PHONES:
                name = p["name"].lower()
                model = str(p.get("model", "")).lower()
                pid = str(p.get("id", "")).lower()
                # Match by name, id, or model
                if any(x in name or x in model or x in pid for x in [left, right]):
                    matches.append(p)
            if matches:
                return matches

    results = []
    for p in PHONES:
        hay = " ".join([
            str(p.get("brand", "")).lower(),
            str(p.get("name", "")).lower(),
            " ".join([t.lower() for t in p.get("tags", [])])
        ])
        matched = False

        # ✅ Budget match
        if budget and isinstance(p.get("price"), int) and p["price"] <= budget:
            matched = True

        # ✅ Brand match
        if brand_filter and p["brand"].lower() != brand_filter:
            continue
        if budget and isinstance(p.get("price"), int) and p["price"] > budget:
            continue
        matched = True


        # ✅ Token match
        for t in tokens:
            if t and t in hay:
                matched = True
                break

        if matched:
            results.append(p)

    # Sort results: high rating, then low price
    results = sorted(results, key=lambda x: (-x.get("rating", 0), x.get("price", 10**9)))

    # If no results, provide top alternatives for fallback messaging
    if not results:
        alt = sorted(PHONES, key=lambda x: (-x.get("rating", 0), x.get("price", 10**9)))[:max_results]
        return alt

    return results[:max_results]


def compare_phones(ids: List[str]) -> Dict[str, Any] | None:
    """Compare phones by IDs or models and return a structured comparison table."""
    selected = [p for p in PHONES if p["id"] in ids or p["model"].lower() in [x.lower() for x in ids]]

    if not selected:
        return None

    specs = {}
    keys = ["display", "processor", "camera", "battery", "ram", "storage", "os"]

    for key in keys:
        specs[key.capitalize()] = [p.get(key, "N/A") for p in selected]

    rationales = [p.get("why_recommended", "") for p in selected]

    return {
        "title": "Comparison Table",
        "names": [p["name"] for p in selected],
        "specs": specs,
        "rationales": rationales,
    }

# def search_phones(query: str, max_results: int = 6) -> List[Dict[str, Any]]:
#     """Search phones by keywords and budget. Returns enriched phone objects."""
#     if not query:
#         results = sorted(PHONES, key=lambda x: (-x["rating"], x.get("price", 10**9)))
#         return results[:max_results]

#     q = query.lower()
#     budget = _extract_budget(q)
#     brand_filter = _extract_brand(q)
#     tokens = re.findall(r"\w+", q)

#     results = []
#     for p in PHONES:
#         hay = " ".join([
#             str(p.get("brand", "")).lower(),
#             str(p.get("name", "")).lower(),
#             " ".join([t.lower() for t in p.get("tags", [])])
#         ])
#         matched = False

#         # ✅ Budget filter (inclusive)
#         if budget and isinstance(p.get("price"), int) and p["price"] <= budget:
#             matched = True

#         # ✅ Brand filter (case-insensitive)
#         if brand_filter and p["brand"].lower() != brand_filter:
#             continue
#         if budget and isinstance(p.get("price"), int) and p["price"] > budget:
#             continue
#         matched = True

#         # Token match
#         for t in tokens:
#             if t and t in hay:
#                 matched = True
#                 break

#         if matched:
#             results.append(p)

#     results = sorted(results, key=lambda x: (-x.get("rating", 0), x.get("price", 10**9)))
#     return results[:max_results]

# def compare_phones(ids):
#     selected = [p for p in PHONES if p["id"] in ids]
#     if not selected:
#         return None

#     specs = {}
#     # Include RAM/Storage correctly
#     for key in ["display", "processor", "camera", "battery", "ram", "storage", "os"]:
#         specs[key.capitalize()] = [p.get(key, "N/A") for p in selected]

#     rationales = [p.get("why_recommended", "") for p in selected]

#     return {
#         "title": "Comparison Table",
#         "names": [p["name"] for p in selected],
#         "specs": specs,
#         "rationales": rationales,
#     }
