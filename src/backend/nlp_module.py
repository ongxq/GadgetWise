import re
from supabase_client import supabase


# ------------------------
# NLP PARSER
# ------------------------
def parse_query(query):

    query = query.lower()

    result = {
        "price_limit": None,
        "price_min": None,
        "performance": None,
        "gaming_only": False,
        "ram": None,
        "ssd": None,
        "brand": None,
        "generation": None,
        "rating_min": None,
        "core_min": None,
        "display_size_min": None,
        "os": None,
        "dedicated_gpu": None,
        "vram_min": None,

        # NEW preference
        "budget_preference": None,
        "cpu_score": None
    }

    cheap_words = ["cheap", "budget", "affordable", "low price", "value","murah", "harga rendah"]
    premium_words = ["premium", "expensive", "high end", "best","mahal", "premium"]

    for word in cheap_words:
        if word in query:
            result["budget_preference"] = "cheap"
            break

    for word in premium_words:
        if word in query:
            result["budget_preference"] = "premium"
            break
    
    if result["budget_preference"] == "cheap" and not result["price_limit"]:
        result["price_limit"] = 2000  # default cheap max price
    # price detection
    match = re.search(r'(under|below|bawah)\s*(price)?\s*(rm)?\s*(\d+)', query)
    if match:
        result["price_limit"] = int(match.group(4))


    # above / over
    match = re.search(r'(above|over|di atas)\s*(\d+)', query)
    if match:
        result["price_min"] = int(match.group(2))

  
    # ------------------------
    # RAM detection (with min/max)
    # ------------------------
    # Detect "above" / "over" RAM
    ram_min_match = re.search(r'(above|over|lebih dari|di atas)\s*(\d+)\s*(gb)?\s*ram', query)
    if ram_min_match:
        result["ram"] = int(ram_min_match.group(2))

    # Detect exact RAM mentions, e.g., "16 GB RAM"
    ram_match = re.search(r'(\d+)\s*(gb)?\s*ram', query)
    if ram_match:
        value = int(ram_match.group(1))
        # only set if not already set by above/over
        if not result["ram"]:
            result["ram"] = value
        ram_match = re.search(r'(\d+)\s*(gb)?\s*ram', query)
        if ram_match:
            value = int(ram_match.group(1))
    
    # Detect if user explicitly wants gaming laptop
    if "gaming" in query:
        result["gaming_only"] = True
        result["performance"] = "gaming"    

     # Performance keywords (English + Malay)
    high_perf_keywords = [
        "gaming", "video editing", "rendering", "3d modeling", "graphic design", "heavy software",
        "prestasi tinggi", "main game", "video editing berat", "rendering berat"
    ]
    for kw in high_perf_keywords:
        if kw in query:
            result["performance"] = "high"
            break


    # ------------------------
    # Brand detection (simple)
    # ------------------------
    brands = ["acer","apple","asus","avita","axl","chuwi","colorful","dell","fujitsu","gigabyte","honor","hp","huawei","iball","infinix","jio","lenovo","lg","microsoft","msi","ninkear","primebook","razer","samsung","tecno","ultimus","walker","wings","xiaomi","zebronics"]
    for b in brands:
        if b in query:
            result["brand"] = b
            break
    

    # Generation & CPU series detection
    # ------------------------
    # 1. Detect Gen style (e.g., 5th Gen, 12th Gen)
    gen_match = re.search(r'(\d+)(th|st|nd|rd)\s*gen', query)
    if gen_match:
        result["generation"] = gen_match.group(0)

    # 2. Detect Intel/AMD series (i3/i5/i7/i9, Ryzen 3/5/7/9, Apple M1/M2/M3)
    series_match = re.search(r'\b(i[3-9]|ryzen\s?[3-9]|m\d+)\b', query, re.IGNORECASE)
    if series_match:
        result["cpu_series"] = series_match.group(0)

    # 3. Detect Intel Core Ultra / Series style (e.g., Ultra 7 Series)
    ultra_match = re.search(r'ultra\s?(\d+)\s?series', query, re.IGNORECASE)
    if ultra_match:
        result["generation_tier"] = ultra_match.group(1)  # e.g., 7 in Ultra 7

    # 4. Detect suffix letters (U, H, HX, P)
    suffix_match = re.search(r'\b([uhhxp]{1,2})\b', query)
    if suffix_match:
        result["suffix"] = suffix_match.group(1).upper()

    # Rating min
    rating_match = re.search(r'(above|over|di atas|lebih dari)\s*(\d+)\s*rating', query)
    if rating_match:
        result["rating_min"] = int(rating_match.group(2))

    # Core detection
    core_match = re.search(r'(above|over|di atas|lebih dari)\s*(\d+)\s*core', query)
    if core_match:
        result["core_min"] = int(core_match.group(2))

    # Display size
    display_match = re.search(r'(above|over|di atas|lebih dari)\s*([\d\.]+)\s*inch', query)
    if display_match:
        result["display_size_min"] = float(display_match.group(2))

    # OS detection
    os_list = ["windows", "mac os", "macos", "windows 10", "windows 11"]
    for os_name in os_list:
        if os_name in query:
            result["os"] = os_name
            break

    # GPU / VRAM detection
    vram_match = re.search(r'(at least|above|over|di atas|lebih dari)\s*(\d+)\s*gb\s*(gpu|graphics)', query)
    if vram_match:
        result["vram_min"] = int(vram_match.group(2))
        result["dedicated_gpu"] = True  # assume VRAM means dedicated GPU
    

    # detect if user simply says "gpu"
    if "gpu" in query or "graphics" in query:
        result["dedicated_gpu"] = True
    
    return result
