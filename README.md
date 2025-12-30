# GeeksforGeeks Profile API

A fast, lightweight FastAPI service to extract user profile data from GeeksforGeeks, including detailed problem-solving statistics by difficulty.

## Features
- **Hybrid Extraction**: Combines HTML scraping for profile stats with a direct API call for problem breakdown.
- **Detailed Stats**: Fetches Coding Score, Total Problems Solved, Institute Rank, and Articles Published.
- **Problem Breakdown**: Accurate counts for School, Basic, Easy, Medium, and Hard problems.

## Setup

### Prerequisites
- Python 3.9+

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally
Start the server:
```bash
python -m uvicorn main:app --reload
```

## API Usage

### Get Profile Data
**Endpoint:** `GET /gfg/{username}`

**Example:**
`http://localhost:8000/gfg/zerotologic`

**Response:**
```json
{
  "username": "zerotologic",
  "profile_url": "https://www.geeksforgeeks.org/profile/zerotologic",
  "institute_rank": "5215",
  "coding_score": 11,
  "total_problems_solved": 5,
  "monthly_coding_score": 0,
  "articles_published": 0,
  "problems_solved_breakdown": {
    "school": 0,
    "basic": 3,
    "easy": 0,
    "medium": 2,
    "hard": 0
  }
}
```
