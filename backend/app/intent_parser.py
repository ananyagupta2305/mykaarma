import re
from typing import Dict, Any, List


BUDGET_RE = re.compile(r"(?:under|below|<=) \u20B9?\s*([0-9,]+)|(?:around|about|~)\s*\u20B9?\s*([0-9,]+)|\u20B9\s*([0-9,]+)", re.I)
COMPARE_RE = re.compile(r"\bcompare\b|\bvs\b|\bversus\b", re.I)
BRAND_RE = re.compile(r"\b(Samsung|OnePlus|Google|Xiaomi|Redmi|Vivo|Realme|Apple|iPhone)\b", re.I)
FEATURE_KEYWORDS = [
"camera", "battery", "charging", "fast charging", "compact", "one-hand", "ois", "eis",
"display", "ram", "storage", "performance", "gaming"
]



def parse_intent(text: str) -> Dict[str, Any]:
    intent = {"raw": text, "budget_in_inr": None, "compare": False, "brands": [], "features": []}
    # Budget
    m = BUDGET_RE.search(text)
    if m:
        for g in m.groups():
            if g:
                num = int(g.replace(",", ""))
                intent["budget_in_inr"] = num
                break
    # Compare
    if COMPARE_RE.search(text):
        intent["compare"] = True
    # Brands
    brands = BRAND_RE.findall(text)
    if brands:
        intent["brands"] = [b for b in brands]
    # Features
    text_low = text.lower()
    found = []
    for k in FEATURE_KEYWORDS:
        if k in text_low:
            found.append(k)
    intent["features"] = found
    return intent