from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from recommendation import recommend
from nlp_module import filter_dataset

app = FastAPI()

class Query(BaseModel):
    query: str


# Allow requests from your frontend
origins = [
    "http://localhost:3000",
    # you can add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allow these origins
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"],         # allow all headers
)


@app.get("/")
def root():
    return {"message": "Backend is running!"}

# @app.post("/recommend")
# def get_recommendation(data: Query):
#     try:
#         results = recommend(data.query)

#         # DEBUG: print the results to backend console
#         print("Recommendation results:", results)

#         return results
#     except Exception as e:
#         print("Error in recommendation:", str(e))
#         return {"error": str(e)}


@app.post("/test_nlp")
def test_nlp(data: Query):

    
        results = filter_dataset(data.query)

        

        return results