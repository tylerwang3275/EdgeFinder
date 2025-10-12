"""
Time utilities for EdgeFinder.
"""

from datetime import datetime, timedelta
from typing import Tuple
import pytz


def get_time_window(hours: int) -> Tuple[datetime, datetime]:
    """
    Get time window for data fetching.
    
    Args:
        hours: Hours to look ahead
        
    Returns:
        Tuple of (start_time, end_time) in UTC
    """
    now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    start_time = now
    end_time = now + timedelta(hours=hours)
    
    return start_time, end_time


def to_local_time(utc_time: datetime, timezone: str = "America/Los_Angeles") -> datetime:
    """
    Convert UTC time to local timezone.
    
    Args:
        utc_time: UTC datetime
        timezone: Target timezone string
        
    Returns:
        Local datetime
    """
    if utc_time.tzinfo is None:
        utc_time = utc_time.replace(tzinfo=pytz.UTC)
    
    local_tz = pytz.timezone(timezone)
    return utc_time.astimezone(local_tz)


def format_time_for_display(dt: datetime, timezone: str = "America/Los_Angeles") -> str:
    """
    Format datetime for display in reports.
    
    Args:
        dt: Datetime to format
        timezone: Target timezone
        
    Returns:
        Formatted time string
    """
    local_time = to_local_time(dt, timezone)
    return local_time.strftime("%Y-%m-%d %I:%M %p %Z")


def is_within_timeframe(dt: datetime, start: datetime, end: datetime) -> bool:
    """
    Check if datetime is within timeframe.
    
    Args:
        dt: Datetime to check
        start: Start of timeframe
        end: End of timeframe
        
    Returns:
        True if within timeframe
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.UTC)
    if start.tzinfo is None:
        start = start.replace(tzinfo=pytz.UTC)
    if end.tzinfo is None:
        end = end.replace(tzinfo=pytz.UTC)
    
    return start <= dt <= end
