"""
Specialized Craft Recommendation System
Provides targeted recommendations based on specific craft specializations
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import HttpOptions
from typing import Dict, List, Optional, Tuple
import json
import logging
from datetime import datetime, timedelta
from artisan_ai_agent import ArtisanProfile, CraftType, ContentType, ContentRecommendation, CraftAnalysis

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class SpecializedRecommendationEngine:
    """Provides specialized recommendations based on craft type and expertise"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.client = genai.Client(
            api_key=self.api_key, 
            http_options=HttpOptions(api_version="v1")
        )
        
        # Specialized knowledge base for different craft types
        self.craft_specializations = {
            CraftType.POTTERY: {
                "techniques": ["wheel throwing", "hand building", "glazing", "firing", "slip casting"],
                "tools": ["pottery wheel", "kiln", "glazes", "clay tools", "brushes"],
                "markets": ["home decor", "functional pottery", "art collectors", "restaurants"],
                "skill_levels": {
                    "beginner": ["basic pinch pots", "coil building", "simple glazing"],
                    "intermediate": ["wheel throwing", "trimming", "decorative techniques"],
                    "advanced": ["complex forms", "specialized glazes", "kiln management"],
                    "expert": ["custom glazes", "artistic installations", "teaching others"]
                },
                "content_focus": ["process videos", "technique tutorials", "firing process", "glazing tips"]
            },
            CraftType.TEXTILES: {
                "techniques": ["weaving", "dyeing", "block printing", "embroidery", "spinning"],
                "tools": ["loom", "natural dyes", "printing blocks", "needles", "spinning wheel"],
                "markets": ["fashion", "home textiles", "cultural wear", "sustainable fashion"],
                "skill_levels": {
                    "beginner": ["basic weaving", "simple patterns", "natural dyeing"],
                    "intermediate": ["complex patterns", "color combinations", "finishing techniques"],
                    "advanced": ["intricate designs", "traditional patterns", "fabric innovation"],
                    "expert": ["master weaver", "pattern creation", "heritage preservation"]
                },
                "content_focus": ["weaving process", "dyeing techniques", "pattern stories", "cultural significance"]
            },
            CraftType.JEWELRY: {
                "techniques": ["wire wrapping", "soldering", "stone setting", "engraving", "polishing"],
                "tools": ["pliers", "soldering torch", "files", "polishing compounds", "stamps"],
                "markets": ["fashion jewelry", "bridal jewelry", "everyday wear", "collectors"],
                "skill_levels": {
                    "beginner": ["basic wire work", "simple designs", "finishing"],
                    "intermediate": ["soldering", "stone setting", "complex designs"],
                    "advanced": ["intricate patterns", "custom settings", "repair work"],
                    "expert": ["master craftsman", "teaching", "innovative designs"]
                },
                "content_focus": ["making process", "design inspiration", "finishing techniques", "styling tips"]
            },
            CraftType.WOODWORK: {
                "techniques": ["carving", "joinery", "finishing", "turning", "inlay work"],
                "tools": ["chisels", "saws", "planes", "sanders", "lathe"],
                "markets": ["furniture", "decorative items", "toys", "architectural elements"],
                "skill_levels": {
                    "beginner": ["basic carving", "simple projects", "tool handling"],
                    "intermediate": ["joinery", "furniture making", "finishing techniques"],
                    "advanced": ["complex projects", "custom designs", "restoration"],
                    "expert": ["master craftsman", "artistic pieces", "teaching"]
                },
                "content_focus": ["carving process", "wood selection", "finishing techniques", "project tutorials"]
            }
        }
    
    def get_specialized_recommendations(self, artisan: ArtisanProfile, craft_analysis: Optional[CraftAnalysis] = None) -> List[ContentRecommendation]:
        """Generate recommendations specific to artisan's craft specialization"""
        try:
            craft_info = self.craft_specializations.get(artisan.specialization, {})
            skill_level = self._determine_skill_level(artisan.experience_years)
            
            # Create specialized prompt
            prompt = f"""
            Generate specialized content recommendations for a {artisan.specialization.value} artisan:
            
            Artisan Details:
            - Name: {artisan.name}
            - Experience: {artisan.experience_years} years ({skill_level} level)
            - Location: {artisan.location}
            - Style: {artisan.signature_style}
            - Target Audience: {artisan.target_audience}
            
            Craft Specialization:
            - Techniques: {', '.join(craft_info.get('techniques', []))}
            - Tools: {', '.join(craft_info.get('tools', []))}
            - Markets: {', '.join(craft_info.get('markets', []))}
            
            """
            
            if craft_analysis:
                prompt += f"""
                Recent Work Analysis:
                - Materials: {', '.join(craft_analysis.materials)}
                - Style: {craft_analysis.style}
                - Complexity: {craft_analysis.complexity_level}
                - Colors: {', '.join(craft_analysis.colors)}
                """
            
            prompt += f"""
            
            Current Skill Level Focus: {', '.join(craft_info.get('skill_levels', {}).get(skill_level, []))}
            
            Provide 6 specialized content recommendations in JSON format:
            [
                {{
                    "content_type": "tutorial/process_video/behind_scenes/etc",
                    "title_suggestion": "Specific title for {artisan.specialization.value}",
                    "description": "Detailed description focusing on {artisan.specialization.value} specifics",
                    "skill_focus": "specific technique or skill to highlight",
                    "target_platforms": ["platform1", "platform2"],
                    "hashtags": ["craft-specific", "hashtags"],
                    "priority_score": 0.9,
                    "reasoning": "Why this is perfect for a {skill_level} {artisan.specialization.value} artisan",
                    "engagement_hooks": ["specific engagement strategies"]
                }}
            ]
            
            Focus on {skill_level}-level content that showcases {artisan.specialization.value} expertise.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt
            )
            
            # Parse and enhance recommendations
            recommendations = self._parse_specialized_recommendations(response.text, artisan, craft_info, skill_level)
            
            logger.info(f"Generated {len(recommendations)} specialized recommendations for {artisan.specialization.value}")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating specialized recommendations: {e}")
            return self._get_craft_specific_fallbacks(artisan)
    
    def _determine_skill_level(self, experience_years: int) -> str:
        """Determine skill level based on experience"""
        if experience_years <= 2:
            return "beginner"
        elif experience_years <= 7:
            return "intermediate"
        elif experience_years <= 15:
            return "advanced"
        else:
            return "expert"
    
    def _parse_specialized_recommendations(self, response_text: str, artisan: ArtisanProfile, craft_info: Dict, skill_level: str) -> List[ContentRecommendation]:
        """Parse specialized recommendations from AI response"""
        try:
            # Find JSON array in response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            json_str = response_text[start_idx:end_idx]
            recommendations_data = json.loads(json_str)
            
            recommendations = []
            for rec_data in recommendations_data:
                try:
                    # Parse content type
                    content_type_str = rec_data.get('content_type', 'process_video')
                    content_type = self._parse_content_type(content_type_str)
                    
                    # Enhance with craft-specific hashtags
                    hashtags = rec_data.get('hashtags', [])
                    craft_hashtags = self._get_craft_hashtags(artisan.specialization, skill_level)
                    enhanced_hashtags = list(set(hashtags + craft_hashtags))
                    
                    rec = ContentRecommendation(
                        content_type=content_type,
                        title_suggestion=rec_data.get('title_suggestion', f'Master {artisan.specialization.value} Techniques'),
                        description=rec_data.get('description', f'Showcase your {artisan.specialization.value} skills'),
                        best_time_to_post=self._get_optimal_posting_time(artisan.specialization),
                        hashtags=enhanced_hashtags[:15],
                        target_platforms=rec_data.get('target_platforms', ['instagram', 'youtube']),
                        priority_score=float(rec_data.get('priority_score', 0.8)),
                        reasoning=rec_data.get('reasoning', f'Perfect for {skill_level} {artisan.specialization.value} artisan')
                    )
                    recommendations.append(rec)
                    
                except Exception as e:
                    logger.warning(f"Error parsing recommendation: {e}")
                    continue
            
            return recommendations
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse specialized recommendations JSON: {e}")
            return self._get_craft_specific_fallbacks(artisan)
    
    def _parse_content_type(self, content_type_str: str) -> ContentType:
        """Parse content type from string"""
        try:
            return ContentType(content_type_str.lower())
        except ValueError:
            return ContentType.PROCESS_VIDEO
    
    def _get_craft_hashtags(self, craft_type: CraftType, skill_level: str) -> List[str]:
        """Get craft-specific hashtags"""
        base_hashtags = [f"#{craft_type.value}", "#handmade", "#artisan", "#indiancrafts"]
        
        craft_specific = {
            CraftType.POTTERY: ["#ceramics", "#pottery", "#clay", "#kiln", "#glaze"],
            CraftType.TEXTILES: ["#weaving", "#handloom", "#naturalDyes", "#textiles", "#sustainable"],
            CraftType.JEWELRY: ["#handmadejewelry", "#artisanjewelry", "#silverjewelry", "#traditional"],
            CraftType.WOODWORK: ["#woodworking", "#carving", "#handcarved", "#furniture", "#woodcraft"]
        }
        
        skill_hashtags = {
            "beginner": ["#learning", "#newartisan", "#practice"],
            "intermediate": ["#skilled", "#crafting", "#technique"],
            "advanced": ["#expert", "#masterpiece", "#advanced"],
            "expert": ["#master", "#heritage", "#teaching", "#traditional"]
        }
        
        return base_hashtags + craft_specific.get(craft_type, []) + skill_hashtags.get(skill_level, [])
    
    def _get_optimal_posting_time(self, craft_type: CraftType) -> str:
        """Get optimal posting time for craft type"""
        optimal_times = {
            CraftType.POTTERY: "6-8 PM",
            CraftType.TEXTILES: "7-9 PM", 
            CraftType.JEWELRY: "11 AM-1 PM",
            CraftType.WOODWORK: "5-7 PM"
        }
        return optimal_times.get(craft_type, "6-8 PM")
    
    def _get_craft_specific_fallbacks(self, artisan: ArtisanProfile) -> List[ContentRecommendation]:
        """Generate fallback recommendations for specific craft"""
        craft_info = self.craft_specializations.get(artisan.specialization, {})
        skill_level = self._determine_skill_level(artisan.experience_years)
        
        fallbacks = [
            ContentRecommendation(
                content_type=ContentType.PROCESS_VIDEO,
                title_suggestion=f"Master {artisan.specialization.value.title()} Techniques - {skill_level.title()} Level",
                description=f"Show your {artisan.specialization.value} creation process step by step",
                best_time_to_post=self._get_optimal_posting_time(artisan.specialization),
                hashtags=self._get_craft_hashtags(artisan.specialization, skill_level),
                target_platforms=['instagram', 'youtube'],
                priority_score=0.9,
                reasoning=f"Process videos are highly engaging for {artisan.specialization.value} content"
            ),
            ContentRecommendation(
                content_type=ContentType.TUTORIAL,
                title_suggestion=f"{artisan.specialization.value.title()} Tutorial for Beginners",
                description=f"Share your knowledge and teach {artisan.specialization.value} techniques",
                best_time_to_post=self._get_optimal_posting_time(artisan.specialization),
                hashtags=self._get_craft_hashtags(artisan.specialization, skill_level),
                target_platforms=['youtube', 'instagram'],
                priority_score=0.85,
                reasoning=f"Educational content builds authority in {artisan.specialization.value}"
            )
        ]
        
        return fallbacks
    
    def get_technique_recommendations(self, artisan: ArtisanProfile, technique: str) -> List[ContentRecommendation]:
        """Get recommendations for specific technique content"""
        craft_info = self.craft_specializations.get(artisan.specialization, {})
        
        if technique not in craft_info.get('techniques', []):
            logger.warning(f"Technique '{technique}' not found for {artisan.specialization.value}")
            return []
        
        return [
            ContentRecommendation(
                content_type=ContentType.TUTORIAL,
                title_suggestion=f"Mastering {technique.title()} in {artisan.specialization.value.title()}",
                description=f"Step-by-step guide to {technique} technique",
                best_time_to_post=self._get_optimal_posting_time(artisan.specialization),
                hashtags=self._get_craft_hashtags(artisan.specialization, "advanced") + [f"#{technique.replace(' ', '')}"],
                target_platforms=['youtube', 'instagram'],
                priority_score=0.95,
                reasoning=f"Technique-specific content showcases expertise in {technique}"
            )
        ]
    
    def get_market_specific_recommendations(self, artisan: ArtisanProfile, target_market: str) -> List[ContentRecommendation]:
        """Get recommendations for specific target market"""
        craft_info = self.craft_specializations.get(artisan.specialization, {})
        markets = craft_info.get('markets', [])
        
        if target_market not in markets:
            logger.warning(f"Market '{target_market}' not typical for {artisan.specialization.value}")
        
        market_strategies = {
            "home decor": {
                "content_focus": "lifestyle integration, room styling, functional beauty",
                "platforms": ["pinterest", "instagram", "facebook"],
                "hashtags": ["#homedecor", "#interiordesign", "#handmadehome"]
            },
            "fashion": {
                "content_focus": "styling tips, outfit coordination, trend integration",
                "platforms": ["instagram", "pinterest", "tiktok"],
                "hashtags": ["#fashion", "#style", "#handmadefashion"]
            },
            "art collectors": {
                "content_focus": "artistic process, uniqueness, investment value",
                "platforms": ["instagram", "youtube", "facebook"],
                "hashtags": ["#artcollection", "#investment", "#uniqueart"]
            }
        }
        
        strategy = market_strategies.get(target_market, market_strategies["home decor"])
        
        return [
            ContentRecommendation(
                content_type=ContentType.FINISHED_PRODUCT,
                title_suggestion=f"{artisan.specialization.value.title()} for {target_market.title()} Enthusiasts",
                description=f"Showcase how your {artisan.specialization.value} fits perfectly in {target_market}",
                best_time_to_post=self._get_optimal_posting_time(artisan.specialization),
                hashtags=self._get_craft_hashtags(artisan.specialization, "intermediate") + strategy["hashtags"],
                target_platforms=strategy["platforms"],
                priority_score=0.9,
                reasoning=f"Market-specific content resonates with {target_market} audience"
            )
        ]
    
    def get_seasonal_craft_recommendations(self, artisan: ArtisanProfile, season: str = None) -> List[ContentRecommendation]:
        """Get seasonal recommendations for specific craft"""
        if season is None:
            current_month = datetime.now().month
            if current_month in [10, 11]:
                season = "festival"
            elif current_month in [6, 7, 8, 9]:
                season = "monsoon"
            elif current_month in [3, 4, 5]:
                season = "summer"
            else:
                season = "winter"
        
        seasonal_content = {
            CraftType.POTTERY: {
                "festival": "Diyas for Diwali, decorative items for celebrations",
                "monsoon": "Indoor pottery activities, water storage vessels",
                "summer": "Cooling vessels, kulhads for summer drinks",
                "winter": "Warm earth tones, cozy home decorations"
            },
            CraftType.TEXTILES: {
                "festival": "Festival wear, ceremonial textiles, bright colors",
                "monsoon": "Natural dyed fabrics, sustainable practices",
                "summer": "Light cotton fabrics, breathable weaves",
                "winter": "Warm woolen textiles, cozy patterns"
            },
            CraftType.JEWELRY: {
                "festival": "Traditional jewelry, statement pieces for celebrations",
                "monsoon": "Care tips for jewelry, protection from humidity",
                "summer": "Lightweight pieces, comfortable daily wear",
                "winter": "Layered jewelry, warm metal tones"
            },
            CraftType.WOODWORK: {
                "festival": "Decorative items, rangoli patterns in wood",
                "monsoon": "Wood care, protection from moisture",
                "summer": "Outdoor furniture, garden decorations",
                "winter": "Indoor furniture, warm wood finishes"
            }
        }
        
        content = seasonal_content.get(artisan.specialization, {}).get(season, "Seasonal craft content")
        
        return [
            ContentRecommendation(
                content_type=ContentType.SEASONAL_CONTENT,
                title_suggestion=f"Perfect {season.title()} {artisan.specialization.value.title()}",
                description=content,
                best_time_to_post=self._get_optimal_posting_time(artisan.specialization),
                hashtags=self._get_craft_hashtags(artisan.specialization, "intermediate") + [f"#{season}"],
                target_platforms=['instagram', 'facebook'],
                priority_score=0.95,
                reasoning=f"Seasonal relevance increases engagement during {season}"
            )
        ]

if __name__ == "__main__":
    # Test the specialized recommendation engine
    engine = SpecializedRecommendationEngine()
    print("🎯 Specialized Recommendation Engine initialized successfully")