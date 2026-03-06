# # recommendation.py
# import re


# # ------------------------
# # Weighted scoring for top laptops
# # ------------------------
# def recommend_top_laptops(filtered_data, feature_vector, top_k=3):
#     scored_laptops = []

#     for laptop in filtered_data:
#         score = 0
#         weights = {
#             "ram": 2,
#             "ssd": 1,
#             "vram": 2,
#             "gaming": 3,
#             "rating": 2,
#             "price": 1
#         }

#         # RAM
#         try:
#             laptop_ram = int(re.search(r'\d+', laptop.get("Ram","0")).group())
#         except:
#             laptop_ram = 0
#         score += laptop_ram * weights["ram"]

#         # SSD
#         try:
#             laptop_ssd = int(re.search(r'\d+', laptop.get("SSD","0")).group())
#         except:
#             laptop_ssd = 0
#         score += laptop_ssd * weights["ssd"]

#         # VRAM / Dedicated GPU scoring
#         laptop_vram = int(laptop.get("VRAM", 0))
#         if feature_vector["dedicated_gpu"] and laptop.get("Dedicated Gpu") != "Yes":
#             laptop_vram = 0  # no score if user wants dedicated GPU but laptop doesn't have
#         score += laptop_vram * weights["vram"]

#         # Gaming preference
#         if feature_vector["gaming"] and "gaming" in laptop.get("Model","").lower():
#             score += weights["gaming"]

#         # Rating
#         try:
#             laptop_rating = float(laptop.get("Rating",0))
#         except:
#             laptop_rating = 0
#         score += laptop_rating * weights["rating"]

#         # Price preference
#         if feature_vector["budget_pref"] < 0:  # cheap
#             price_limit = feature_vector["price_limit"] if feature_vector["price_limit"] else 0
#             price_score = max(price_limit - laptop.get("Price (RM)",0),0)/1000
#             score += price_score * weights["price"]

#         scored_laptops.append((score, laptop))

#     # Sort descending
#     scored_laptops.sort(key=lambda x: x[0], reverse=True)
#     top_laptops = [laptop for score, laptop in scored_laptops[:top_k]]
#     return top_laptops

# recommendation.py
import re
import math

# ------------------------
# Weighted + KNN scoring for top laptops
# ------------------------
def recommend_top_laptops(filtered_data, feature_vector, top_k=3, knn_weight=0.5, weighted_weight=0.5):
    scored_laptops = []

    for laptop in filtered_data:
        # ------------------------
        # Weighted scoring
        # ------------------------
        score_weighted = 0
        weights = {
            "ram": 2,
            "ssd": 1,
            "vram": 2,
            "gaming": 3,
            "rating": 2,
            "price": 1
        }

        # RAM
        try:
            laptop_ram = int(re.search(r'\d+', laptop.get("Ram","0")).group())
        except:
            laptop_ram = 0
        score_weighted += laptop_ram * weights["ram"]

        # SSD
        try:
            laptop_ssd = int(re.search(r'\d+', laptop.get("SSD","0")).group())
        except:
            laptop_ssd = 0
        score_weighted += laptop_ssd * weights["ssd"]

        # VRAM / Dedicated GPU
        laptop_vram = int(laptop.get("VRAM", 0))
        if feature_vector["dedicated_gpu"] and laptop.get("Dedicated Gpu") != "Yes":
            laptop_vram = 0
        score_weighted += laptop_vram * weights["vram"]

        # Gaming preference
        if feature_vector["gaming"] and "gaming" in laptop.get("Model","").lower():
            score_weighted += weights["gaming"]

        # Rating
        try:
            laptop_rating = float(laptop.get("Rating",0))
        except:
            laptop_rating = 0
        score_weighted += laptop_rating * weights["rating"]

        # Price preference (cheap)
        if feature_vector["budget_pref"] < 0:
            price_limit = feature_vector["price_limit"] if feature_vector["price_limit"] else 0
            price_score = max(price_limit - laptop.get("Price (RM)",0),0)/1000
            score_weighted += price_score * weights["price"]

        # ------------------------
        # KNN similarity scoring (Euclidean distance)
        # ------------------------
        # create laptop vector same as feature_vector
        laptop_vector = [
            laptop_ram,
            laptop_ssd,
            laptop_vram,
            1 if "gaming" in laptop.get("Model","").lower() else 0,
            laptop_rating,
            laptop.get("Price (RM)",0)
        ]
        user_vector = [
            feature_vector["ram"],
            feature_vector["ssd"],
            feature_vector["vram_min"],
            feature_vector["gaming"],
            feature_vector["rating_min"],
            feature_vector["price_limit"] or 0
        ]
        # Euclidean distance
        dist = math.sqrt(sum((lv - uv)**2 for lv, uv in zip(laptop_vector, user_vector)))
        score_knn = 1 / (1 + dist)  # higher is better

        # ------------------------
        # Combine weighted score + KNN similarity
        # ------------------------
        final_score = weighted_weight * score_weighted + knn_weight * score_knn
        scored_laptops.append((final_score, laptop))

    # Sort descending
    scored_laptops.sort(key=lambda x: x[0], reverse=True)
    top_laptops = [laptop for score, laptop in scored_laptops[:top_k]]
    return top_laptops