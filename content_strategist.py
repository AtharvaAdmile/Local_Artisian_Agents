"""
Content Strategy Recommendation Engine
Provides personalized content strategies for artisans based on their specialization
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import HttpOptions
from typing import Dict, List, Optional
import json
import logging
from datetime import datetime, timedelta
from artisan_ai_agent import ArtisanProfile, CraftType, ContentType, ContentRecommendation, CraftAnalysis

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class ContentStrategist:
    """AI-powered content strategist for artisans"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.client = genai.Client(
            api_key=self.api_key, 
            http_options=HttpOptions(api_version="v1")
        )
        
        # Content strategy knowledge base for Indian artisans
        self.content_strategies = {
            CraftType.POTTERY: {
                "popular_content": [
                    ContentType.PROCESS_VIDEO,
                    ContentType.TIME_LAPSE,
                    ContentType.TUTORIAL,
                    ContentType.BEHIND_SCENES
                ],
                "best_posting_times": ["6-8 PM", "10-12 PM"],
                "trending_hashtags": ["#pottery", "#handmade", "#ceramics", "#indiancrafts", "#earthenware"],
                "seasonal_content": {
                    "festival": "Diwali diyas, festival decorations",
                    "monsoon": "Indoor pottery activities",
                    "summer": "Water cooling vessels, kulhads"
                }
            },
            CraftType.TEXTILES: {
                "popular_content": [
                    ContentType.PROCESS_VIDEO,
                    ContentType.FINISHED_PRODUCT,
                    ContentType.CULTURAL_CONTEXT,
                    ContentType.STORY_TELLING
                ],
                "best_posting_times": ["7-9 PM", "12-2 PM"],
                "trending_hashtags": ["#handloom", "#textiles", "#indianfabric", "#weaving", "#sustainable"],
                "seasonal_content": {
                    "wedding": "Bridal textiles, ceremonial wear",
                    "festival": "Festival wear, traditional patterns",
                    "summer": "Light cotton fabrics, breathable textiles"
                }
            },
            CraftType.JEWELRY: {
                "popular_content": [
                    ContentType.FINISHED_PRODUCT,
                    ContentType.PROCESS_VIDEO,
                    ContentType.CUSTOMER_TESTIMONIAL,
                    ContentType.CULTURAL_CONTEXT
                ],
                "best_posting_times": ["6-8 PM", "11 AM-1 PM"],
                "trending_hashtags": ["#handmadejewelry", "#silverjewelry", "#traditionaljewelry", "#artisanjewelry"],
                "seasonal_content": {
                    "wedding": "Bridal jewelry sets, engagement pieces",
                    "festival": "Temple jewelry, festive accessories",
                    "everyday": "Contemporary daily wear"
                }
            },
            CraftType.WOODWORK: {
                "popular_content": [
                    ContentType.PROCESS_VIDEO,
                    ContentType.TIME_LAPSE,
                    ContentType.TUTORIAL,
                    ContentType.FINISHED_PRODUCT
                ],
                "best_posting_times": ["5-7 PM", "9-11 AM"],
                "trending_hashtags": ["#woodworking", "#furniture", "#handcarved", "#sustainablewood"],
                "seasonal_content": {
                    "monsoon": "Indoor furniture, preservation tips",
                    "festival": "Decorative items, rangoli designs",
                    "summer": "Outdoor furniture, garden items"
                }
            }
        }
    
    def generate_content_strategy(self, artisan: ArtisanProfile, craft_analysis: Optional[CraftAnalysis] = None) -> List[ContentRecommendation]:
        """
        Generate personalized content strategy recommendations
        """
        try:
            # Create strategy prompt
            strategy_prompt = f"""
            Generate content strategy recommendations for an Indian artisan with the following profile:
            
            Name: {artisan.name}
            Location: {artisan.location}
            Specialization: {artisan.specialization.value}
            Experience: {artisan.experience_years} years
            Target Audience: {artisan.target_audience}
            Platforms: {', '.join(artisan.social_media_platforms)}
            
            """
            
            if craft_analysis:
                strategy_prompt += f"""
                Recent craft analysis:
                - Colors: {', '.join(craft_analysis.colors)}
                - Materials: {', '.join(craft_analysis.materials)}
                - Style: {craft_analysis.style}
                - Complexity: {craft_analysis.complexity_level}
                """
            
            strategy_prompt += """
            
            Provide 5 specific content recommendations in JSON format:
            [
                {
                    "content_type": "process_video/finished_product/tutorial/etc",
                    "title_suggestion": "Specific title suggestion",
                    "description": "Detailed description of the content",
                    "best_time_to_post": "optimal posting time",
                    "hashtags": ["relevant", "hashtags"],
                    "target_platforms": ["instagram", "youtube", "facebook"],
                    "priority_score": 0.9,
                    "reasoning": "Why this content is recommended"
                }
            ]
            
            Focus on Indian market, cultural relevance, and platform-specific strategies.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=strategy_prompt
            )
            
            # Parse recommendations
            recommendations = self._parse_content_recommendations(response.text)
            
            # Enhance with local knowledge
            enhanced_recommendations = self._enhance_recommendations(recommendations, artisan, craft_analysis)
            
            logger.info(f"Generated {len(enhanced_recommendations)} content recommendations")
            return enhanced_recommendations
            
        except Exception as e:
            logger.error(f"Error generating content strategy: {e}")
            return self._get_fallback_recommendations(artisan)
    
    def _parse_content_recommendations(self, response_text: str) -> List[Dict]:
        """Parse content recommendations from AI response"""
        try:
            # Find JSON array in response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse recommendations JSON: {e}")
            return []
    
    def _enhance_recommendations(self, recommendations: List[Dict], artisan: ArtisanProfile, craft_analysis: Optional[CraftAnalysis]) -> List[ContentRecommendation]:
        """Enhance AI recommendations with local knowledge"""
        enhanced = []
        craft_strategy = self.content_strategies.get(artisan.specialization, {})
        
        for rec in recommendations:
            try:
                # Convert content type
                content_type = self._parse_content_type(rec.get('content_type', 'process_video'))
                
                # Enhance hashtags with craft-specific ones
                hashtags = rec.get('hashtags', [])
                craft_hashtags = craft_strategy.get('trending_hashtags', [])
                enhanced_hashtags = list(set(hashtags + craft_hashtags))
                
                # Optimize posting time
                best_times = craft_strategy.get('best_posting_times', ['6-8 PM'])
                optimal_time = rec.get('best_time_to_post', best_times[0])
                
                enhanced_rec = ContentRecommendation(
                    content_type=content_type,
                    title_suggestion=rec.get('title_suggestion', 'Share Your Craft Story'),
                    description=rec.get('description', 'Showcase your beautiful handmade craft'),
                    best_time_to_post=optimal_time,
                    hashtags=enhanced_hashtags[:15],  # Limit hashtags
                    target_platforms=rec.get('target_platforms', ['instagram']),
                    priority_score=float(rec.get('priority_score', 0.7)),
                    reasoning=rec.get('reasoning', 'Great content for engagement')
                )
                enhanced.append(enhanced_rec)
                
            except Exception as e:
                logger.warning(f"Error enhancing recommendation: {e}")
                continue
        
        return enhanced
    
    def _parse_content_type(self, content_type_str: str) -> ContentType:
        """Parse content type from string"""
        try:
            return ContentType(content_type_str.lower())
        except ValueError:
            return ContentType.PROCESS_VIDEO
    
    def _get_fallback_recommendations(self, artisan: ArtisanProfile) -> List[ContentRecommendation]:
        """Generate fallback recommendations when AI fails"""
        craft_strategy = self.content_strategies.get(artisan.specialization, self.content_strategies[CraftType.POTTERY])
        
        fallback_recs = [
            ContentRecommendation(
                content_type=ContentType.PROCESS_VIDEO,
                title_suggestion=f"Creating Beautiful {artisan.specialization.value.title()} - Behind the Scenes",
                description="Show your craft creation process to engage viewers",
                best_time_to_post=craft_strategy['best_posting_times'][0],
                hashtags=craft_strategy['trending_hashtags'],
                target_platforms=['instagram', 'youtube'],
                priority_score=0.9,
                reasoning="Process videos are highly engaging for craft content"
            ),
            ContentRecommendation(
                content_type=ContentType.FINISHED_PRODUCT,
                title_suggestion=f"Latest {artisan.specialization.value.title()} Creation",
                description="Showcase your finished masterpiece",
                best_time_to_post=craft_strategy['best_posting_times'][0],
                hashtags=craft_strategy['trending_hashtags'],
                target_platforms=['instagram', 'facebook'],
                priority_score=0.8,
                reasoning="Finished product photos drive sales interest"
            )
        ]
        
        return fallback_recs
    
    def get_seasonal_recommendations(self, artisan: ArtisanProfile, season: str = None) -> List[ContentRecommendation]:
        """Get seasonal content recommendations"""
        if season is None:
            current_month = datetime.now().month
            if current_month in [10, 11]:  # Festival season
                season = "festival"
            elif current_month in [6, 7, 8, 9]:  # Monsoon
                season = "monsoon"
            elif current_month in [3, 4, 5]:  # Summer
                season = "summer"
            else:
                season = "winter"
        
        craft_strategy = self.content_strategies.get(artisan.specialization, {})
        seasonal_content = craft_strategy.get('seasonal_content', {})
        
        if season in seasonal_content:
            return [
                ContentRecommendation(
                    content_type=ContentType.SEASONAL_CONTENT,
                    title_suggestion=f"Perfect {season.title()} {artisan.specialization.value.title()}",
                    description=seasonal_content[season],
                    best_time_to_post="6-8 PM",
                    hashtags=craft_strategy.get('trending_hashtags', []) + [f"#{season}"],
                    target_platforms=['instagram', 'facebook'],
                    priority_score=0.95,
                    reasoning=f"Seasonal relevance increases engagement during {season}"
                )
            ]
        
        return []
    
    def analyze_content_performance(self, content_history: List[Dict]) -> Dict[str, float]:
        """Analyze past content performance to improve recommendations"""
        # This would integrate with social media APIs in a real implementation
        performance_metrics = {
            "engagement_rate": 0.0,
            "reach": 0.0,
            "best_performing_type": "process_video",
            "optimal_posting_time": "6-8 PM"
        }
        
        # Placeholder for performance analysis logic
        return performance_metrics
    
    def generate_content_calendar(self, artisan: ArtisanProfile, days: int = 30) -> Dict[str, List[ContentRecommendation]]:
        """Generate a content calendar for specified days"""
        calendar = {}
        base_recommendations = self.generate_content_strategy(artisan)
        
        current_date = datetime.now()
        for i in range(days):
            date = current_date + timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            # Assign 1-2 recommendations per day, cycling through types
            daily_content = []
            if i % 2 == 0 and base_recommendations:  # Every other day
                rec_index = i % len(base_recommendations)
                daily_content.append(base_recommendations[rec_index])
            
            calendar[date_str] = daily_content
        
        return calendar

if __name__ == "__main__":
    # Test the content strategist
    strategist = ContentStrategist()
    print("📋 Content Strategist initialized successfully")