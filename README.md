# GfG Profile API

A fast, lightweight FastAPI service to fetch GeeksforGeeks user profile data from public profiles.

**No Authentication Required** - all data is extracted from public profile pages!

## Features

- ✅ Fetch profile data for any public GfG user
- ✅ Extract scoring data, problem statistics, and more
- ✅ Handles Next.js dynamic data structures
- ✅ Ready for **Vercel Deployment**

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

## Deployment on Vercel

This project is configured for easy deployment on Vercel.

### 1. Install Vercel CLI (Optional)
If you prefer command line:
```bash
npm i -g vercel
```

### 2. Deploy
Run the deploy command in the project folder:
```bash
vercel
```
Follow the prompts (accept defaults).

### 3. Manual Deployment (Git Integration)
1. Push this code to a GitHub repository.
2. Log in to [Vercel](https://vercel.com).
3. Click **"Add New..."** > **"Project"**.
4. Import your GitHub repository.
5. Vercel will automatically detect the Python configuration (via `vercel.json`) and deploy.

### Configuration
The included `vercel.json` handles the configuration:
```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

## Project Structure

```
gfg api/
├── main.py              # FastAPI application
├── scraper.py           # Scraping logic (Next.js support)
├── requirements.txt     # Dependencies
├── vercel.json          # Deployment config
└── README.md           # Documentation
```

## Troubleshooting

**"Profile not found" error:**
1. Verify the username is correct and public on GeeksforGeeks.
2. Check if the profile URL is accessible in a browser.

**Vercel Deployment Issues:**
- Ensure `requirements.txt` is present and correct.
- Check Vercel logs for build errors.
