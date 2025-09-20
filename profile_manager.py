"""
Artisan Profile Management System
Manages artisan profiles, preferences, and specialization tracking
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import asdict
from artisan_ai_agent import ArtisanProfile, CraftType

logger = logging.getLogger(__name__)

class ProfileManager:
    """Manages artisan profiles and their specializations"""
    
    def __init__(self, profiles_file: str = "artisan_profiles.json"):
        self.profiles_file = profiles_file
        self.profiles: Dict[str, ArtisanProfile] = {}
        self.load_profiles()
    
    def create_profile(self, 
                      name: str,
                      location: str,
                      specialization: CraftType,
                      experience_years: int,
                      signature_style: str,
                      target_audience: str,
                      social_media_platforms: List[str]) -> str:
        """Create a new artisan profile"""
        try:
            # Generate unique profile ID
            profile_id = f"{name.lower().replace(' ', '_')}_{len(self.profiles) + 1}"
            
            # Create profile
            profile = ArtisanProfile(
                name=name,
                location=location,
                specialization=specialization,
                experience_years=experience_years,
                signature_style=signature_style,
                target_audience=target_audience,
                social_media_platforms=social_media_platforms
            )
            
            # Store profile
            self.profiles[profile_id] = profile
            self.save_profiles()
            
            logger.info(f"Created profile for {name} with ID: {profile_id}")
            return profile_id
            
        except Exception as e:
            logger.error(f"Error creating profile: {e}")
            raise
    
    def get_profile(self, profile_id: str) -> Optional[ArtisanProfile]:
        """Get artisan profile by ID"""
        return self.profiles.get(profile_id)
    
    def update_profile(self, profile_id: str, **kwargs) -> bool:
        """Update artisan profile"""
        try:
            if profile_id not in self.profiles:
                logger.warning(f"Profile {profile_id} not found")
                return False
            
            profile = self.profiles[profile_id]
            
            # Update allowed fields
            allowed_fields = [
                'name', 'location', 'specialization', 'experience_years',
                'signature_style', 'target_audience', 'social_media_platforms'
            ]
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    if field == 'specialization' and isinstance(value, str):
                        value = CraftType(value.lower())
                    setattr(profile, field, value)
            
            self.save_profiles()
            logger.info(f"Updated profile {profile_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            return False
    
    def delete_profile(self, profile_id: str) -> bool:
        """Delete artisan profile"""
        try:
            if profile_id in self.profiles:
                del self.profiles[profile_id]
                self.save_profiles()
                logger.info(f"Deleted profile {profile_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting profile: {e}")
            return False
    
    def list_profiles(self) -> List[Dict]:
        """List all profiles with basic info"""
        profile_list = []
        for profile_id, profile in self.profiles.items():
            profile_info = {
                'id': profile_id,
                'name': profile.name,
                'location': profile.location,
                'specialization': profile.specialization.value,
                'experience_years': profile.experience_years,
                'created_at': profile.created_at.isoformat()
            }
            profile_list.append(profile_info)
        return profile_list
    
    def find_profiles_by_craft(self, craft_type: CraftType) -> List[str]:
        """Find profiles by craft specialization"""
        matching_profiles = []
        for profile_id, profile in self.profiles.items():
            if profile.specialization == craft_type:
                matching_profiles.append(profile_id)
        return matching_profiles
    
    def find_profiles_by_location(self, location: str) -> List[str]:
        """Find profiles by location"""
        matching_profiles = []
        location_lower = location.lower()
        for profile_id, profile in self.profiles.items():
            if location_lower in profile.location.lower():
                matching_profiles.append(profile_id)
        return matching_profiles
    
    def get_craft_statistics(self) -> Dict[str, int]:
        """Get statistics about craft types"""
        stats = {}
        for profile in self.profiles.values():
            craft_name = profile.specialization.value
            stats[craft_name] = stats.get(craft_name, 0) + 1
        return stats
    
    def get_experience_distribution(self) -> Dict[str, int]:
        """Get distribution of experience levels"""
        distribution = {
            'beginner (0-2 years)': 0,
            'intermediate (3-7 years)': 0,
            'experienced (8-15 years)': 0,
            'expert (15+ years)': 0
        }
        
        for profile in self.profiles.values():
            years = profile.experience_years
            if years <= 2:
                distribution['beginner (0-2 years)'] += 1
            elif years <= 7:
                distribution['intermediate (3-7 years)'] += 1
            elif years <= 15:
                distribution['experienced (8-15 years)'] += 1
            else:
                distribution['expert (15+ years)'] += 1
        
        return distribution
    
    def save_profiles(self):
        """Save profiles to JSON file"""
        try:
            profiles_data = {}
            for profile_id, profile in self.profiles.items():
                profile_dict = asdict(profile)
                profile_dict['created_at'] = profile.created_at.isoformat()
                profile_dict['specialization'] = profile.specialization.value
                profiles_data[profile_id] = profile_dict
            
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(profiles_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(self.profiles)} profiles to {self.profiles_file}")
            
        except Exception as e:
            logger.error(f"Error saving profiles: {e}")
            raise
    
    def load_profiles(self):
        """Load profiles from JSON file"""
        try:
            with open(self.profiles_file, 'r', encoding='utf-8') as f:
                profiles_data = json.load(f)
            
            for profile_id, profile_dict in profiles_data.items():
                try:
                    profile_dict['specialization'] = CraftType(profile_dict['specialization'])
                    profile_dict['created_at'] = datetime.fromisoformat(profile_dict['created_at'])
                    self.profiles[profile_id] = ArtisanProfile(**profile_dict)
                except Exception as e:
                    logger.warning(f"Error loading profile {profile_id}: {e}")
            
            logger.info(f"Loaded {len(self.profiles)} profiles from {self.profiles_file}")
            
        except FileNotFoundError:
            logger.info("No existing profiles file found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading profiles: {e}")
    
    def export_profiles(self, export_file: str = None) -> str:
        """Export profiles to a backup file"""
        if export_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_file = f"profiles_backup_{timestamp}.json"
        
        try:
            profiles_data = {}
            for profile_id, profile in self.profiles.items():
                profile_dict = asdict(profile)
                profile_dict['created_at'] = profile.created_at.isoformat()
                profile_dict['specialization'] = profile.specialization.value
                profiles_data[profile_id] = profile_dict
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(profiles_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported {len(self.profiles)} profiles to {export_file}")
            return export_file
            
        except Exception as e:
            logger.error(f"Error exporting profiles: {e}")
            raise
    
    def validate_profile_data(self, profile_data: Dict) -> List[str]:
        """Validate profile data and return list of errors"""
        errors = []
        
        required_fields = ['name', 'location', 'specialization', 'experience_years', 
                          'signature_style', 'target_audience', 'social_media_platforms']
        
        for field in required_fields:
            if field not in profile_data:
                errors.append(f"Missing required field: {field}")
        
        if 'experience_years' in profile_data:
            try:
                years = int(profile_data['experience_years'])
                if years < 0 or years > 80:
                    errors.append("Experience years must be between 0 and 80")
            except (ValueError, TypeError):
                errors.append("Experience years must be a valid number")
        
        if 'specialization' in profile_data:
            try:
                CraftType(profile_data['specialization'].lower())
            except ValueError:
                valid_crafts = [craft.value for craft in CraftType]
                errors.append(f"Invalid specialization. Valid options: {valid_crafts}")
        
        if 'social_media_platforms' in profile_data:
            platforms = profile_data['social_media_platforms']
            if not isinstance(platforms, list) or len(platforms) == 0:
                errors.append("At least one social media platform is required")
        
        return errors

# Craft-specific profile templates for quick setup
CRAFT_PROFILE_TEMPLATES = {
    CraftType.POTTERY: {
        "signature_style": "Traditional terracotta pottery with modern designs",
        "target_audience": "Home decor enthusiasts and functional pottery users",
        "suggested_platforms": ["instagram", "youtube", "facebook"],
        "common_hashtags": ["#pottery", "#ceramics", "#handmade", "#terracotta"]
    },
    CraftType.TEXTILES: {
        "signature_style": "Handwoven textiles with traditional patterns",
        "target_audience": "Fashion conscious buyers and home decorators",
        "suggested_platforms": ["instagram", "pinterest", "facebook"],
        "common_hashtags": ["#handloom", "#textiles", "#weaving", "#sustainable"]
    },
    CraftType.JEWELRY: {
        "signature_style": "Traditional silver jewelry with contemporary appeal",
        "target_audience": "Fashion enthusiasts and jewelry collectors",
        "suggested_platforms": ["instagram", "facebook", "pinterest"],
        "common_hashtags": ["#handmadejewelry", "#silverjewelry", "#artisan"]
    },
    CraftType.WOODWORK: {
        "signature_style": "Handcrafted wooden furniture and decorative items",
        "target_audience": "Home furniture buyers and art collectors",
        "suggested_platforms": ["instagram", "youtube", "facebook"],
        "common_hashtags": ["#woodworking", "#furniture", "#handcarved"]
    }
}

def get_profile_template(craft_type: CraftType) -> Dict:
    """Get profile template for specific craft type"""
    return CRAFT_PROFILE_TEMPLATES.get(craft_type, {})

if __name__ == "__main__":
    # Test the profile manager
    pm = ProfileManager()
    print(f"👤 Profile Manager initialized with {len(pm.profiles)} profiles")