"""
AI-Powered Storytelling Engine for Artisan Content
Generates compelling narratives that connect craft analysis with marketing stories
Integrates with existing A2A AI Agent system for enhanced storytelling
"""

import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai.types import HttpOptions
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
from ai_agent_manager import StoryContent, StoryType, AIAgentManager
from artisan_ai_agent import ArtisanProfile, CraftAnalysis, CraftType

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class StorytellingEngine:
    """AI-powered storytelling engine for artisan content"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.client = genai.Client(
            api_key=self.api_key, 
            http_options=HttpOptions(api_version="v1")
        )
        
        # Story templates and frameworks
        self.story_frameworks = self._initialize_story_frameworks()
        
        # Cultural storytelling elements for Indian artisans
        self.cultural_elements = self._initialize_cultural_elements()
        
        # Platform-specific storytelling guidelines
        self.platform_guidelines = self._initialize_platform_guidelines()
    
    def _initialize_story_frameworks(self) -> Dict[StoryType, Dict]:
        """Initialize storytelling frameworks for different story types"""
        return {
            StoryType.ORIGIN_STORY: {
                "structure": ["heritage", "inspiration", "first_creation", "evolution", "legacy"],
                "emotional_arc": "humble_beginnings_to_mastery",
                "key_elements": ["family_tradition", "cultural_significance", "personal_journey"],
                "call_to_action": "discover_heritage"
            },
            StoryType.CRAFT_JOURNEY: {
                "structure": ["learning", "challenges", "breakthrough", "mastery", "innovation"],
                "emotional_arc": "struggle_to_triumph",
                "key_elements": ["skill_development", "dedication", "artistic_growth"],
                "call_to_action": "appreciate_craftsmanship"
            },
            StoryType.CULTURAL_HERITAGE: {
                "structure": ["ancient_roots", "traditional_methods", "cultural_meaning", "preservation", "modern_relevance"],
                "emotional_arc": "pride_and_preservation",
                "key_elements": ["historical_context", "cultural_symbols", "traditional_techniques"],
                "call_to_action": "preserve_tradition"
            },
            StoryType.CUSTOMER_STORY: {
                "structure": ["customer_need", "craft_solution", "creation_process", "delivery", "satisfaction"],
                "emotional_arc": "problem_to_joy",
                "key_elements": ["personal_connection", "custom_creation", "emotional_value"],
                "call_to_action": "create_your_story"
            },
            StoryType.BEHIND_SCENES: {
                "structure": ["workspace", "tools", "process", "challenges", "satisfaction"],
                "emotional_arc": "curiosity_to_appreciation",
                "key_elements": ["intimate_details", "crafting_secrets", "personal_touch"],
                "call_to_action": "experience_craftsmanship"
            },
            StoryType.SEASONAL_STORY: {
                "structure": ["season_significance", "traditional_connection", "craft_adaptation", "celebration", "community"],
                "emotional_arc": "anticipation_to_celebration",
                "key_elements": ["seasonal_relevance", "festival_connection", "cultural_celebration"],
                "call_to_action": "celebrate_with_us"
            },
            StoryType.PROCESS_STORY: {
                "structure": ["raw_materials", "preparation", "creation_steps", "refinement", "final_product"],
                "emotional_arc": "transformation_journey",
                "key_elements": ["technical_skill", "artistic_vision", "patience_and_precision"],
                "call_to_action": "appreciate_process"
            },
            StoryType.INSPIRATION_STORY: {
                "structure": ["inspiration_source", "creative_vision", "design_process", "execution", "impact"],
                "emotional_arc": "inspiration_to_creation",
                "key_elements": ["creative_spark", "artistic_interpretation", "unique_perspective"],
                "call_to_action": "find_inspiration"
            }
        }
    
    def _initialize_cultural_elements(self) -> Dict[str, List[str]]:
        """Initialize Indian cultural elements for storytelling"""
        return {
            "festivals": [
                "Diwali", "Holi", "Dussehra", "Eid", "Christmas", "Karva Chauth", 
                "Raksha Bandhan", "Navratri", "Durga Puja", "Ganesh Chaturthi"
            ],
            "traditions": [
                "family_legacy", "guru_shishya_parampara", "community_bonding", 
                "spiritual_connection", "ancestral_wisdom", "cultural_pride"
            ],
            "values": [
                "respect_for_elders", "devotion_to_craft", "patience", "dedication", 
                "community_service", "cultural_preservation", "spiritual_growth"
            ],
            "symbols": [
                "lotus", "peacock", "elephant", "om", "swastika", "mandala", 
                "tree_of_life", "rangoli", "diyas", "kalash"
            ],
            "regional_elements": {
                "rajasthan": ["desert_beauty", "royal_heritage", "vibrant_colors", "folk_traditions"],
                "kerala": ["backwaters", "spices", "ayurveda", "classical_arts"],
                "punjab": ["fertility", "harvest", "bhangra", "golden_fields"],
                "gujarat": ["business_acumen", "textile_heritage", "garba", "entrepreneurship"],
                "tamil_nadu": ["temple_architecture", "classical_dance", "bronze_casting", "silk_weaving"]
            }
        }
    
    def _initialize_platform_guidelines(self) -> Dict[str, Dict]:
        """Initialize platform-specific storytelling guidelines"""
        return {
            "instagram": {
                "tone": "visual_and_inspiring",
                "length": "concise_with_impact",
                "style": "aesthetic_focused",
                "engagement": "hashtag_heavy",
                "call_to_action": "swipe_save_share"
            },
            "facebook": {
                "tone": "community_oriented",
                "length": "detailed_narrative",
                "style": "conversational",
                "engagement": "comment_discussion",
                "call_to_action": "share_experience"
            },
            "youtube": {
                "tone": "educational_entertaining",
                "length": "comprehensive_story",
                "style": "documentary_style",
                "engagement": "subscribe_like",
                "call_to_action": "watch_learn_share"
            },
            "pinterest": {
                "tone": "aspirational",
                "length": "brief_descriptive",
                "style": "DIY_inspiration",
                "engagement": "pin_save",
                "call_to_action": "try_create"
            }
        }
    
    def generate_story_content(self, 
                             artisan_profile: ArtisanProfile,
                             craft_analysis: Optional[CraftAnalysis],
                             story_type: StoryType,
                             target_platforms: List[str],
                             additional_context: Dict = None) -> StoryContent:
        """Generate AI-powered story content based on artisan profile and craft analysis"""
        try:
            # Get story framework
            framework = self.story_frameworks.get(story_type)
            
            # Build context for AI
            context = self._build_story_context(artisan_profile, craft_analysis, additional_context)
            
            # Generate story prompt
            story_prompt = self._create_story_prompt(
                artisan_profile, craft_analysis, story_type, framework, context, target_platforms
            )
            
            # Generate content using AI
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=story_prompt
            )
            
            # Parse AI response
            story_data = self._parse_story_response(response.text, story_type, target_platforms)
            
            # Create StoryContent object
            story_content = StoryContent(
                story_id=f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{story_type.value}",
                story_type=story_type,
                title=story_data.get('title', f'{artisan_profile.name} - {story_type.value.replace("_", " ").title()}'),
                narrative=story_data.get('narrative', ''),
                hook=story_data.get('hook', ''),
                call_to_action=story_data.get('call_to_action', ''),
                emotional_tone=story_data.get('emotional_tone', framework.get('emotional_arc', 'inspiring')),
                target_audience=story_data.get('target_audience', artisan_profile.target_audience),
                key_messages=story_data.get('key_messages', []),
                supporting_assets=story_data.get('supporting_assets', []),
                platform_adaptations=story_data.get('platform_adaptations', {}),
                artisan_profile_id=f"{artisan_profile.name.lower().replace(' ', '_')}",
                craft_analysis_id=getattr(craft_analysis, 'id', '') if craft_analysis else ''
            )
            
            logger.info(f"Generated {story_type.value} story for {artisan_profile.name}")
            return story_content
            
        except Exception as e:
            logger.error(f"Error generating story content: {e}")
            raise
    
    def _build_story_context(self, 
                           artisan_profile: ArtisanProfile, 
                           craft_analysis: Optional[CraftAnalysis],
                           additional_context: Dict = None) -> Dict:
        """Build comprehensive context for story generation"""
        context = {
            "artisan": {
                "name": artisan_profile.name,
                "location": artisan_profile.location,
                "specialization": artisan_profile.specialization.value,
                "experience_years": artisan_profile.experience_years,
                "signature_style": artisan_profile.signature_style,
                "target_audience": artisan_profile.target_audience
            },
            "cultural_context": self._get_cultural_context(artisan_profile.location, artisan_profile.specialization),
            "skill_level": self._determine_skill_narrative(artisan_profile.experience_years),
            "craft_details": {}
        }
        
        if craft_analysis:
            context["craft_details"] = {
                "colors": craft_analysis.colors,
                "materials": craft_analysis.materials,
                "patterns": craft_analysis.patterns,
                "style": craft_analysis.style,
                "complexity": craft_analysis.complexity_level,
                "estimated_time": craft_analysis.estimated_time
            }
        
        if additional_context:
            context.update(additional_context)
        
        return context
    
    def _get_cultural_context(self, location: str, craft_type: CraftType) -> Dict:
        """Get cultural context based on location and craft type"""
        cultural_context = {
            "regional_elements": [],
            "relevant_festivals": [],
            "traditional_values": self.cultural_elements["values"][:3],
            "cultural_symbols": []
        }
        
        # Extract state/region from location
        location_lower = location.lower()
        for region, elements in self.cultural_elements["regional_elements"].items():
            if region in location_lower:
                cultural_context["regional_elements"] = elements
                break
        
        # Add craft-specific cultural elements
        craft_cultural_map = {
            CraftType.POTTERY: ["earthy_traditions", "fire_element", "divine_creation"],
            CraftType.TEXTILES: ["weaving_traditions", "color_symbolism", "fabric_heritage"],
            CraftType.JEWELRY: ["adornment_culture", "precious_traditions", "ceremonial_importance"],
            CraftType.WOODWORK: ["tree_reverence", "carved_heritage", "furniture_traditions"]
        }
        
        cultural_context["craft_traditions"] = craft_cultural_map.get(craft_type, [])
        
        return cultural_context
    
    def _determine_skill_narrative(self, experience_years: int) -> str:
        """Determine skill level narrative based on experience"""
        if experience_years <= 2:
            return "emerging_artisan_passionate_beginner"
        elif experience_years <= 7:
            return "skilled_craftsperson_growing_expertise"
        elif experience_years <= 15:
            return "experienced_master_refined_technique"
        else:
            return "legendary_artisan_heritage_keeper"
    
    def _create_story_prompt(self, 
                           artisan_profile: ArtisanProfile,
                           craft_analysis: Optional[CraftAnalysis],
                           story_type: StoryType,
                           framework: Dict,
                           context: Dict,
                           target_platforms: List[str]) -> str:
        """Create detailed AI prompt for story generation"""
        
        prompt = f"""
        Create a compelling {story_type.value.replace('_', ' ')} story for an Indian artisan with the following details:
        
        ARTISAN PROFILE:
        - Name: {artisan_profile.name}
        - Location: {artisan_profile.location}
        - Craft: {artisan_profile.specialization.value.title()}
        - Experience: {artisan_profile.experience_years} years ({context['skill_level'].replace('_', ' ')})
        - Style: {artisan_profile.signature_style}
        - Target Audience: {artisan_profile.target_audience}
        
        """
        
        if craft_analysis:
            prompt += f"""
            CURRENT CRAFT ANALYSIS:
            - Colors: {', '.join(craft_analysis.colors)}
            - Materials: {', '.join(craft_analysis.materials)}
            - Patterns: {', '.join(craft_analysis.patterns)}
            - Style: {craft_analysis.style}
            - Complexity: {craft_analysis.complexity_level}
            - Creation Time: {craft_analysis.estimated_time}
            """
        
        prompt += f"""
        
        CULTURAL CONTEXT:
        - Regional Elements: {', '.join(context['cultural_context']['regional_elements'])}
        - Traditional Values: {', '.join(context['cultural_context']['traditional_values'])}
        - Craft Traditions: {', '.join(context['cultural_context'].get('craft_traditions', []))}
        
        STORY FRAMEWORK:
        - Type: {story_type.value.replace('_', ' ').title()}
        - Structure: {' → '.join(framework['structure'])}
        - Emotional Arc: {framework['emotional_arc'].replace('_', ' ')}
        - Key Elements: {', '.join(framework['key_elements'])}
        
        TARGET PLATFORMS: {', '.join(target_platforms)}
        
        Please generate a comprehensive story response in JSON format:
        {{
            "title": "Compelling title that captures the essence",
            "hook": "Opening line that immediately grabs attention",
            "narrative": "Complete story following the structure - compelling, authentic, culturally rich",
            "key_messages": ["3-5 key takeaway messages"],
            "emotional_tone": "Primary emotional tone of the story",
            "target_audience": "Specific audience this story resonates with",
            "call_to_action": "Clear, motivating call to action",
            "platform_adaptations": {{
                "instagram": "Instagram-optimized version (visual, concise, hashtag-friendly)",
                "facebook": "Facebook-optimized version (community-focused, discussion-worthy)",
                "youtube": "YouTube-optimized version (detailed, educational)",
                "pinterest": "Pinterest-optimized version (inspirational, actionable)"
            }},
            "supporting_assets": ["Types of visual/video content that would support this story"],
            "hashtags": ["15 relevant hashtags combining craft, culture, and story themes"],
            "cultural_hooks": ["Specific cultural elements that make this story authentically Indian"],
            "marketing_angles": ["How this story supports marketing and sales objectives"]
        }}
        
        GUIDELINES:
        - Make the story authentically Indian with cultural depth
        - Include sensory details about the craft process
        - Emphasize the human connection and emotional journey
        - Balance tradition with modern relevance
        - Include subtle marketing elements without being promotional
        - Use storytelling techniques that build trust and connection
        - Ensure the story supports sales by building value and desire
        - Make it shareable and memorable
        """
        
        return prompt
    
    def _parse_story_response(self, response_text: str, story_type: StoryType, target_platforms: List[str]) -> Dict:
        """Parse AI response and extract story data"""
        try:
            # Find JSON in response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            story_data = json.loads(json_str)
            
            return story_data
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse story JSON response: {e}")
            # Return fallback story data
            return self._create_fallback_story(story_type, target_platforms)
    
    def _create_fallback_story(self, story_type: StoryType, target_platforms: List[str]) -> Dict:
        """Create fallback story when AI parsing fails"""
        framework = self.story_frameworks.get(story_type, {})
        
        return {
            "title": f"The Art of {story_type.value.replace('_', ' ').title()}",
            "narrative": f"Every craft tells a story, and this {story_type.value.replace('_', ' ')} is no different. Through dedication and skill, our artisan brings tradition to life.",
            "hook": "In the heart of India, tradition meets artistry...",
            "call_to_action": framework.get('call_to_action', 'Discover the story behind the craft'),
            "emotional_tone": framework.get('emotional_arc', 'inspiring'),
            "target_audience": "Craft enthusiasts and cultural appreciators",
            "key_messages": ["Authentic craftsmanship", "Cultural heritage", "Artistic excellence"],
            "supporting_assets": ["process_video", "finished_product_photo"],
            "platform_adaptations": {platform: "Platform-optimized content coming soon" for platform in target_platforms}
        }
    
    def generate_marketing_story_chain(self, 
                                     artisan_profile: ArtisanProfile,
                                     craft_analysis: CraftAnalysis,
                                     content_recommendations: List[Dict]) -> List[StoryContent]:
        """Generate a chain of stories that build a comprehensive marketing narrative"""
        try:
            story_chain = []
            
            # Story sequence for marketing funnel
            story_sequence = [
                (StoryType.BEHIND_SCENES, ["instagram", "facebook"]),
                (StoryType.PROCESS_STORY, ["youtube", "instagram"]),
                (StoryType.CULTURAL_HERITAGE, ["facebook", "pinterest"]),
                (StoryType.CUSTOMER_STORY, ["instagram", "facebook"]),
                (StoryType.ORIGIN_STORY, ["youtube", "facebook"])
            ]
            
            for story_type, platforms in story_sequence:
                # Add context from content recommendations
                additional_context = {
                    "marketing_context": self._extract_marketing_context(content_recommendations),
                    "story_sequence_position": len(story_chain) + 1,
                    "total_stories": len(story_sequence)
                }
                
                story = self.generate_story_content(
                    artisan_profile=artisan_profile,
                    craft_analysis=craft_analysis,
                    story_type=story_type,
                    target_platforms=platforms,
                    additional_context=additional_context
                )
                
                story_chain.append(story)
            
            logger.info(f"Generated marketing story chain of {len(story_chain)} stories")
            return story_chain
            
        except Exception as e:
            logger.error(f"Error generating marketing story chain: {e}")
            raise
    
    def _extract_marketing_context(self, content_recommendations: List[Dict]) -> Dict:
        """Extract marketing context from content recommendations"""
        context = {
            "recommended_content_types": [],
            "priority_platforms": [],
            "key_hashtags": [],
            "optimal_posting_times": []
        }
        
        for rec in content_recommendations:
            context["recommended_content_types"].append(rec.get('content_type', ''))
            context["priority_platforms"].extend(rec.get('target_platforms', []))
            context["key_hashtags"].extend(rec.get('hashtags', [])[:5])
            context["optimal_posting_times"].append(rec.get('best_time_to_post', ''))
        
        # Remove duplicates and limit
        context["priority_platforms"] = list(set(context["priority_platforms"]))[:3]
        context["key_hashtags"] = list(set(context["key_hashtags"]))[:10]
        
        return context
    
    def optimize_story_for_sales(self, story_content: StoryContent, sales_objectives: Dict) -> StoryContent:
        """Optimize story content for specific sales objectives"""
        try:
            # Sales optimization prompt
            optimization_prompt = f"""
            Optimize this story for sales objectives:
            
            CURRENT STORY:
            Title: {story_content.title}
            Narrative: {story_content.narrative}
            Call to Action: {story_content.call_to_action}
            
            SALES OBJECTIVES:
            - Primary Goal: {sales_objectives.get('primary_goal', 'Increase brand awareness')}
            - Target Revenue: {sales_objectives.get('target_revenue', 'Not specified')}
            - Key Products: {', '.join(sales_objectives.get('key_products', []))}
            - Urgency Level: {sales_objectives.get('urgency_level', 'Medium')}
            
            Please provide sales-optimized version in JSON format:
            {{
                "optimized_title": "Sales-focused title",
                "optimized_narrative": "Narrative with subtle sales elements",
                "optimized_cta": "Strong, conversion-focused call to action",
                "sales_hooks": ["Specific elements that drive purchase intent"],
                "value_propositions": ["Clear value statements"],
                "urgency_elements": ["Elements that create appropriate urgency"]
            }}
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=optimization_prompt
            )
            
            # Parse optimization response
            try:
                start_idx = response.text.find('{')
                end_idx = response.text.rfind('}') + 1
                json_str = response.text[start_idx:end_idx]
                optimization_data = json.loads(json_str)
                
                # Update story content
                story_content.title = optimization_data.get('optimized_title', story_content.title)
                story_content.narrative = optimization_data.get('optimized_narrative', story_content.narrative)
                story_content.call_to_action = optimization_data.get('optimized_cta', story_content.call_to_action)
                
                # Add sales-specific metadata
                if not hasattr(story_content, 'sales_metadata'):
                    story_content.sales_metadata = {}
                
                story_content.sales_metadata.update({
                    'sales_hooks': optimization_data.get('sales_hooks', []),
                    'value_propositions': optimization_data.get('value_propositions', []),
                    'urgency_elements': optimization_data.get('urgency_elements', []),
                    'optimized_for_sales': True,
                    'optimization_date': datetime.now().isoformat()
                })
                
            except (json.JSONDecodeError, ValueError):
                logger.warning("Failed to parse sales optimization response")
            
            return story_content
            
        except Exception as e:
            logger.error(f"Error optimizing story for sales: {e}")
            return story_content

if __name__ == "__main__":
    # Test the storytelling engine
    engine = StorytellingEngine()
    print("📖 Storytelling Engine initialized successfully")