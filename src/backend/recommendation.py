# # recommendation.py
# from nlp_module import parse_query
# from supabase_client import get_dataset

# def normalize_laptop(l):
#     """
#     Map Supabase laptop fields to standard keys expected by scoring:
#     name, brand, price_rm, processor
#     """
#     return {
#         # If your table has a product/model name column, replace "Brand" here
#         "name": l.get("Brand") + " " + l.get("Generation", ""),  
#         "brand": l.get("Brand") or "Unknown",
#         "price_rm": l.get("Price (RM)") or l.get("Price") or 0,
#         "processor": l.get("Generation") or "Unknown",
#         **l
#     }

# def score_laptop(laptop, prefs):
#     """
#     Assign a score based on CPU performance and budget preferences
#     """
#     score = 0
#     cpu = laptop.get("processor", "").lower()
#     price = laptop.get("price_rm", 0)

#     # Performance scoring
#     if prefs.get("performance") == "high":
#         if any(x in cpu for x in ["i7", "i9", "ryzen 7", "ryzen 9"]):
#             score += 3
#         elif any(x in cpu for x in ["i5", "ryzen 5"]):
#             score += 2

#     # Budget scoring
#     budget = prefs.get("budget")
#     if budget == "low" and price < 2000:
#         score += 2
#     elif budget == "medium" and 2000 <= price <= 5000:
#         score += 2

#     return score

# def recommend(query):
#     """
#     Returns top 5 laptops from Supabase based on the parsed query
#     """
#     try:
#         # Parse query to extract preferences
#         prefs = parse_query(query)
#         prefs.setdefault("performance", "medium")
#         prefs.setdefault("budget", "medium")
#         prefs.setdefault("price_limit", None)

#         # Get dataset from Supabase
#         laptops = get_dataset() or []

#         # Normalize fields so scoring works
#         laptops = [normalize_laptop(l) for l in laptops]

#         # Remove laptops without required fields
#         laptops = [
#             l for l in laptops
#             if l.get("name") != "Unknown" and l.get("brand") != "Unknown"
#         ]

#         # Apply price filter if specified
#         if prefs["price_limit"]:
#             laptops = [l for l in laptops if l.get("price_rm", 0) <= prefs["price_limit"]]

#         # Score laptops
#         for laptop in laptops:
#             laptop["score"] = score_laptop(laptop, prefs)

#         # Sort by score descending
#         laptops = sorted(laptops, key=lambda x: x["score"], reverse=True)

#         # Debug: print recommendations in backend
#         print("Recommendation results:", laptops[:5])

#         # Return top 5
#         return [dict(l) for l in laptops[:5]]

#     except Exception as e:
#         # Return error for debugging
#         print("Error in recommendation:", str(e))
#         return {"error": str(e)}