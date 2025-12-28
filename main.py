from fastapi import FastAPI, HTTPException
from scraper import get_gfg_profile

app = FastAPI(
    title="GFG Profile API",
    description="Fetch GeeksforGeeks user profile data from public profiles",
    version="2.0"
)

@app.get("/")
def home():
    return {
        "message": "GFG Profile API is running",
        "version": "2.0",
        "note": "No authentication required - fetches public profile data",
        "endpoints": {
            "profile": "GET /gfg/{username}",
            "docs": "GET /docs"
        }
    }

@app.get("/gfg/{username}")
def fetch_gfg_profile(username: str):
    """
    Fetch GfG profile data for any user from their public profile page
    
    No authentication required - all data is publicly available on GfG profiles.
    """
    data = get_gfg_profile(username)

    if not data:
        raise HTTPException(
            status_code=404, 
            detail=f"Profile not found for username: {username}. Please check the username and try again."
        )

    return data

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return {}
