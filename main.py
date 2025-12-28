from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_gfg_profile
import time

app = FastAPI(
    title="GFG Profile API",
    description="Fetch GeeksforGeeks user profile data from public profiles",
    version="2.0"
)

# Enable CORS for frontend applications that use Vercel Speed Insights
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware to add performance monitoring headers for Vercel Speed Insights
@app.middleware("http")
async def add_performance_headers(request: Request, call_next):
    """
    Middleware to track and expose performance metrics.
    These headers are compatible with Vercel Speed Insights monitoring.
    Enables frontend applications to measure API performance metrics.
    """
    start_time = time.time()
    response = await call_next(request)
    
    # Calculate response time in milliseconds
    process_time = (time.time() - start_time) * 1000
    
    # Add Vercel-specific headers for monitoring and caching
    response.headers["X-Response-Time"] = f"{process_time:.0f}ms"
    response.headers["Server-Timing"] = f"total;dur={process_time:.0f}"
    
    # Enable caching for profile endpoints to optimize performance
    if request.url.path.startswith("/gfg/"):
        response.headers["Cache-Control"] = "public, max-age=3600"
    
    return response


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
