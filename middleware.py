"""
FastAPI middleware for analytics and monitoring.

This module provides middleware to track API requests and errors using
Vercel Web Analytics when deployed on Vercel.
"""

import os
import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from analytics import analytics

logger = logging.getLogger(__name__)


class AnalyticsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to track API requests and performance metrics.
    
    This middleware tracks:
    - API endpoint calls
    - Response times
    - HTTP status codes
    - Error rates
    
    Data is sent to Vercel Web Analytics when running on Vercel.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process each request and track analytics.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware/route handler
        
        Returns:
            The HTTP response
        """
        start_time = time.time()
        
        # Get request information
        method = request.method
        path = request.url.path
        
        try:
            response = await call_next(request)
            duration = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Track the API call
            analytics.track_event(
                "api_request",
                {
                    "method": method,
                    "path": path,
                    "status": response.status_code,
                    "duration_ms": int(duration),
                },
                url=path
            )
            
            # Log the request
            logger.info(
                f"{method} {path} - Status: {response.status_code} - Duration: {duration:.2f}ms"
            )
            
            return response
        
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            
            # Track errors
            analytics.track_event(
                "api_error",
                {
                    "method": method,
                    "path": path,
                    "error": str(type(e).__name__),
                    "duration_ms": int(duration),
                },
                url=path
            )
            
            logger.error(
                f"{method} {path} - Error: {str(e)} - Duration: {duration:.2f}ms",
                exc_info=True
            )
            
            raise
