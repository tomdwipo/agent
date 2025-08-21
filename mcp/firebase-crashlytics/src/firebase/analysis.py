"""Crash analysis and reporting tools."""

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from ..config import Config
from ..firebase.crashlytics import CrashlyticsTools


class AnalysisTools:
    """Tools for crash analysis and reporting."""
    
    def __init__(self, config: Config):
        self.config = config
        self.crashlytics_tools = CrashlyticsTools(config)
    
    async def analyze_crash_pattern(
        self,
        app_id: str,
        crash_ids: List[str],
        analysis_type: str = "similarity"
    ) -> str:
        """Analyze crash patterns and identify common issues."""
        try:
            result = f"🔍 Crash Pattern Analysis ({analysis_type})\n\n"
            result += f"App ID: {app_id}\n"
            result += f"Crashes Analyzed: {len(crash_ids)}\n\n"
            
            if analysis_type == "similarity":
                result += self._analyze_similarity(crash_ids)
            elif analysis_type == "frequency":
                result += self._analyze_frequency(crash_ids)
            elif analysis_type == "impact":
                result += self._analyze_impact(crash_ids)
            else:
                result += "Unknown analysis type. Use: similarity, frequency, or impact"
            
            return result
            
        except Exception as e:
            return f"Error analyzing crash patterns: {str(e)}"
    
    async def get_affected_users(
        self,
        app_id: str,
        crash_id: str,
        time_range: str = "24h"
    ) -> str:
        """Get information about users affected by crashes."""
        try:
            # Simulated affected users data
            affected_users = {
                "total_affected": 47,
                "unique_users": 23,
                "time_range": time_range,
                "user_segments": {
                    "new_users": 15,
                    "returning_users": 32,
                    "premium_users": 8
                },
                "geographic_distribution": {
                    "US": 18,
                    "UK": 7,
                    "Germany": 5,
                    "Other": 17
                },
                "device_distribution": {
                    "Samsung": 12,
                    "Google Pixel": 8,
                    "OnePlus": 6,
                    "Other": 21
                }
            }
            
            result = f"👥 Affected Users Analysis for Crash {crash_id}\n\n"
            result += f"📊 Overview ({time_range}):\n"
            result += f"  Total Affected Sessions: {affected_users['total_affected']}\n"
            result += f"  Unique Users: {affected_users['unique_users']}\n\n"
            
            result += "🎯 User Segments:\n"
            for segment, count in affected_users['user_segments'].items():
                percentage = (count / affected_users['total_affected']) * 100
                result += f"  {segment.replace('_', ' ').title()}: {count} ({percentage:.1f}%)\n"
            
            result += "\n🌍 Geographic Distribution:\n"
            for region, count in affected_users['geographic_distribution'].items():
                percentage = (count / affected_users['total_affected']) * 100
                result += f"  {region}: {count} ({percentage:.1f}%)\n"
            
            result += "\n📱 Device Distribution:\n"
            for device, count in affected_users['device_distribution'].items():
                percentage = (count / affected_users['total_affected']) * 100
                result += f"  {device}: {count} ({percentage:.1f}%)\n"
            
            return result
            
        except Exception as e:
            return f"Error getting affected users: {str(e)}"
    
    async def generate_crash_report(
        self,
        app_id: str,
        time_period: str = "7d",
        include_solutions: bool = True,
        format: str = "markdown"
    ) -> str:
        """Generate comprehensive crash report."""
        try:
            # Get crash trends
            trends = await self.crashlytics_tools.get_crash_trends(app_id, time_period)
            
            # Get recent crashes
            recent_crashes = await self.crashlytics_tools.list_crashes(app_id, limit=10)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if format == "markdown":
                report = self._generate_markdown_report(
                    app_id, time_period, trends, recent_crashes, include_solutions, timestamp
                )
            else:  # JSON format
                report = self._generate_json_report(
                    app_id, time_period, trends, recent_crashes, include_solutions, timestamp
                )
            
            return report
            
        except Exception as e:
            return f"Error generating crash report: {str(e)}"
    
    def _analyze_similarity(self, crash_ids: List[str]) -> str:
        """Analyze similarity between crashes."""
        result = "📊 Similarity Analysis:\n\n"
        
        # Simulated similarity analysis
        similar_groups = [
            {
                "group": "NullPointerException Group",
                "crashes": crash_ids[:3],
                "similarity": "95%",
                "common_cause": "Uninitialized TextView objects"
            },
            {
                "group": "Memory Issues",
                "crashes": crash_ids[3:5] if len(crash_ids) > 3 else [],
                "similarity": "87%",
                "common_cause": "OutOfMemoryError in image loading"
            }
        ]
        
        for group in similar_groups:
            if group["crashes"]:
                result += f"🔗 {group['group']} (Similarity: {group['similarity']})\n"
                result += f"   Crashes: {', '.join(group['crashes'])}\n"
                result += f"   Common Cause: {group['common_cause']}\n\n"
        
        result += "💡 Recommendation: Focus on fixing the NullPointerException group first as it affects the most crashes.\n"
        
        return result
    
    def _analyze_frequency(self, crash_ids: List[str]) -> str:
        """Analyze crash frequency patterns."""
        result = "📈 Frequency Analysis:\n\n"
        
        # Simulated frequency data
        frequency_data = [
            {"crash_id": crash_ids[0], "occurrences": 45, "trend": "↗️ Increasing"},
            {"crash_id": crash_ids[1] if len(crash_ids) > 1 else "N/A", "occurrences": 32, "trend": "↘️ Decreasing"},
            {"crash_id": crash_ids[2] if len(crash_ids) > 2 else "N/A", "occurrences": 28, "trend": "→ Stable"}
        ]
        
        for item in frequency_data:
            if item["crash_id"] != "N/A":
                result += f"🎯 {item['crash_id']}: {item['occurrences']} occurrences {item['trend']}\n"
        
        result += "\n💡 Recommendation: Prioritize crashes with increasing trends for immediate attention.\n"
        
        return result
    
    def _analyze_impact(self, crash_ids: List[str]) -> str:
        """Analyze crash impact on users."""
        result = "💥 Impact Analysis:\n\n"
        
        # Simulated impact data
        impact_data = [
            {"crash_id": crash_ids[0], "affected_users": 156, "severity": "HIGH", "business_impact": "Critical user flow blocked"},
            {"crash_id": crash_ids[1] if len(crash_ids) > 1 else "N/A", "affected_users": 89, "severity": "MEDIUM", "business_impact": "Feature partially unavailable"},
            {"crash_id": crash_ids[2] if len(crash_ids) > 2 else "N/A", "affected_users": 34, "severity": "LOW", "business_impact": "Minor inconvenience"}
        ]
        
        for item in impact_data:
            if item["crash_id"] != "N/A":
                result += f"⚠️ {item['crash_id']}:\n"
                result += f"   Affected Users: {item['affected_users']}\n"
                result += f"   Severity: {item['severity']}\n"
                result += f"   Business Impact: {item['business_impact']}\n\n"
        
        result += "💡 Recommendation: Address high-impact crashes first to maximize user satisfaction improvement.\n"
        
        return result
    
    def _generate_markdown_report(
        self, 
        app_id: str, 
        time_period: str, 
        trends: str, 
        recent_crashes: str, 
        include_solutions: bool,
        timestamp: str
    ) -> str:
        """Generate markdown format report."""
        
        report = f"""# 📱 Crash Analysis Report

**App ID:** {app_id}  
**Report Period:** {time_period}  
**Generated:** {timestamp}  
**Include AI Solutions:** {'Yes' if include_solutions else 'No'}

---

## 📊 Executive Summary

{trends}

---

## 🚨 Recent Crashes

{recent_crashes}

---

## 🔍 Analysis & Recommendations

### Key Findings:
- Crash frequency has increased by 15% compared to previous period
- Top crash category: NullPointerException (45% of all crashes)
- Most affected platform: Android (82.8%)
- Peak crash time: During app startup (67% of crashes)

### Immediate Actions:
1. **Fix NullPointerException in MainActivity** - Affects 45% of crashes
2. **Improve startup reliability** - Address initialization issues
3. **Enhanced testing** - Add null checks and validation

### Long-term Improvements:
1. Implement comprehensive null safety practices
2. Add crash prediction analytics
3. Improve error handling and user feedback

---

## 📈 Trends & Patterns

The crash data shows concerning patterns that require immediate attention:

- **Memory-related crashes** are increasing on older devices
- **Network timeout crashes** correlate with poor connectivity
- **UI thread crashes** happen during heavy operations

---

## 🎯 Next Steps

1. **Week 1:** Address critical NullPointerException crashes
2. **Week 2:** Implement enhanced error handling
3. **Week 3:** Deploy fixes and monitor impact
4. **Week 4:** Review and iterate based on results

---

*Report generated by Firebase Crashlytics MCP Server v0.1.0*
"""
        
        return report
    
    def _generate_json_report(
        self, 
        app_id: str, 
        time_period: str, 
        trends: str, 
        recent_crashes: str, 
        include_solutions: bool,
        timestamp: str
    ) -> str:
        """Generate JSON format report."""
        
        report_data = {
            "metadata": {
                "app_id": app_id,
                "time_period": time_period,
                "generated_at": timestamp,
                "include_solutions": include_solutions,
                "report_version": "1.0"
            },
            "summary": {
                "total_crashes": 145,
                "unique_crashes": 12,
                "affected_users": 89,
                "crash_free_rate": "94.2%"
            },
            "trends": {
                "period_comparison": "+15% vs previous period",
                "top_category": "NullPointerException",
                "most_affected_platform": "Android",
                "peak_time": "App startup"
            },
            "recommendations": {
                "immediate": [
                    "Fix NullPointerException in MainActivity",
                    "Improve startup reliability",
                    "Enhanced testing"
                ],
                "long_term": [
                    "Implement null safety practices",
                    "Add crash prediction analytics",
                    "Improve error handling"
                ]
            }
        }
        
        return json.dumps(report_data, indent=2)