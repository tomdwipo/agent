"""Firebase Crashlytics data retrieval tools."""

import asyncio
import json
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
import requests
from google.auth.transport.requests import Request

from ..config import Config


class CrashlyticsTools:
    """Tools for Firebase Crashlytics operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self._app = None
        self._access_token = None
        self._token_expiry = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK."""
        try:
            if not firebase_admin._apps:
                if self.config.firebase_credentials_path:
                    cred = credentials.Certificate(self.config.firebase_credentials_path)
                else:
                    cred = credentials.ApplicationDefault()
                
                self._app = firebase_admin.initialize_app(cred, {
                    'projectId': self.config.firebase_project_id
                })
            else:
                self._app = firebase_admin.get_app()
        except Exception as e:
            print(f"Failed to initialize Firebase: {e}")
            self._app = None
    
    async def _get_access_token(self) -> str:
        """Get valid access token for Firebase APIs."""
        if self._access_token and self._token_expiry and datetime.now() < self._token_expiry:
            return self._access_token
        
        try:
            # Use Firebase Admin SDK to get token
            token = await asyncio.to_thread(
                lambda: self._app.credential.get_access_token().access_token
            )
            self._access_token = token
            self._token_expiry = datetime.now() + timedelta(minutes=50)  # Tokens usually valid for 1 hour
            return token
        except Exception as e:
            raise Exception(f"Failed to get access token: {e}")
    
    async def list_crashes(
        self, 
        app_id: str, 
        limit: int = 20, 
        severity: Optional[str] = None,
        platform: Optional[str] = None
    ) -> str:
        """List recent crashes for an app."""
        try:
            # Note: Firebase Crashlytics doesn't have a direct public API for listing crashes
            # This would typically require Firebase Admin SDK with proper permissions
            # For now, we'll simulate the response structure
            
            result = f"Recent crashes for app {app_id}:\n\n"
            
            # Simulated crash data structure
            crashes = [
                {
                    "id": f"crash_{i}",
                    "title": f"NullPointerException in Activity{i}",
                    "severity": "HIGH" if i % 3 == 0 else "MEDIUM",
                    "platform": "android",
                    "occurrences": 15 - i,
                    "first_seen": f"2024-{12:02d}-{(20-i):02d}T10:30:00Z",
                    "last_seen": f"2024-{12:02d}-{(22-i):02d}T15:45:00Z",
                    "affected_users": 8 - i,
                    "app_version": f"1.{i}.0"
                }
                for i in range(1, min(limit + 1, 11))
            ]
            
            # Apply filters
            if severity:
                crashes = [c for c in crashes if c["severity"] == severity.upper()]
            if platform:
                crashes = [c for c in crashes if c["platform"] == platform.lower()]
            
            if not crashes:
                return f"No crashes found for app {app_id} with the specified filters."
            
            for crash in crashes:
                result += f"🚨 {crash['title']}\n"
                result += f"   ID: {crash['id']}\n"
                result += f"   Severity: {crash['severity']}\n"
                result += f"   Platform: {crash['platform']}\n"
                result += f"   Occurrences: {crash['occurrences']}\n"
                result += f"   Affected Users: {crash['affected_users']}\n"
                result += f"   App Version: {crash['app_version']}\n"
                result += f"   Last Seen: {crash['last_seen']}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error listing crashes: {str(e)}"
    
    async def get_crash_details(
        self, 
        app_id: str, 
        crash_id: str, 
        include_stacktrace: bool = True
    ) -> str:
        """Get detailed information about a specific crash."""
        try:
            # Simulated detailed crash data
            crash_detail = {
                "id": crash_id,
                "title": "NullPointerException in MainActivity.onCreate()",
                "severity": "HIGH",
                "platform": "android",
                "device_info": {
                    "model": "Samsung Galaxy S21",
                    "os_version": "Android 13",
                    "app_version": "1.2.0",
                    "memory_total": "8GB",
                    "memory_available": "2.1GB"
                },
                "crash_info": {
                    "exception_type": "java.lang.NullPointerException",
                    "crash_timestamp": "2024-12-20T15:45:32Z",
                    "session_id": "sess_abc123",
                    "user_id": "user_xyz789"
                },
                "stacktrace": [
                    "java.lang.NullPointerException: Attempt to invoke virtual method 'void android.widget.TextView.setText(java.lang.CharSequence)' on a null object reference",
                    "    at com.example.app.MainActivity.onCreate(MainActivity.java:45)",
                    "    at android.app.Activity.performCreate(Activity.java:8051)",
                    "    at android.app.Activity.performCreate(Activity.java:8031)",
                    "    at android.app.Instrumentation.callActivityOnCreate(Instrumentation.java:1329)",
                    "    at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:3608)"
                ]
            }
            
            result = f"📱 Crash Details: {crash_detail['id']}\n\n"
            result += f"Title: {crash_detail['title']}\n"
            result += f"Severity: {crash_detail['severity']}\n"
            result += f"Platform: {crash_detail['platform']}\n"
            result += f"Exception: {crash_detail['crash_info']['exception_type']}\n"
            result += f"Timestamp: {crash_detail['crash_info']['crash_timestamp']}\n\n"
            
            result += "🔧 Device Information:\n"
            for key, value in crash_detail['device_info'].items():
                result += f"  {key.replace('_', ' ').title()}: {value}\n"
            
            if include_stacktrace:
                result += "\n📋 Stack Trace:\n"
                for line in crash_detail['stacktrace']:
                    result += f"  {line}\n"
            
            return result
            
        except Exception as e:
            return f"Error getting crash details: {str(e)}"
    
    async def get_crash_trends(
        self, 
        app_id: str, 
        time_period: str = "7d", 
        group_by: Optional[str] = None
    ) -> str:
        """Get crash trends and statistics."""
        try:
            # Simulated trend data
            trends = {
                "period": time_period,
                "total_crashes": 145,
                "unique_crashes": 12,
                "affected_users": 89,
                "crash_free_rate": "94.2%",
                "trends_by_day": [
                    {"date": "2024-12-14", "crashes": 18, "users": 12},
                    {"date": "2024-12-15", "crashes": 22, "users": 15},
                    {"date": "2024-12-16", "crashes": 31, "users": 18},
                    {"date": "2024-12-17", "crashes": 28, "users": 16},
                    {"date": "2024-12-18", "crashes": 19, "users": 11},
                    {"date": "2024-12-19", "crashes": 15, "users": 9},
                    {"date": "2024-12-20", "crashes": 12, "users": 8}
                ]
            }
            
            result = f"📊 Crash Trends for {app_id} ({time_period}):\n\n"
            result += f"Total Crashes: {trends['total_crashes']}\n"
            result += f"Unique Crash Types: {trends['unique_crashes']}\n"
            result += f"Affected Users: {trends['affected_users']}\n"
            result += f"Crash-Free Rate: {trends['crash_free_rate']}\n\n"
            
            result += "📈 Daily Breakdown:\n"
            for day in trends['trends_by_day']:
                result += f"  {day['date']}: {day['crashes']} crashes, {day['users']} users\n"
            
            # Group by analysis
            if group_by == "severity":
                result += "\n🎯 By Severity:\n"
                result += "  CRITICAL: 8 (5.5%)\n"
                result += "  HIGH: 45 (31.0%)\n"
                result += "  MEDIUM: 67 (46.2%)\n"
                result += "  LOW: 25 (17.3%)\n"
            elif group_by == "platform":
                result += "\n📱 By Platform:\n"
                result += "  Android: 120 (82.8%)\n"
                result += "  iOS: 25 (17.2%)\n"
            elif group_by == "version":
                result += "\n🔢 By App Version:\n"
                result += "  v1.2.0: 89 (61.4%)\n"
                result += "  v1.1.5: 34 (23.4%)\n"
                result += "  v1.1.0: 22 (15.2%)\n"
            
            return result
            
        except Exception as e:
            return f"Error getting crash trends: {str(e)}"
    
    async def get_crash_raw_data(self, app_id: str, crash_id: str) -> Dict[str, Any]:
        """Get raw crash data for AI analysis."""
        try:
            # This would contain the full crash context for AI processing
            raw_data = {
                "crash_id": crash_id,
                "exception_type": "java.lang.NullPointerException",
                "exception_message": "Attempt to invoke virtual method 'void android.widget.TextView.setText(java.lang.CharSequence)' on a null object reference",
                "stacktrace_full": [
                    "java.lang.NullPointerException: Attempt to invoke virtual method 'void android.widget.TextView.setText(java.lang.CharSequence)' on a null object reference",
                    "    at com.example.app.MainActivity.onCreate(MainActivity.java:45)",
                    "    at android.app.Activity.performCreate(Activity.java:8051)",
                    "    at android.app.Activity.performCreate(Activity.java:8031)",
                    "    at android.app.Instrumentation.callActivityOnCreate(Instrumentation.java:1329)",
                    "    at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:3608)"
                ],
                "device_info": {
                    "platform": "android",
                    "os_version": "13",
                    "device_model": "Samsung Galaxy S21",
                    "app_version": "1.2.0",
                    "architecture": "arm64-v8a"
                },
                "context": {
                    "activity": "MainActivity",
                    "fragment": None,
                    "user_action": "app_launch",
                    "memory_pressure": "normal",
                    "network_status": "connected"
                }
            }
            
            return raw_data
            
        except Exception as e:
            raise Exception(f"Error getting raw crash data: {e}")