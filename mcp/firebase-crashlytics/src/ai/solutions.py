"""AI-powered solution generator for crash analysis."""

import asyncio
from typing import List, Dict, Any, Optional
import openai
from openai import OpenAI

from ..config import Config
from ..firebase.crashlytics import CrashlyticsTools


class SolutionGenerator:
    """AI-powered crash solution generator."""
    
    def __init__(self, config: Config):
        self.config = config
        self.crashlytics_tools = CrashlyticsTools(config)
        self._client = None
        
        if config.is_openai_configured():
            self._client = OpenAI(api_key=config.openai_api_key)
    
    def _is_available(self) -> bool:
        """Check if AI solution generation is available."""
        return self.config.enable_ai_solutions and self._client is not None
    
    async def generate_solution(
        self,
        app_id: str,
        crash_id: str,
        detail_level: str = "detailed",
        include_code: bool = True,
        platform_context: Optional[str] = None
    ) -> str:
        """Generate AI-powered solution for a specific crash."""
        if not self._is_available():
            return "❌ AI solution generation is not available. Please configure OpenAI API key."
        
        try:
            # Get crash data
            raw_crash_data = await self.crashlytics_tools.get_crash_raw_data(app_id, crash_id)
            
            # Build AI prompt
            prompt = self._build_solution_prompt(
                raw_crash_data, detail_level, include_code, platform_context
            )
            
            # Generate solution using OpenAI
            response = await asyncio.to_thread(
                self._client.chat.completions.create,
                model=self.config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert mobile application developer and crash analysis specialist. Provide accurate, actionable solutions for mobile app crashes with clear explanations and code examples when requested."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.config.openai_max_tokens,
                temperature=self.config.openai_temperature
            )
            
            solution = response.choices[0].message.content.strip()
            
            # Format the response
            result = f"🤖 AI-Generated Solution for Crash {crash_id}\n\n"
            result += f"📱 Platform: {raw_crash_data['device_info']['platform'].title()}\n"
            result += f"🔧 Detail Level: {detail_level.title()}\n\n"
            result += solution
            
            return result
            
        except Exception as e:
            return f"Error generating AI solution: {str(e)}"
    
    async def bulk_solution_analysis(
        self,
        app_id: str,
        crash_ids: List[str],
        priority_order: bool = True
    ) -> str:
        """Generate solutions for multiple related crashes."""
        if not self._is_available():
            return "❌ AI solution generation is not available. Please configure OpenAI API key."
        
        try:
            # Get crash data for all crashes
            crash_data_list = []
            for crash_id in crash_ids:
                crash_data = await self.crashlytics_tools.get_crash_raw_data(app_id, crash_id)
                crash_data_list.append(crash_data)
            
            # Build bulk analysis prompt
            prompt = self._build_bulk_analysis_prompt(crash_data_list, priority_order)
            
            # Generate bulk analysis
            response = await asyncio.to_thread(
                self._client.chat.completions.create,
                model=self.config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert mobile application architect specializing in crash pattern analysis. Analyze multiple crashes to identify common root causes, prioritize fixes, and provide comprehensive solutions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.config.openai_max_tokens,
                temperature=self.config.openai_temperature
            )
            
            analysis = response.choices[0].message.content.strip()
            
            result = f"🔍 Bulk Crash Analysis for {len(crash_ids)} crashes\n\n"
            result += f"📱 App ID: {app_id}\n"
            result += f"🎯 Priority Ordering: {'Enabled' if priority_order else 'Disabled'}\n\n"
            result += analysis
            
            return result
            
        except Exception as e:
            return f"Error generating bulk analysis: {str(e)}"
    
    async def suggest_preventive_measures(
        self,
        app_id: str,
        time_period: str = "30d",
        focus_area: Optional[str] = None
    ) -> str:
        """Suggest preventive measures based on crash patterns."""
        if not self._is_available():
            return "❌ AI solution generation is not available. Please configure OpenAI API key."
        
        try:
            # Get crash trends data
            trends_data = await self.crashlytics_tools.get_crash_trends(app_id, time_period)
            
            # Build preventive measures prompt
            prompt = self._build_preventive_measures_prompt(trends_data, focus_area)
            
            # Generate preventive suggestions
            response = await asyncio.to_thread(
                self._client.chat.completions.create,
                model=self.config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior mobile application quality assurance specialist. Analyze crash patterns and provide comprehensive preventive measures, best practices, and proactive development strategies."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.config.openai_max_tokens,
                temperature=self.config.openai_temperature
            )
            
            suggestions = response.choices[0].message.content.strip()
            
            result = f"🛡️ Preventive Measures for {app_id}\n\n"
            result += f"📊 Analysis Period: {time_period}\n"
            if focus_area:
                result += f"🎯 Focus Area: {focus_area.title()}\n"
            result += "\n"
            result += suggestions
            
            return result
            
        except Exception as e:
            return f"Error generating preventive measures: {str(e)}"
    
    def _build_solution_prompt(
        self,
        crash_data: Dict[str, Any],
        detail_level: str,
        include_code: bool,
        platform_context: Optional[str]
    ) -> str:
        """Build AI prompt for crash solution generation."""
        
        prompt = f"""
Analyze the following mobile app crash and provide a comprehensive solution:

## Crash Information:
- Exception Type: {crash_data['exception_type']}
- Exception Message: {crash_data['exception_message']}
- Platform: {crash_data['device_info']['platform']}
- OS Version: {crash_data['device_info']['os_version']}
- App Version: {crash_data['device_info']['app_version']}
- Device: {crash_data['device_info']['device_model']}

## Stack Trace:
{chr(10).join(crash_data['stacktrace_full'])}

## Context:
- Activity/Screen: {crash_data['context']['activity']}
- User Action: {crash_data['context']['user_action']}
- Memory Pressure: {crash_data['context']['memory_pressure']}
- Network Status: {crash_data['context']['network_status']}

"""
        
        if platform_context:
            prompt += f"## Additional Platform Context:\n{platform_context}\n\n"
        
        prompt += f"""
Please provide a solution with the following detail level: {detail_level}

Include the following in your response:
1. **Root Cause Analysis**: Explain what caused this crash
2. **Immediate Fix**: Direct solution to prevent this specific crash
3. **Code Solution**: {"Provide specific code fixes and examples" if include_code else "Describe the fix without code examples"}
4. **Testing Strategy**: How to test the fix
5. **Prevention**: How to prevent similar crashes in the future

"""
        
        if detail_level == "expert":
            prompt += """
6. **Architecture Recommendations**: Suggest architectural improvements
7. **Performance Considerations**: Impact on app performance
8. **Monitoring**: What to monitor to catch similar issues early
"""
        
        return prompt
    
    def _build_bulk_analysis_prompt(self, crash_data_list: List[Dict[str, Any]], priority_order: bool) -> str:
        """Build prompt for bulk crash analysis."""
        
        prompt = "Analyze the following multiple crashes and provide comprehensive insights:\n\n"
        
        for i, crash_data in enumerate(crash_data_list, 1):
            prompt += f"## Crash {i}:\n"
            prompt += f"- ID: {crash_data['crash_id']}\n"
            prompt += f"- Exception: {crash_data['exception_type']}\n"
            prompt += f"- Message: {crash_data['exception_message']}\n"
            prompt += f"- Context: {crash_data['context']['activity']}\n\n"
        
        prompt += """
Please provide:
1. **Pattern Analysis**: Identify common patterns and root causes
2. **Priority Ranking**: Rank crashes by severity and impact
3. **Grouped Solutions**: Group related crashes and provide solutions
4. **Development Recommendations**: Overall code quality improvements
5. **Action Plan**: Step-by-step fix implementation strategy

"""
        
        if priority_order:
            prompt += "Focus on prioritizing fixes based on user impact and frequency.\n"
        
        return prompt
    
    def _build_preventive_measures_prompt(self, trends_data: str, focus_area: Optional[str]) -> str:
        """Build prompt for preventive measures."""
        
        prompt = f"""
Based on the following crash trends data, provide comprehensive preventive measures:

## Crash Trends:
{trends_data}

"""
        
        if focus_area:
            prompt += f"Focus specifically on: {focus_area}\n\n"
        
        prompt += """
Please provide:
1. **Proactive Development Practices**: Best practices to prevent crashes
2. **Code Quality Measures**: Static analysis, code review guidelines
3. **Testing Strategy**: Comprehensive testing approaches
4. **Monitoring & Alerting**: Early warning systems
5. **Architecture Improvements**: Structural changes to reduce crash likelihood
6. **Development Process**: SDLC improvements for quality assurance
7. **Team Training**: Areas where the development team should focus learning

Format as actionable recommendations with specific implementation steps.
"""
        
        return prompt