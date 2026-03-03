import re

def parse_query(query):

    query = query.lower()

    result = {
        "price_limit": None,
        "performance": None,
        "budget": None
    }

    # detect numeric price constraint
    match = re.search(r'(under|below)\s*(\d+)', query)
    if match:
        result["price_limit"] = int(match.group(2))

    # qualitative price
    if "cheap" in query or "affordable" in query or "budget" in query:
        result["budget"] = "low"

    if "mid-range" in query:
        result["budget"] = "medium"

    if "premium" in query:
        result["budget"] = "high"

    # performance keywords
    if "gaming" in query or "performance" in query:
        result["performance"] = "high"

    return result