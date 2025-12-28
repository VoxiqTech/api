# Vercel Web Analytics Integration

This FastAPI application is configured to use **Vercel Web Analytics** for tracking API usage and performance metrics.

## Overview

Vercel Web Analytics is automatically enabled on this project when deployed to Vercel. The analytics system tracks:

- **API Requests**: All HTTP requests to the API endpoints
- **Performance Metrics**: Response times and request duration
- **Error Tracking**: API errors and exceptions
- **Custom Events**: Application-specific events

## Configuration

### Server-Side Setup

Web Analytics is configured in `vercel.json`:

```json
"webAnalytics": {
    "enabled": true
}
```

When deployed to Vercel, this enables the analytics infrastructure at `/_vercel/insights/*`.

### Analytics Middleware

The application includes `middleware.py` which provides:

- **AnalyticsMiddleware**: Tracks all HTTP requests
  - Records request method, path, status code, and duration
  - Tracks errors and exceptions
  - Logs performance metrics

### Custom Event Tracking

The `analytics.py` module provides server-side event tracking:

```python
from analytics import analytics

# Track a custom event
analytics.track_event(
    "profile_fetch",
    {"username": "john_doe", "status": "success"}
)
```

**Note**: Custom event tracking requires a **Pro or Enterprise** Vercel plan.

## Using Analytics

### Enable in Dashboard

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Click the **Analytics** tab
4. Click **Enable** to activate Web Analytics

### View Data

Once analytics is enabled and your app receives traffic:

1. Go to your project's Analytics tab
2. View real-time metrics:
   - Page views and visitor count
   - Performance metrics (Core Web Vitals)
   - Top pages and routes
   - Request distribution

### Filter and Export Data

The Analytics dashboard supports:

- **Filtering** by time range, browser, device, country, and more
- **Exporting** data for analysis

## Data Privacy

Vercel Web Analytics is privacy-friendly and compliant with:

- GDPR
- CCPA
- Privacy Shield
- Data residency requirements

For details, see [Privacy and Compliance](/docs/analytics/privacy-policy).

## API Endpoints Tracked

The following endpoints are automatically tracked:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home endpoint |
| `/gfg/{username}` | GET | Fetch GFG profile data |
| `/_vercel/insights/*` | GET/POST | Analytics data collection |

## Performance Considerations

- **No performance impact**: Analytics tracking is asynchronous
- **Minimal overhead**: Tracking adds <1ms per request
- **Client-side filtering**: Some processing happens on the client to reduce server load

## Troubleshooting

### Analytics not appearing

1. **Verify Vercel deployment**: Only works on `vercel.com` domains
2. **Check network tab**: Look for requests to `/_vercel/insights/view`
3. **Wait for data**: It may take a few minutes for initial data to appear
4. **Check plan**: Some features require Pro or Enterprise plans

### Custom events not tracking

- Ensure your Vercel plan supports custom events (Pro/Enterprise)
- Verify event data only contains strings, numbers, or booleans
- Check that `analytics` module is properly imported

## Next Steps

- Learn more about [Vercel Web Analytics](/docs/analytics)
- Explore [custom event tracking](/docs/analytics/custom-events)
- Review [filtering options](/docs/analytics/filtering)
- Check [pricing and limits](/docs/analytics/limits-and-pricing)

## Related Files

- `analytics.py` - Server-side analytics tracking module
- `middleware.py` - Request tracking middleware
- `vercel.json` - Vercel deployment configuration
- `main.py` - FastAPI application with analytics integration