# ------------------------
# CREATE FEATURE VECTOR
# ------------------------
def create_feature_vector(preferences):
    budget_score = 0

    if preferences["budget_preference"] == "cheap":
        budget_score = -1
    elif preferences["budget_preference"] == "premium":
        budget_score = 1
    feature_vector = {
        "price_limit": preferences["price_limit"] if preferences["price_limit"] else 0,
        "price_min": preferences["price_min"] if preferences["price_min"] else 0,
        "ram": preferences["ram"] if preferences["ram"] else 0,
        "ssd": preferences["ssd"] if preferences["ssd"] else 0,
        "gaming": 1 if preferences["performance"] == "gaming" else 0,
        "rating_min": preferences["rating_min"] or 0,
        "core_min": preferences["core_min"] or 0,
        "display_size_min": preferences["display_size_min"] or 0,
        "vram_min": preferences["vram_min"] or 0,
        "dedicated_gpu": 1 if preferences["dedicated_gpu"] else 0,
        "budget_pref": budget_score
    }

    return feature_vector




# ------------------------
# FILTER DATASET
# ------------------------
def filter_dataset(query):

    preferences = parse_query(query)

    # create feature vector for AI module
    feature_vector = create_feature_vector(preferences)
    
    # fetch dataset from supabase
    response = supabase.table("laptop").select("*").execute()
    data = response.data

    filtered = data

    # price filter
    if preferences["price_limit"]:
        filtered = [
            item for item in filtered
            if item["Price (RM)"] <= preferences["price_limit"]
        ]


    # minimum price
    if preferences["price_min"]:
        filtered = [
            item for item in filtered
            if item["Price (RM)"] >= preferences["price_min"]
     ]

    # RAM filter
    if preferences["ram"]:
        filtered = [
            item for item in filtered
            if int(re.search(r'\d+', item["Ram"]).group()) >= preferences["ram"]
        ]

    # SSD filter
    if preferences["ssd"]:
        filtered = [
            item for item in filtered
            if str(preferences["ssd"]) in item["SSD"]
        ]

    # Gaming filter
    if preferences.get("gaming_only"):
        # Only include laptops marked as gaming in dataset
        filtered = [item for item in filtered if item.get("Gaming?") == "Yes"]
    elif preferences.get("performance") == "high":
        # High-performance non-gaming: favor high RAM, VRAM, cores, SSD in scoring
        pass  # Keep them for ranking; no strict filter


    # Brand filter
    if preferences.get("brand"):
        filtered = [
            item for item in filtered
            if preferences["brand"].lower() in item["Brand"].lower()
    ]
    # Generation filter
    if preferences.get("generation"):
        filtered = [item for item in filtered if preferences["generation"].lower() in item["Generation"].lower()]

    # CPU series filter
    if preferences.get("cpu_series"):
        filtered = [
            item for item in filtered
            if preferences["cpu_series"].lower() in item["Generation"].lower() 
            or preferences["cpu_series"].lower() in item["Model"].lower()
    ]

# Ultra / series tier filter
    if preferences.get("generation_tier"):
        filtered = [
            item for item in filtered
            if preferences["generation_tier"] in item["Generation"] 
            or preferences["generation_tier"] in item["Model"]
    ]
    # Rating filter
    if preferences.get("rating_min"):
        filtered = [item for item in filtered if float(item["Rating"]) >= preferences["rating_min"]]

    # Core filter
    if preferences.get("core_min"):
        def get_core_count(core_str):
            match = re.search(r'(\d+)\s*Cores', core_str)
            return int(match.group(1)) if match else 0
        filtered = [item for item in filtered if get_core_count(item["Core"]) >= preferences["core_min"]]

    # Display filter
    if preferences.get("display_size_min"):
        def get_display_size(display_str):
            match = re.search(r'([\d\.]+)\s*inches', display_str)
            return float(match.group(1)) if match else 0
        filtered = [item for item in filtered if get_display_size(item["Display"]) >= preferences["display_size_min"]]

    # OS filter
    if preferences.get("os"):
        filtered = [item for item in filtered if preferences["os"].lower() in item["OS"].lower()]

    # VRAM / Dedicated GPU filter using dataset columns directly
    if preferences.get("vram_min") or preferences.get("dedicated_gpu"):
        filtered = [
            item for item in filtered
            if (item.get("Dedicated Gpu") == "Yes" if preferences.get("dedicated_gpu") else True) 
            and int(item.get("VRAM", 0)) >= (preferences.get("vram_min") or 0)
        ]

    print("Parsed preferences:", preferences)
    print("Feature vector for KNN:", feature_vector)
    # print("Filtered dataset:", filtered)
    
    return {
        "parsed_preferences": preferences,
        "feature_vector_for_knn": feature_vector,
        "filtered_results": filtered
    }
    