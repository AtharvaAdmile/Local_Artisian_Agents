#!/usr/bin/env python3
"""
AI Agent Manager for Social Media and Storytelling
Manages artisan social media presence, content assets, and storytelling
Integrates with the A2A AI Agent system for comprehensive content strategy
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SocialMediaPlatform(Enum):
    """Social media platforms supported"""
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    YOUTUBE = "youtube"
    PINTEREST = "pinterest"
    TWITTER = "twitter"
    TIKTOK = "tiktok"
    LINKEDIN = "linkedin"
    WHATSAPP = "whatsapp"

class ContentAssetType(Enum):
    """Types of content assets"""
    IMAGE = "image"
    VIDEO = "video"
    STORY = "story"
    REEL = "reel"
    POST = "post"
    CAROUSEL = "carousel"
    LIVE = "live"
    BLOG = "blog"

class StoryType(Enum):
    """Types of storytelling content"""
    ORIGIN_STORY = "origin_story"
    CRAFT_JOURNEY = "craft_journey"
    CULTURAL_HERITAGE = "cultural_heritage"
    CUSTOMER_STORY = "customer_story"
    BEHIND_SCENES = "behind_scenes"
    SEASONAL_STORY = "seasonal_story"
    PROCESS_STORY = "process_story"
    INSPIRATION_STORY = "inspiration_story"

class PostingStatus(Enum):
    """Status of content posts"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"

