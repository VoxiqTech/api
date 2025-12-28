# GfG Profile API

A fast, lightweight FastAPI service to fetch GeeksforGeeks user profile data from public profiles.

**No Authentication Required** - all data is extracted from public profile pages!

## Features

- ✅ Fetch profile data for any public GfG user
- ✅ Extract scoring data, problem statistics, and more
- ✅ Handles Next.js dynamic data structures
- ✅ Ready for **Vercel Deployment**
- ✅ Performance monitoring compatible with **Vercel Speed Insights**
- ✅ CORS enabled for frontend integration

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

## Performance Monitoring with Vercel Speed Insights

This API is optimized for monitoring with **Vercel Speed Insights**. The API includes:

- **CORS headers** - Frontend applications can make requests and measure performance
- **Performance metrics headers** - `X-Response-Time` and `Server-Timing` headers track API latency
- **Caching headers** - Responses include `Cache-Control` headers for optimal performance
- **Compatible with frontend integration** - Works seamlessly with frontend apps using `@vercel/speed-insights`

### Setting Up Speed Insights with a Frontend

If you have a frontend application (React, Next.js, Vue, etc.) that uses this API, you can track end-to-end performance:

1. **Install the Speed Insights package** in your frontend:
   ```bash
   npm install @vercel/speed-insights
   ```

2. **Add the SpeedInsights component** to your app:
   
   **React/Next.js:**
   ```jsx
   import { SpeedInsights } from '@vercel/speed-insights/react';
   
   export default function App() {
     return (
       <>
         {/* Your app content */}
         <SpeedInsights />
       </>
     );
   }
   ```

   **Vue/Nuxt:**
   ```vue
   <script setup>
   import { SpeedInsights } from '@vercel/speed-insights/vue';
   </script>

   <template>
     <SpeedInsights />
   </template>
   ```

   **Other Frameworks:** See [Vercel Speed Insights documentation](https://vercel.com/docs/speed-insights/quickstart)

3. **Deploy to Vercel** - The Speed Insights dashboard will track:
   - Frontend performance metrics (Core Web Vitals)
   - API response times (via Server-Timing headers)
   - User experience metrics across all requests

### Performance Metrics Exposed

This API exposes the following headers for performance monitoring:

- **X-Response-Time** - Total response time in milliseconds
- **Server-Timing** - Detailed timing data for performance analysis
- **Cache-Control** - Caching directives for optimized performance

### Vercel Deployment

The application is already configured for Vercel deployment:

```bash
vercel deploy
```

Once deployed, enable Speed Insights in the Vercel dashboard for your project to start tracking performance metrics.

## Project Structure

```
gfg api/
├── main.py              # FastAPI application with monitoring
├── scraper.py           # Scraping logic (Next.js support)
├── requirements.txt     # Dependencies
├── vercel.json          # Vercel deployment config
└── README.md           # Documentation
```

## Troubleshooting

**"Profile not found" error:**
1. Verify the username is correct and public on GeeksforGeeks.
2. Check if the profile URL is accessible in a browser.

**CORS errors in browser console:**
- This API has CORS enabled, so cross-origin requests should work
- Ensure your frontend is making requests to the correct API endpoint

**Speed Insights not showing data:**
- Ensure your app is deployed on Vercel
- Speed Insights is enabled in your Vercel project settings
- Wait a few minutes to 1 hour for initial data collection
- Check that your frontend includes the SpeedInsights component

## Learn More

- [Vercel Speed Insights Quickstart](https://vercel.com/docs/speed-insights/quickstart)
- [@vercel/speed-insights Package Documentation](https://vercel.com/docs/speed-insights/package)
- [Vercel Speed Insights Metrics Guide](https://vercel.com/docs/speed-insights/metrics)
