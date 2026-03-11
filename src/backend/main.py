# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from recommendation import recommend_top_laptops
# from nlp_module import filter_dataset

# app = FastAPI()

# # class Query(BaseModel):
# #     query: str




# # Allow requests from your frontend
# origins = [
#     "http://localhost:3000",
#     # you can add more origins if needed
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,       # allow these origins
#     allow_credentials=True,
#     allow_methods=["*"],         # allow all HTTP methods
#     allow_headers=["*"],         # allow all headers
# )

# class QueryRequest(BaseModel):
#     query: str
#     top_k: int = 3  # default top 3 recommendations

# @app.get("/")
# def root():
#     return {"message": "Backend is running!"}

# @app.post("/recommend")
# def recommend(request: QueryRequest):
#     # Step 1: NLP filter dataset
#     data = filter_dataset(request.query)

#     # Step 2: Weighted scoring
#     top3 = recommend_top_laptops(data["filtered_results"], data["feature_vector_for_knn"], top_k=3)

#     # Step 3: Return JSON
#     return {
#         "parsed_preferences": data["parsed_preferences"],
#         "top_recommendations": top3
#     }


# # @app.post("/test_nlp")
# # def test_nlp(data: Query):

    
# #         results = filter_dataset(data.query)

        

# #         return results

# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nlp_module import filter_dataset
from recommendation import recommend_top_laptops

app = FastAPI()

# ------------------------
# CORS middleware
# ------------------------
origins = [
    "http://localhost:3000",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Request model
# ------------------------
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3  # default top 3

# ------------------------
# Helper: normalize Supabase keys for frontend
# ------------------------
def normalize_laptop_keys(laptop):
    return {
        "model": laptop.get("Model"),
        "brand": laptop.get("Brand"),
        "price": laptop.get("Price (RM)"),
        "ram": laptop.get("Ram"),
        "ssd": laptop.get("SSD"),
        "gpu": laptop.get("Graphics"),
    }



@app.get("/")
def root():
    return {"message": "Backend is running!"}

# ------------------------
# API endpoint
# ------------------------
@app.post("/recommend")
def recommend(request: QueryRequest):
    # Step 1: NLP filter dataset
    data = filter_dataset(request.query)

    # Step 2: Weighted scoring / top-k recommendation
    top_laptops = recommend_top_laptops(
        data["filtered_results"],
        data["feature_vector_for_knn"],
        top_k=request.top_k
    )

    # Step 3: Normalize keys for frontend
    top_laptops_normalized = [normalize_laptop_keys(l) for l in top_laptops]

    # Step 4: Return JSON
    return {
        "parsed_preferences": data["parsed_preferences"],
        "recommendations": top_laptops_normalized
    }