@dataclass
class SocialMediaProfile:
    """Social media profile configuration"""
    platform: SocialMediaPlatform
    username: str
    profile_url: str
    followers_count: int
    engagement_rate: float
    content_style: str
    posting_frequency: str
    best_posting_times: List[str]
    target_hashtags: List[str]
    bio: str
    profile_image_url: str = ""
    verified: bool = False
    business_account: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class ContentAsset:
    """Content asset for social media"""
    asset_id: str
    asset_type: ContentAssetType
    title: str
    description: str
    file_path: str
    gcs_uri: str
    tags: List[str]
    dimensions: Dict[str, int]
    file_size: int
    mime_type: str
    craft_analysis_id: str  # Link to original craft analysis
    artisan_profile_id: str
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class StoryContent:
    """AI-generated storytelling content"""
    story_id: str
    story_type: StoryType
    title: str
    narrative: str
    hook: str
    call_to_action: str
    emotional_tone: str
    target_audience: str
    key_messages: List[str]
    supporting_assets: List[str]  # Asset IDs
    platform_adaptations: Dict[str, str]  # Platform-specific versions
    artisan_profile_id: str
    craft_analysis_id: str = ""
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class ScheduledPost:
    """Scheduled social media post"""
    post_id: str
    platform: SocialMediaPlatform
    content_asset_id: str
    story_content_id: str
    caption: str
    hashtags: List[str]
    scheduled_time: datetime
    status: PostingStatus
    performance_metrics: Dict[str, int]
    artisan_profile_id: str
    created_at: datetime = None
    published_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class AIAgentManager:
    """Main AI Agent Manager for social media and storytelling"""
    
    def __init__(self):
        self.social_profiles: Dict[str, Dict[str, SocialMediaProfile]] = {}  # artisan_id -> platform -> profile
        self.content_assets: Dict[str, ContentAsset] = {}
        self.story_contents: Dict[str, StoryContent] = {}
        self.scheduled_posts: Dict[str, ScheduledPost] = {}
        
        # Load existing data
        self.load_data()
        
        # Platform-specific configurations
        self.platform_configs = self._initialize_platform_configs()
        
    def _initialize_platform_configs(self) -> Dict[SocialMediaPlatform, Dict]:
        """Initialize platform-specific configurations"""
        return {
            SocialMediaPlatform.INSTAGRAM: {
                "max_caption_length": 2200,
                "max_hashtags": 30,
                "image_aspect_ratios": ["1:1", "4:5", "9:16"],
                "video_max_length": 60,
                "optimal_posting_times": ["6-9 AM", "12-2 PM", "5-7 PM"],
                "content_types": ["photo", "video", "carousel", "reel", "story"]
            },
            SocialMediaPlatform.FACEBOOK: {
                "max_caption_length": 63206,
                "max_hashtags": 10,
                "image_aspect_ratios": ["16:9", "1:1", "4:5"],
                "video_max_length": 240,
                "optimal_posting_times": ["9-10 AM", "1-3 PM", "3-4 PM"],
                "content_types": ["photo", "video", "carousel", "event", "live"]
            },
            SocialMediaPlatform.YOUTUBE: {
                "max_title_length": 100,
                "max_description_length": 5000,
                "video_formats": ["MP4", "MOV", "AVI"],
                "optimal_posting_times": ["2-4 PM", "6-9 PM"],
                "content_types": ["video", "short", "live", "premiere"]
            },
            SocialMediaPlatform.PINTEREST: {
                "max_description_length": 500,
                "optimal_aspect_ratio": "2:3",
                "max_hashtags": 20,
                "optimal_posting_times": ["8-11 PM", "2-4 AM"],
                "content_types": ["pin", "video_pin", "story_pin"]
            }
        }
    
    def create_social_media_profile(self, 
                                  artisan_id: str,
                                  platform: SocialMediaPlatform,
                                  username: str,
                                  profile_url: str,
                                  **kwargs) -> str:
        """Create a social media profile for an artisan"""
        try:
            profile = SocialMediaProfile(
                platform=platform,
                username=username,
                profile_url=profile_url,
                followers_count=kwargs.get('followers_count', 0),
                engagement_rate=kwargs.get('engagement_rate', 0.0),
                content_style=kwargs.get('content_style', 'Traditional craft showcase'),
                posting_frequency=kwargs.get('posting_frequency', 'Daily'),
                best_posting_times=kwargs.get('best_posting_times', 
                    self.platform_configs[platform]["optimal_posting_times"]),
                target_hashtags=kwargs.get('target_hashtags', []),
                bio=kwargs.get('bio', ''),
                profile_image_url=kwargs.get('profile_image_url', ''),
                verified=kwargs.get('verified', False),
                business_account=kwargs.get('business_account', False)
            )
            
            if artisan_id not in self.social_profiles:
                self.social_profiles[artisan_id] = {}
            
            self.social_profiles[artisan_id][platform.value] = profile
            self.save_data()
            
            logger.info(f"Created {platform.value} profile for artisan {artisan_id}")
            return f"{artisan_id}_{platform.value}"
            
        except Exception as e:
            logger.error(f"Error creating social media profile: {e}")
            raise
    
    def add_content_asset(self,
                         asset_type: ContentAssetType,
                         title: str,
                         description: str,
                         file_path: str,
                         gcs_uri: str,
                         artisan_profile_id: str,
                         craft_analysis_id: str = "",
                         **kwargs) -> str:
        """Add a content asset to the management system"""
        try:
            asset_id = f"asset_{uuid.uuid4().hex[:12]}"
            
            asset = ContentAsset(
                asset_id=asset_id,
                asset_type=asset_type,
                title=title,
                description=description,
                file_path=file_path,
                gcs_uri=gcs_uri,
                tags=kwargs.get('tags', []),
                dimensions=kwargs.get('dimensions', {}),
                file_size=kwargs.get('file_size', 0),
                mime_type=kwargs.get('mime_type', ''),
                craft_analysis_id=craft_analysis_id,
                artisan_profile_id=artisan_profile_id
            )
            
            self.content_assets[asset_id] = asset
            self.save_data()
            
            logger.info(f"Added content asset {asset_id} for artisan {artisan_profile_id}")
            return asset_id
            
        except Exception as e:
            logger.error(f"Error adding content asset: {e}")
            raise
    
    def get_artisan_social_profiles(self, artisan_id: str) -> Dict[str, SocialMediaProfile]:
        """Get all social media profiles for an artisan"""
        return self.social_profiles.get(artisan_id, {})
    
    def get_artisan_content_assets(self, artisan_id: str) -> List[ContentAsset]:
        """Get all content assets for an artisan"""
        return [asset for asset in self.content_assets.values() 
                if asset.artisan_profile_id == artisan_id]
    
    def get_artisan_stories(self, artisan_id: str) -> List[StoryContent]:
        """Get all story content for an artisan"""
        return [story for story in self.story_contents.values() 
                if story.artisan_profile_id == artisan_id]
    
    def update_social_profile(self, artisan_id: str, platform: str, **updates) -> bool:
        """Update social media profile"""
        try:
            if artisan_id in self.social_profiles and platform in self.social_profiles[artisan_id]:
                profile = self.social_profiles[artisan_id][platform]
                
                for key, value in updates.items():
                    if hasattr(profile, key):
                        setattr(profile, key, value)
                
                self.save_data()
                logger.info(f"Updated {platform} profile for artisan {artisan_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating social profile: {e}")
            return False
    
    def delete_content_asset(self, asset_id: str) -> bool:
        """Delete a content asset"""
        try:
            if asset_id in self.content_assets:
                del self.content_assets[asset_id]
                self.save_data()
                logger.info(f"Deleted content asset {asset_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting content asset: {e}")
            return False
    
    def get_platform_analytics(self, artisan_id: str) -> Dict[str, Dict]:
        """Get analytics across all platforms for an artisan"""
        analytics = {}
        
        if artisan_id in self.social_profiles:
            for platform, profile in self.social_profiles[artisan_id].items():
                analytics[platform] = {
                    "followers": profile.followers_count,
                    "engagement_rate": profile.engagement_rate,
                    "posts_scheduled": len([p for p in self.scheduled_posts.values() 
                                          if p.artisan_profile_id == artisan_id 
                                          and p.platform.value == platform]),
                    "content_assets": len([a for a in self.content_assets.values() 
                                         if a.artisan_profile_id == artisan_id])
                }
        
        return analytics
    
    def save_data(self):
        """Save all data to files"""
        try:
            # Save social profiles
            profiles_data = {}
            for artisan_id, platforms in self.social_profiles.items():
                profiles_data[artisan_id] = {}
                for platform, profile in platforms.items():
                    profile_dict = asdict(profile)
                    profile_dict['platform'] = profile.platform.value
                    profile_dict['created_at'] = profile.created_at.isoformat()
                    profiles_data[artisan_id][platform] = profile_dict
            
            with open('social_media_profiles.json', 'w', encoding='utf-8') as f:
                json.dump(profiles_data, f, indent=2, ensure_ascii=False)
            
            # Save content assets
            assets_data = {}
            for asset_id, asset in self.content_assets.items():
                asset_dict = asdict(asset)
                asset_dict['asset_type'] = asset.asset_type.value
                asset_dict['created_at'] = asset.created_at.isoformat()
                assets_data[asset_id] = asset_dict
            
            with open('content_assets.json', 'w', encoding='utf-8') as f:
                json.dump(assets_data, f, indent=2, ensure_ascii=False)
            
            # Save story contents
            stories_data = {}
            for story_id, story in self.story_contents.items():
                story_dict = asdict(story)
                story_dict['story_type'] = story.story_type.value
                story_dict['created_at'] = story.created_at.isoformat()
                stories_data[story_id] = story_dict
            
            with open('story_contents.json', 'w', encoding='utf-8') as f:
                json.dump(stories_data, f, indent=2, ensure_ascii=False)
            
            # Save scheduled posts
            posts_data = {}
            for post_id, post in self.scheduled_posts.items():
                post_dict = asdict(post)
                post_dict['platform'] = post.platform.value
                post_dict['status'] = post.status.value
                post_dict['scheduled_time'] = post.scheduled_time.isoformat()
                post_dict['created_at'] = post.created_at.isoformat()
                if post.published_at:
                    post_dict['published_at'] = post.published_at.isoformat()
                posts_data[post_id] = post_dict
            
            with open('scheduled_posts.json', 'w', encoding='utf-8') as f:
                json.dump(posts_data, f, indent=2, ensure_ascii=False)
            
            logger.info("Social media manager data saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise
    
    def load_data(self):
        """Load data from files"""
        try:
            # Load social profiles
            try:
                with open('social_media_profiles.json', 'r', encoding='utf-8') as f:
                    profiles_data = json.load(f)
                
                for artisan_id, platforms in profiles_data.items():
                    self.social_profiles[artisan_id] = {}
                    for platform, profile_dict in platforms.items():
                        profile_dict['platform'] = SocialMediaPlatform(profile_dict['platform'])
                        profile_dict['created_at'] = datetime.fromisoformat(profile_dict['created_at'])
                        self.social_profiles[artisan_id][platform] = SocialMediaProfile(**profile_dict)
                
                logger.info(f"Loaded {len(self.social_profiles)} social media profiles")
            except FileNotFoundError:
                logger.info("No existing social media profiles file found")
            
            # Load content assets
            try:
                with open('content_assets.json', 'r', encoding='utf-8') as f:
                    assets_data = json.load(f)
                
                for asset_id, asset_dict in assets_data.items():
                    asset_dict['asset_type'] = ContentAssetType(asset_dict['asset_type'])
                    asset_dict['created_at'] = datetime.fromisoformat(asset_dict['created_at'])
                    self.content_assets[asset_id] = ContentAsset(**asset_dict)
                
                logger.info(f"Loaded {len(self.content_assets)} content assets")
            except FileNotFoundError:
                logger.info("No existing content assets file found")
            
            # Load story contents
            try:
                with open('story_contents.json', 'r', encoding='utf-8') as f:
                    stories_data = json.load(f)
                
                for story_id, story_dict in stories_data.items():
                    story_dict['story_type'] = StoryType(story_dict['story_type'])
                    story_dict['created_at'] = datetime.fromisoformat(story_dict['created_at'])
                    self.story_contents[story_id] = StoryContent(**story_dict)
                
                logger.info(f"Loaded {len(self.story_contents)} story contents")
            except FileNotFoundError:
                logger.info("No existing story contents file found")
            
            # Load scheduled posts
            try:
                with open('scheduled_posts.json', 'r', encoding='utf-8') as f:
                    posts_data = json.load(f)
                
                for post_id, post_dict in posts_data.items():
                    post_dict['platform'] = SocialMediaPlatform(post_dict['platform'])
                    post_dict['status'] = PostingStatus(post_dict['status'])
                    post_dict['scheduled_time'] = datetime.fromisoformat(post_dict['scheduled_time'])
                    post_dict['created_at'] = datetime.fromisoformat(post_dict['created_at'])
                    if post_dict.get('published_at'):
                        post_dict['published_at'] = datetime.fromisoformat(post_dict['published_at'])
                    self.scheduled_posts[post_id] = ScheduledPost(**post_dict)
                
                logger.info(f"Loaded {len(self.scheduled_posts)} scheduled posts")
            except FileNotFoundError:
                logger.info("No existing scheduled posts file found")
                
        except Exception as e:
            logger.error(f"Error loading data: {e}")

if __name__ == "__main__":
    print("🤖 AI Agent Manager - Social Media & Storytelling System")
    print("=" * 60)
    manager = AIAgentManager()
    print(f"System initialized with:")
    print(f"- {sum(len(platforms) for platforms in manager.social_profiles.values())} social media profiles")
    print(f"- {len(manager.content_assets)} content assets")
    print(f"- {len(manager.story_contents)} story contents")
    print(f"- {len(manager.scheduled_posts)} scheduled posts")