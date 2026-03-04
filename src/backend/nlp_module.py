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
        "ram": None,
        "ssd": None
    }

    # price detection
    match = re.search(r'(under|below)\s*(\d+)', query)
    if match:
        result["price_limit"] = int(match.group(2))


    # above / over
    match = re.search(r'(above|over)\s*(\d+)', query)
    if match:
        result["price_min"] = int(match.group(2))

  
    # ------------------------
    # RAM detection (with min/max)
    # ------------------------
    # Detect "above" / "over" RAM
    ram_min_match = re.search(r'(above|over)\s*(\d+)\s*(gb)?\s*ram', query)
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
    
        

    # SSD detection
    ssd_match = re.search(r'(\d+)\s*gb\s*ssd', query)
    if ssd_match:
        result["ssd"] = int(ssd_match.group(1))

    # performance detection
    if "gaming" in query:
        result["performance"] = "gaming"

    return result

# ------------------------
# CREATE FEATURE VECTOR
# ------------------------
def create_feature_vector(preferences):

    feature_vector = {
        "price_limit": preferences["price_limit"] if preferences["price_limit"] else 0,
        "price_min": preferences["price_min"] if preferences["price_min"] else 0,
        "ram": preferences["ram"] if preferences["ram"] else 0,
        "ssd": preferences["ssd"] if preferences["ssd"] else 0,
        "gaming": 1 if preferences["performance"] == "gaming" else 0
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

    # gaming filter
    if preferences["performance"] == "gaming":
        filtered = [
            item for item in filtered
            if "gaming" in item["Model"].lower()
        ]

    print("Parsed preferences:", preferences)
    print("Feature vector for KNN:", feature_vector)
    # print("Filtered dataset:", filtered)
    
    return {
        "parsed_preferences": preferences,
        "feature_vector_for_knn": feature_vector,
        "filtered_results": filtered
    }

    