import os
from supabase import create_client
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the URL and key from your environment
url = os.getenv("VITE_SUPABASE_URL")        # matches your .env
key = os.getenv("VITE_SUPABASE_ANON_KEY")   # matches your .env

# Create Supabase client
supabase = create_client(url, key)

def get_dataset():
    """
    Fetch all laptops from Supabase table 'laptop'
    Returns a list of dictionaries.
    """
    response = supabase.table("laptop").select("*").execute()

    # DEBUG: print what is returned
    print("Supabase response:", response)
    if response.data:
        print("Data fetched:", response.data)
    else:
        print("No data found in table 'laptop'!")

    return response.data or []