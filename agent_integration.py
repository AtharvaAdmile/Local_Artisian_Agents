"""
Agent Integration Layer
Connects A2A AI Agent with Social Media Manager for seamless workflow
Chains inputs from craft analysis + profile to generate comprehensive stories
"""

import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import asdict

# Import existing A2A AI Agent components
from artisan_ai_agent import ArtisanProfile, CraftType, ContentType
from profile_manager import ProfileManager
from gcs_image_analyzer import GCSCraftImageAnalyzer
from content_strategist import ContentStrategist
from specialized_recommendations import SpecializedRecommendationEngine

# Import new Social Media Manager components
from ai_agent_manager import AIAgentManager, SocialMediaPlatform, ContentAssetType, StoryType
from storytelling_engine import StorytellingEngine

logger = logging.getLogger(__name__)

class IntegratedAIAgentSystem:
    """Integrated system that combines craft analysis, content strategy, and social media management"""
    
    def __init__(self):
        # Initialize A2A AI Agent components
        self.profile_manager = ProfileManager()
        self.image_analyzer = GCSCraftImageAnalyzer()
        self.content_strategist = ContentStrategist()
        self.specialized_engine = SpecializedRecommendationEngine()
        
        # Initialize Social Media Manager components
        self.social_media_manager = AIAgentManager()
        self.storytelling_engine = StorytellingEngine()
        
        logger.info("Integrated AI Agent System initialized successfully")
    
    def complete_artisan_workflow(self, 
                                 artisan_data: Dict,
                                 uploaded_image_file,
                                 social_media_setup: Dict,
                                 story_preferences: Dict = None) -> Dict:
        """
        Complete workflow from artisan onboarding to social media content generation
        """
        try:
            workflow_result = {
                "artisan_profile": None,
                "craft_analysis": None,
                "content_recommendations": [],
                "social_media_profiles": [],
                "story_content": [],
                "content_assets": [],
                "integrated_strategy": {}
            }
            
            # Step 1: Create or get artisan profile
            logger.info("Step 1: Creating artisan profile")
            artisan_profile_id = self.profile_manager.create_profile(
                name=artisan_data['name'],
                location=artisan_data['location'],
                specialization=CraftType(artisan_data['specialization']),
                experience_years=artisan_data['experience_years'],
                signature_style=artisan_data.get('signature_style'),
                target_audience=artisan_data.get('target_audience'),
                social_media_platforms=artisan_data.get('social_media_platforms', [])
            )
            
            artisan_profile = self.profile_manager.get_profile(artisan_profile_id)
            workflow_result["artisan_profile"] = artisan_profile_id
            
            # Step 2: Analyze craft image if provided
            if uploaded_image_file:
                logger.info("Step 2: Analyzing craft image")
                analysis_result = self.image_analyzer.analyze_uploaded_image(
                    uploaded_image_file, artisan_profile_id
                )
                workflow_result["craft_analysis"] = analysis_result
                
                # Create content asset for the uploaded image
                asset_id = self.social_media_manager.add_content_asset(
                    asset_type=ContentAssetType.IMAGE,
                    title=f"{artisan_profile.name}'s {artisan_profile.specialization.value} Work",
                    description=analysis_result['analysis']['style'],
                    file_path=uploaded_image_file.name,
                    gcs_uri=analysis_result['gcs_uri'],
                    artisan_profile_id=artisan_profile_id,
                    craft_analysis_id=analysis_result.get('analysis_id', ''),
                    tags=analysis_result['analysis']['colors'] + analysis_result['analysis']['materials'],
                    mime_type=uploaded_image_file.type
                )
                workflow_result["content_assets"].append(asset_id)
            
            # Step 3: Generate content recommendations
            logger.info("Step 3: Generating content recommendations")
            craft_analysis_obj = self._convert_to_craft_analysis(
                workflow_result["craft_analysis"]["analysis"]) if workflow_result["craft_analysis"] else None
            
            general_recommendations = self.content_strategist.generate_content_strategy(
                artisan_profile, craft_analysis_obj
            )
            specialized_recommendations = self.specialized_engine.get_specialized_recommendations(
                artisan_profile, craft_analysis_obj
            )
            
            workflow_result["content_recommendations"] = {
                "general": [self._recommendation_to_dict(rec) for rec in general_recommendations],
                "specialized": [self._recommendation_to_dict(rec) for rec in specialized_recommendations]
            }
            
            # Step 4: Set up social media profiles
            logger.info("Step 4: Setting up social media profiles")
            for platform_data in social_media_setup.get('platforms', []):
                profile_id = self.social_media_manager.create_social_media_profile(
                    artisan_id=artisan_profile_id,
                    platform=SocialMediaPlatform(platform_data['platform']),
                    username=platform_data['username'],
                    profile_url=platform_data['profile_url'],
                    **platform_data.get('additional_data', {})
                )
                workflow_result["social_media_profiles"].append(profile_id)
            
            # Step 5: Generate storytelling content
            logger.info("Step 5: Generating storytelling content")
            if story_preferences:
                story_types = story_preferences.get('story_types', [StoryType.ORIGIN_STORY, StoryType.CRAFT_JOURNEY])
                target_platforms = story_preferences.get('target_platforms', ['instagram', 'facebook'])
                
                for story_type in story_types:
                    story_content = self.storytelling_engine.generate_story_content(
                        artisan_profile=artisan_profile,
                        craft_analysis=craft_analysis_obj,
                        story_type=StoryType(story_type) if isinstance(story_type, str) else story_type,
                        target_platforms=target_platforms,
                        additional_context=story_preferences.get('additional_context', {})
                    )
                    
                    # Store story content
                    self.social_media_manager.story_contents[story_content.story_id] = story_content
                    workflow_result["story_content"].append(story_content.story_id)
            
            # Step 6: Create integrated content strategy
            logger.info("Step 6: Creating integrated content strategy")
            integrated_strategy = self.create_integrated_strategy(
                artisan_profile_id, 
                workflow_result["content_recommendations"],
                workflow_result["story_content"]
            )
            workflow_result["integrated_strategy"] = integrated_strategy
            
            # Save all data
            self.social_media_manager.save_data()
            
            logger.info("Complete artisan workflow finished successfully")
            return workflow_result
            
        except Exception as e:
            logger.error(f"Error in complete artisan workflow: {e}")
            raise
    
    def generate_marketing_story_chain(self, 
                                     artisan_profile_id: str,
                                     craft_analysis_data: Dict = None,
                                     marketing_objectives: Dict = None) -> List[str]:
        """Generate a chain of stories optimized for marketing and sales"""
        try:
            artisan_profile = self.profile_manager.get_profile(artisan_profile_id)
            if not artisan_profile:
                raise ValueError(f"Artisan profile {artisan_profile_id} not found")
            
            # Convert craft analysis data if provided
            craft_analysis = None
            if craft_analysis_data:
                craft_analysis = self._convert_to_craft_analysis(craft_analysis_data)
            
            # Get content recommendations for context
            content_recommendations = self.content_strategist.generate_content_strategy(
                artisan_profile, craft_analysis
            )
            content_recs_dict = [self._recommendation_to_dict(rec) for rec in content_recommendations]
            
            # Generate marketing story chain
            story_chain = self.storytelling_engine.generate_marketing_story_chain(
                artisan_profile=artisan_profile,
                craft_analysis=craft_analysis,
                content_recommendations=content_recs_dict
            )
            
            # Store stories and optimize for sales if objectives provided
            story_ids = []
            for story in story_chain:
                if marketing_objectives:
                    story = self.storytelling_engine.optimize_story_for_sales(
                        story, marketing_objectives
                    )
                
                self.social_media_manager.story_contents[story.story_id] = story
                story_ids.append(story.story_id)
            
            # Save data
            self.social_media_manager.save_data()
            
            logger.info(f"Generated marketing story chain with {len(story_ids)} stories")
            return story_ids
            
        except Exception as e:
            logger.error(f"Error generating marketing story chain: {e}")
            raise
    
    def create_content_calendar(self, 
                              artisan_profile_id: str,
                              days: int = 30,
                              include_stories: bool = True) -> Dict:
        """Create integrated content calendar combining recommendations and stories"""
        try:
            artisan_profile = self.profile_manager.get_profile(artisan_profile_id)
            if not artisan_profile:
                raise ValueError(f"Artisan profile {artisan_profile_id} not found")
            
            # Get base content calendar
            base_calendar = self.content_strategist.generate_content_calendar(artisan_profile, days)
            
            # Get artisan's stories
            artisan_stories = self.social_media_manager.get_artisan_stories(artisan_profile_id)
            
            # Integrate stories into calendar
            integrated_calendar = {}
            story_index = 0
            
            for i in range(days):
                date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
                
                daily_content = {
                    "content_recommendations": base_calendar.get(date, []),
                    "story_content": [],
                    "suggested_posts": []
                }
                
                # Add stories every 3-4 days
                if include_stories and i % 3 == 0 and story_index < len(artisan_stories):
                    daily_content["story_content"].append({
                        "story_id": artisan_stories[story_index].story_id,
                        "story_type": artisan_stories[story_index].story_type.value,
                        "title": artisan_stories[story_index].title,
                        "platforms": list(artisan_stories[story_index].platform_adaptations.keys())
                    })
                    story_index += 1
                
                # Create suggested posts combining recommendations and stories
                daily_content["suggested_posts"] = self._create_daily_post_suggestions(
                    daily_content["content_recommendations"],
                    daily_content["story_content"]
                )
                
                integrated_calendar[date] = daily_content
            
            logger.info(f"Created integrated content calendar for {days} days")
            return integrated_calendar
            
        except Exception as e:
            logger.error(f"Error creating content calendar: {e}")
            raise
    
    def create_integrated_strategy(self, 
                                 artisan_profile_id: str,
                                 content_recommendations: Dict,
                                 story_content_ids: List[str]) -> Dict:
        """Create comprehensive integrated strategy"""
        try:
            artisan_profile = self.profile_manager.get_profile(artisan_profile_id)
            social_profiles = self.social_media_manager.get_artisan_social_profiles(artisan_profile_id)
            content_assets = self.social_media_manager.get_artisan_content_assets(artisan_profile_id)
            
            integrated_strategy = {
                "overview": {
                    "artisan_name": artisan_profile.name,
                    "specialization": artisan_profile.specialization.value,
                    "experience_level": self._determine_experience_level(artisan_profile.experience_years),
                    "target_audience": artisan_profile.target_audience,
                    "content_pillars": self._extract_content_pillars(content_recommendations),
                    "storytelling_themes": self._extract_storytelling_themes(story_content_ids)
                },
                "platform_strategy": {},
                "content_mix": self._analyze_content_mix(content_recommendations, story_content_ids),
                "posting_schedule": self._create_posting_schedule(social_profiles),
                "performance_targets": self._set_performance_targets(artisan_profile, social_profiles),
                "growth_recommendations": self._generate_growth_recommendations(artisan_profile, social_profiles)
            }
            
            # Platform-specific strategies
            for platform, profile in social_profiles.items():
                integrated_strategy["platform_strategy"][platform] = {
                    "content_focus": self._get_platform_content_focus(platform, content_recommendations),
                    "posting_frequency": profile.posting_frequency,
                    "optimal_times": profile.best_posting_times,
                    "engagement_strategy": self._get_engagement_strategy(platform),
                    "growth_tactics": self._get_platform_growth_tactics(platform)
                }
            
            return integrated_strategy
            
        except Exception as e:
            logger.error(f"Error creating integrated strategy: {e}")
            raise
    
    def _convert_to_craft_analysis(self, analysis_data: Dict):
        """Convert analysis data dictionary to CraftAnalysis object"""
        from artisan_ai_agent import CraftAnalysis, CraftType
        
        return CraftAnalysis(
            colors=analysis_data.get('colors', []),
            patterns=analysis_data.get('patterns', []),
            materials=analysis_data.get('materials', []),
            style=analysis_data.get('style', ''),
            craft_type=CraftType(analysis_data.get('craft_type', 'unknown')),
            complexity_level=analysis_data.get('complexity_level', 'intermediate'),
            estimated_time=analysis_data.get('estimated_time', '2-4 hours'),
            confidence_score=float(analysis_data.get('confidence_score', 0.8))
        )
    
    def _recommendation_to_dict(self, recommendation) -> Dict:
        """Convert recommendation object to dictionary"""
        return {
            'title_suggestion': recommendation.title_suggestion,
            'content_type': recommendation.content_type.value,
            'description': recommendation.description,
            'best_time_to_post': recommendation.best_time_to_post,
            'hashtags': recommendation.hashtags,
            'target_platforms': recommendation.target_platforms,
            'priority_score': recommendation.priority_score,
            'reasoning': recommendation.reasoning
        }
    
    def _determine_experience_level(self, years: int) -> str:
        """Determine experience level description"""
        if years <= 2:
            return "Emerging Artisan"
        elif years <= 7:
            return "Skilled Craftsperson"
        elif years <= 15:
            return "Expert Artisan"
        else:
            return "Master Craftsperson"
    
    def _extract_content_pillars(self, content_recommendations: Dict) -> List[str]:
        """Extract main content pillars from recommendations"""
        pillars = set()
        
        for category in ['general', 'specialized']:
            for rec in content_recommendations.get(category, []):
                content_type = rec.get('content_type', '').replace('_', ' ').title()
                pillars.add(content_type)
        
        return list(pillars)[:5]  # Top 5 pillars
    
    def _extract_storytelling_themes(self, story_content_ids: List[str]) -> List[str]:
        """Extract storytelling themes from story content"""
        themes = []
        
        for story_id in story_content_ids:
            if story_id in self.social_media_manager.story_contents:
                story = self.social_media_manager.story_contents[story_id]
                themes.append(story.story_type.value.replace('_', ' ').title())
        
        return themes
    
    def _analyze_content_mix(self, content_recommendations: Dict, story_content_ids: List[str]) -> Dict:
        """Analyze the mix of content types"""
        content_types = {}
        
        # Count content recommendations
        for category in ['general', 'specialized']:
            for rec in content_recommendations.get(category, []):
                content_type = rec.get('content_type', 'unknown')
                content_types[content_type] = content_types.get(content_type, 0) + 1
        
        # Add story content
        story_count = len(story_content_ids)
        if story_count > 0:
            content_types['storytelling'] = story_count
        
        return content_types
    
    def _create_posting_schedule(self, social_profiles: Dict) -> Dict:
        """Create posting schedule based on social profiles"""
        schedule = {}
        
        for platform, profile in social_profiles.items():
            schedule[platform] = {
                "frequency": profile.posting_frequency,
                "optimal_times": profile.best_posting_times,
                "weekly_posts": self._calculate_weekly_posts(profile.posting_frequency)
            }
        
        return schedule
    
    def _calculate_weekly_posts(self, frequency: str) -> int:
        """Calculate weekly posts based on frequency"""
        frequency_map = {
            "daily": 7,
            "every_other_day": 3,
            "twice_weekly": 2,
            "weekly": 1,
            "bi_weekly": 0.5
        }
        return frequency_map.get(frequency.lower().replace(' ', '_'), 3)
    
    def _set_performance_targets(self, artisan_profile, social_profiles: Dict) -> Dict:
        """Set performance targets based on profile and platform data"""
        targets = {
            "follower_growth": "5-10% monthly",
            "engagement_rate": "3-5% minimum",
            "content_reach": "Increase by 20% monthly",
            "story_engagement": "Higher than average posts",
            "sales_inquiries": "2-5 per month through social media"
        }
        
        # Adjust targets based on experience level
        if artisan_profile.experience_years > 10:
            targets["brand_recognition"] = "Establish as expert in " + artisan_profile.specialization.value
        
        return targets
    
    def _generate_growth_recommendations(self, artisan_profile, social_profiles: Dict) -> List[str]:
        """Generate specific growth recommendations"""
        recommendations = [
            "Maintain consistent posting schedule across all platforms",
            "Engage with followers through comments and direct messages",
            "Use storytelling to build emotional connections with audience",
            "Collaborate with other local artisans for cross-promotion",
            "Share behind-the-scenes content to build authenticity"
        ]
        
        # Add platform-specific recommendations
        if 'instagram' in social_profiles:
            recommendations.append("Use Instagram Reels for process videos")
        
        if 'youtube' in social_profiles:
            recommendations.append("Create detailed tutorial videos for YouTube")
        
        return recommendations
    
    def _get_platform_content_focus(self, platform: str, content_recommendations: Dict) -> str:
        """Get content focus for specific platform"""
        platform_focus = {
            "instagram": "Visual storytelling and behind-the-scenes content",
            "facebook": "Community building and detailed craft stories",
            "youtube": "Educational content and detailed tutorials",
            "pinterest": "Inspirational craft ideas and process images"
        }
        
        return platform_focus.get(platform, "Craft showcase and storytelling")
    
    def _get_engagement_strategy(self, platform: str) -> str:
        """Get engagement strategy for platform"""
        strategies = {
            "instagram": "Stories, polls, Q&A sessions, and user-generated content",
            "facebook": "Community posts, event announcements, and live videos",
            "youtube": "Comment responses, community posts, and collaborations",
            "pinterest": "Rich pins, seasonal boards, and DIY content"
        }
        
        return strategies.get(platform, "Regular interaction and community building")
    
    def _get_platform_growth_tactics(self, platform: str) -> List[str]:
        """Get platform-specific growth tactics"""
        tactics = {
            "instagram": ["Use trending hashtags", "Post at optimal times", "Create Reels", "Engage with craft community"],
            "facebook": ["Join craft groups", "Share in local communities", "Use Facebook Shops", "Host live sessions"],
            "youtube": ["Optimize video titles", "Create playlists", "Use custom thumbnails", "Collaborate with creators"],
            "pinterest": ["Create seasonal boards", "Use rich pins", "Pin consistently", "Join group boards"]
        }
        
        return tactics.get(platform, ["Consistent posting", "Community engagement"])
    
    def _create_daily_post_suggestions(self, content_recs: List, story_content: List) -> List[Dict]:
        """Create daily post suggestions combining recommendations and stories"""
        suggestions = []
        
        # Add content recommendations as post suggestions
        for rec in content_recs:
            suggestions.append({
                "type": "content_recommendation",
                "title": rec.title_suggestion if hasattr(rec, 'title_suggestion') else "Content Post",
                "description": rec.description if hasattr(rec, 'description') else "Regular content post",
                "platforms": rec.target_platforms if hasattr(rec, 'target_platforms') else ["instagram"]
            })
        
        # Add story content as post suggestions
        for story in story_content:
            suggestions.append({
                "type": "story_content",
                "title": story.get("title", "Story Post"),
                "description": "Storytelling content for audience engagement",
                "platforms": story.get("platforms", ["instagram", "facebook"])
            })
        
        return suggestions

if __name__ == "__main__":
    # Test the integrated system
    integrated_system = IntegratedAIAgentSystem()
    print("🔗 Integrated AI Agent System initialized successfully")