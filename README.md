# GfG Profile API

A fast, lightweight FastAPI service to fetch GeeksforGeeks user profile data from public profiles.

**No Authentication Required** - all data is extracted from public profile pages!

## Features

- ✅ Fetch profile data for any public GfG user
- ✅ Extract scoring data, problem statistics, and more
- ✅ Handles Next.js dynamic data structures
- ✅ Ready for **Vercel Deployment**
- ✅ Built-in **Vercel Web Analytics** support for tracking API usage

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Locally

```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### `GET /`
Home endpoint showing API status.

### `GET /gfg/{username}`
Fetch GfG profile data.

**Example:**
```bash
curl http://localhost:8000/gfg/zerotologic
```

**Response:**
```json
{
  "username": "zerotologic",
  "name": "User Name",
  "overall_coding_score": 2,
  "total_problems_solved": 1,
  "monthly_score": 0,
  "institute_rank": 987,
  "profile_image_url": "...",
  "created_date": "2025-05-25 15:00:27"
}
```

## Project Structure

```
gfg api/
├── main.py              # FastAPI application with analytics
├── scraper.py           # Scraping logic (Next.js support)
├── analytics.py         # Server-side analytics tracking
├── middleware.py        # Request tracking middleware
├── requirements.txt     # Dependencies
├── vercel.json          # Deployment config
├── ANALYTICS.md         # Analytics documentation
└── README.md           # Documentation
```

## Analytics

Vercel Web Analytics is pre-configured for tracking API usage and performance metrics. See [ANALYTICS.md](./ANALYTICS.md) for detailed setup and usage instructions.

## Troubleshooting

**"Profile not found" error:**
1. Verify the username is correct and public on GeeksforGeeks.
2. Check if the profile URL is accessible in a browser.

**Analytics not working:**
1. Ensure the app is deployed to Vercel
2. Enable Web Analytics in your Vercel project settings
3. See [ANALYTICS.md](./ANALYTICS.md) for more details
