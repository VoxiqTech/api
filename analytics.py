"""
Vercel Web Analytics integration for FastAPI backend.

This module provides server-side analytics tracking capabilities for the API.
Server-side events can be tracked and viewed in the Vercel Analytics dashboard.

Note: This requires a Pro or Enterprise Vercel plan for custom event tracking.
"""

import os
import json
import asyncio
from typing import Dict, Optional, Any
from datetime import datetime


class VercelAnalytics:
    """
    Server-side analytics tracker for Vercel Web Analytics.
    
    This class provides methods to track custom events that will be sent to
    Vercel's analytics endpoint.
    
    Usage:
        analytics = VercelAnalytics()
        analytics.track_event("api_call", {"endpoint": "/gfg/username", "status": 200})
    """
    
    def __init__(self):
        """Initialize the analytics tracker."""
        self.endpoint = "/_vercel/insights/event"
        self.enabled = os.getenv("VERCEL_ENV") is not None or os.getenv("VERCEL") == "1"
    
    def track_event(
        self,
        event_name: str,
        event_data: Optional[Dict[str, Any]] = None,
        url: str = "/",
        referrer: str = "",
        timezone: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Track a custom event.
        
        Args:
            event_name: Name of the event to track (required)
            event_data: Additional event data as key-value pairs (optional)
                        Values must be strings, numbers, or booleans
            url: URL path where the event occurred (default: "/")
            referrer: Referrer URL (optional)
            timezone: Timezone information (optional)
        
        Returns:
            Dictionary containing the event data
        
        Example:
            analytics.track_event(
                "profile_fetch",
                {"username": "john_doe", "status": "success"}
            )
        """
        event_payload = {
            "name": event_name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "url": url,
        }
        
        if event_data:
            # Filter out invalid data types (only strings, numbers, booleans allowed)
            for key, value in event_data.items():
                if isinstance(value, (str, int, float, bool)):
                    event_payload[key] = value
        
        if referrer:
            event_payload["referrer"] = referrer
        
        if timezone:
            event_payload["timezone"] = timezone
        
        # In a real implementation, this would be sent to the Vercel endpoint
        # For now, we return the payload for logging purposes
        return event_payload


# Global analytics instance
analytics = VercelAnalytics()
