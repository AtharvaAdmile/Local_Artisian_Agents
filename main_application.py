#!/usr/bin/env python3
"""
Main Application Interface for A2A AI Agent
Local Artisan Content Strategist System for India

This is the main entry point that integrates all components:
- Profile Management
- Image Analysis
- Content Strategy
- Specialized Recommendations
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional, List, Dict
import json

# Import all modules
from artisan_ai_agent import ArtisanAIAgent, ArtisanProfile, CraftType, ContentType
from profile_manager import ProfileManager, get_profile_template
from image_analyzer import CraftImageAnalyzer
from content_strategist import ContentStrategist
from specialized_recommendations import SpecializedRecommendationEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('artisan_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ArtisanContentManager:
    """Main application class that coordinates all AI agent functionality"""
    
    def __init__(self):
        """Initialize all components"""
        try:
            print("🎨 Initializing Artisan AI Agent System...")
            
            # Initialize core components
            self.profile_manager = ProfileManager()
            self.image_analyzer = CraftImageAnalyzer()
            self.content_strategist = ContentStrategist()
            self.specialized_engine = SpecializedRecommendationEngine()
            
            print("✅ All components initialized successfully!")
            print(f"📊 System loaded with {len(self.profile_manager.profiles)} artisan profiles")
            
        except Exception as e:
            logger.error(f"Error initializing system: {e}")
            raise
    
    def create_artisan_profile(self, 
                              name: str,
                              location: str,
                              specialization: str,
                              experience_years: int,
                              signature_style: str = None,
                              target_audience: str = None,
                              social_media_platforms: List[str] = None) -> str:
        """Create a new artisan profile with guided setup"""
        try:
            # Validate and convert specialization
            craft_type = CraftType(specialization.lower())
            
            # Get template defaults if not provided
            template = get_profile_template(craft_type)
            
            if signature_style is None:
                signature_style = template.get('signature_style', f'Traditional {specialization} with modern appeal')
            
            if target_audience is None:
                target_audience = template.get('target_audience', 'Art enthusiasts and cultural appreciators')
            
            if social_media_platforms is None:
                social_media_platforms = template.get('suggested_platforms', ['instagram', 'facebook'])
            
            # Create profile
            profile_id = self.profile_manager.create_profile(
                name=name,
                location=location,
                specialization=craft_type,
                experience_years=experience_years,
                signature_style=signature_style,
                target_audience=target_audience,
                social_media_platforms=social_media_platforms
            )
            
            print(f"✅ Created profile for {name} (ID: {profile_id})")
            print(f"📝 Specialization: {specialization}")
            print(f"🎯 Target Audience: {target_audience}")
            print(f"📱 Platforms: {', '.join(social_media_platforms)}")
            
            return profile_id
            
        except ValueError as e:
            valid_crafts = [craft.value for craft in CraftType]
            print(f"❌ Invalid specialization '{specialization}'")
            print(f"Valid options: {', '.join(valid_crafts)}")
            raise
        except Exception as e:
            logger.error(f"Error creating profile: {e}")
            raise
    
    def analyze_craft_image(self, profile_id: str, image_path: str) -> Dict:
        """Analyze craft image and generate content recommendations"""
        try:
            print(f"🔍 Analyzing craft image: {image_path}")
            
            # Get artisan profile
            profile = self.profile_manager.get_profile(profile_id)
            if not profile:
                raise ValueError(f"Profile {profile_id} not found")
            
            # Analyze image
            craft_analysis = self.image_analyzer.analyze_craft_image(image_path)
            
            # Get insights
            insights = self.image_analyzer.get_craft_insights(craft_analysis)
            
            # Generate content recommendations based on analysis
            general_recommendations = self.content_strategist.generate_content_strategy(profile, craft_analysis)
            specialized_recommendations = self.specialized_engine.get_specialized_recommendations(profile, craft_analysis)
            
            result = {
                'analysis': {
                    'colors': craft_analysis.colors,
                    'patterns': craft_analysis.patterns,
                    'materials': craft_analysis.materials,
                    'style': craft_analysis.style,
                    'craft_type': craft_analysis.craft_type.value,
                    'complexity_level': craft_analysis.complexity_level,
                    'estimated_time': craft_analysis.estimated_time,
                    'confidence_score': craft_analysis.confidence_score
                },
                'insights': insights,
                'content_recommendations': {
                    'general': [self._recommendation_to_dict(rec) for rec in general_recommendations],
                    'specialized': [self._recommendation_to_dict(rec) for rec in specialized_recommendations]
                }
            }
            
            print("✅ Image analysis completed!")
            print(f"🎨 Detected: {craft_analysis.craft_type.value.title()} ({craft_analysis.complexity_level} level)")
            print(f"🎯 Generated {len(general_recommendations)} general + {len(specialized_recommendations)} specialized recommendations")
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing craft image: {e}")
            raise
    
    def get_content_strategy(self, profile_id: str) -> Dict:
        """Get comprehensive content strategy for an artisan"""
        try:
            profile = self.profile_manager.get_profile(profile_id)
            if not profile:
                raise ValueError(f"Profile {profile_id} not found")
            
            print(f"📋 Generating content strategy for {profile.name}...")
            
            # Generate various types of recommendations
            general_strategy = self.content_strategist.generate_content_strategy(profile)
            specialized_strategy = self.specialized_engine.get_specialized_recommendations(profile)
            seasonal_strategy = self.specialized_engine.get_seasonal_craft_recommendations(profile)
            content_calendar = self.content_strategist.generate_content_calendar(profile, days=7)
            
            strategy = {
                'artisan_info': {
                    'name': profile.name,
                    'specialization': profile.specialization.value,
                    'experience_years': profile.experience_years,
                    'location': profile.location,
                    'target_audience': profile.target_audience
                },
                'recommendations': {
                    'general': [self._recommendation_to_dict(rec) for rec in general_strategy],
                    'specialized': [self._recommendation_to_dict(rec) for rec in specialized_strategy],
                    'seasonal': [self._recommendation_to_dict(rec) for rec in seasonal_strategy]
                },
                'content_calendar': {
                    date: [self._recommendation_to_dict(rec) for rec in recs] 
                    for date, recs in content_calendar.items()
                }
            }
            
            print("✅ Content strategy generated!")
            print(f"📊 {len(general_strategy)} general recommendations")
            print(f"🎯 {len(specialized_strategy)} specialized recommendations")
            print(f"🗓️ 7-day content calendar created")
            
            return strategy
            
        except Exception as e:
            logger.error(f"Error generating content strategy: {e}")
            raise
    
    def get_technique_recommendations(self, profile_id: str, technique: str) -> List[Dict]:
        """Get recommendations for specific technique content"""
        try:
            profile = self.profile_manager.get_profile(profile_id)
            if not profile:
                raise ValueError(f"Profile {profile_id} not found")
            
            recommendations = self.specialized_engine.get_technique_recommendations(profile, technique)
            
            print(f"🎯 Generated {len(recommendations)} recommendations for {technique} technique")
            
            return [self._recommendation_to_dict(rec) for rec in recommendations]
            
        except Exception as e:
            logger.error(f"Error getting technique recommendations: {e}")
            raise
    
    def get_market_recommendations(self, profile_id: str, target_market: str) -> List[Dict]:
        """Get recommendations for specific target market"""
        try:
            profile = self.profile_manager.get_profile(profile_id)
            if not profile:
                raise ValueError(f"Profile {profile_id} not found")
            
            recommendations = self.specialized_engine.get_market_specific_recommendations(profile, target_market)
            
            print(f"🎯 Generated {len(recommendations)} recommendations for {target_market} market")
            
            return [self._recommendation_to_dict(rec) for rec in recommendations]
            
        except Exception as e:
            logger.error(f"Error getting market recommendations: {e}")
            raise
    
    def list_artisan_profiles(self) -> List[Dict]:
        """List all artisan profiles"""
        return self.profile_manager.list_profiles()
    
    def get_craft_statistics(self) -> Dict:
        """Get statistics about registered artisans"""
        craft_stats = self.profile_manager.get_craft_statistics()
        experience_dist = self.profile_manager.get_experience_distribution()
        
        return {
            'total_artisans': len(self.profile_manager.profiles),
            'craft_distribution': craft_stats,
            'experience_distribution': experience_dist
        }
    
    def _recommendation_to_dict(self, recommendation) -> Dict:
        """Convert recommendation object to dictionary"""
        return {
            'content_type': recommendation.content_type.value,
            'title_suggestion': recommendation.title_suggestion,
            'description': recommendation.description,
            'best_time_to_post': recommendation.best_time_to_post,
            'hashtags': recommendation.hashtags,
            'target_platforms': recommendation.target_platforms,
            'priority_score': recommendation.priority_score,
            'reasoning': recommendation.reasoning
        }
    
    def export_profile_data(self, profile_id: str, export_path: str = None) -> str:
        """Export complete profile data including recommendations"""
        try:
            profile = self.profile_manager.get_profile(profile_id)
            if not profile:
                raise ValueError(f"Profile {profile_id} not found")
            
            # Generate complete strategy
            strategy = self.get_content_strategy(profile_id)
            
            # Prepare export data
            export_data = {
                'export_date': datetime.now().isoformat(),
                'profile_id': profile_id,
                'strategy': strategy
            }
            
            # Set export path
            if export_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                export_path = f"{profile.name.replace(' ', '_')}_strategy_{timestamp}.json"
            
            # Save export
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Profile data exported to: {export_path}")
            return export_path
            
        except Exception as e:
            logger.error(f"Error exporting profile data: {e}")
            raise

def main():
    """Main application entry point with interactive menu"""
    try:
        # Initialize system
        app = ArtisanContentManager()
        
        while True:
            print("\n" + "="*60)
            print("🎨 ARTISAN AI AGENT - CONTENT STRATEGIST")
            print("="*60)
            print("1. Create New Artisan Profile")
            print("2. List All Profiles")
            print("3. Analyze Craft Image")
            print("4. Get Content Strategy")
            print("5. Get Technique Recommendations")
            print("6. Get Market Recommendations")
            print("7. Export Profile Data")
            print("8. View Statistics")
            print("0. Exit")
            print("-"*60)
            
            choice = input("Select an option (0-8): ").strip()
            
            if choice == "0":
                print("👋 Thank you for using Artisan AI Agent!")
                break
            elif choice == "1":
                create_profile_interactive(app)
            elif choice == "2":
                list_profiles_interactive(app)
            elif choice == "3":
                analyze_image_interactive(app)
            elif choice == "4":
                get_strategy_interactive(app)
            elif choice == "5":
                get_technique_recommendations_interactive(app)
            elif choice == "6":
                get_market_recommendations_interactive(app)
            elif choice == "7":
                export_data_interactive(app)
            elif choice == "8":
                show_statistics_interactive(app)
            else:
                print("❌ Invalid option. Please try again.")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"❌ An error occurred: {e}")

def create_profile_interactive(app):
    """Interactive profile creation"""
    print("\n📝 Creating New Artisan Profile")
    print("-" * 40)
    
    name = input("Artisan Name: ").strip()
    location = input("Location: ").strip()
    
    print("\nAvailable Craft Types:")
    for i, craft in enumerate(CraftType):
        if craft != CraftType.UNKNOWN:
            print(f"{i+1}. {craft.value.title()}")
    
    craft_choice = input("Select craft type (1-10): ").strip()
    try:
        craft_index = int(craft_choice) - 1
        craft_types = [c for c in CraftType if c != CraftType.UNKNOWN]
        specialization = craft_types[craft_index].value
    except (ValueError, IndexError):
        print("❌ Invalid craft type selection")
        return
    
    try:
        experience_years = int(input("Years of experience: ").strip())
    except ValueError:
        print("❌ Invalid experience years")
        return
    
    # Optional fields
    signature_style = input("Signature style (optional): ").strip() or None
    target_audience = input("Target audience (optional): ").strip() or None
    
    platforms_input = input("Social media platforms (comma-separated, optional): ").strip()
    platforms = [p.strip() for p in platforms_input.split(",")] if platforms_input else None
    
    try:
        profile_id = app.create_artisan_profile(
            name=name,
            location=location,
            specialization=specialization,
            experience_years=experience_years,
            signature_style=signature_style,
            target_audience=target_audience,
            social_media_platforms=platforms
        )
        print(f"\n✅ Profile created successfully! ID: {profile_id}")
    except Exception as e:
        print(f"❌ Error creating profile: {e}")

def list_profiles_interactive(app):
    """Interactive profile listing"""
    profiles = app.list_artisan_profiles()
    
    if not profiles:
        print("\n📭 No artisan profiles found.")
        return
    
    print(f"\n👥 Registered Artisans ({len(profiles)})")
    print("-" * 60)
    
    for profile in profiles:
        print(f"ID: {profile['id']}")
        print(f"Name: {profile['name']}")
        print(f"Location: {profile['location']}")
        print(f"Craft: {profile['specialization'].title()}")
        print(f"Experience: {profile['experience_years']} years")
        print(f"Created: {profile['created_at'][:10]}")
        print("-" * 40)

def analyze_image_interactive(app):
    """Interactive image analysis"""
    profiles = app.list_artisan_profiles()
    
    if not profiles:
        print("\n📭 No artisan profiles found. Create a profile first.")
        return
    
    print("\n🔍 Craft Image Analysis")
    print("-" * 40)
    
    # Show profiles
    for i, profile in enumerate(profiles):
        print(f"{i+1}. {profile['name']} ({profile['specialization']})")
    
    try:
        profile_choice = int(input("Select artisan profile (number): ").strip()) - 1
        profile_id = profiles[profile_choice]['id']
    except (ValueError, IndexError):
        print("❌ Invalid profile selection")
        return
    
    image_path = input("Enter image file path: ").strip()
    
    if not os.path.exists(image_path):
        print("❌ Image file not found")
        return
    
    try:
        result = app.analyze_craft_image(profile_id, image_path)
        
        print("\n📊 Analysis Results:")
        print(f"Craft Type: {result['analysis']['craft_type'].title()}")
        print(f"Complexity: {result['analysis']['complexity_level'].title()}")
        print(f"Colors: {', '.join(result['analysis']['colors'])}")
        print(f"Materials: {', '.join(result['analysis']['materials'])}")
        print(f"Confidence: {result['analysis']['confidence_score']:.2f}")
        
        print(f"\n💡 Generated {len(result['content_recommendations']['general'])} general recommendations")
        print(f"🎯 Generated {len(result['content_recommendations']['specialized'])} specialized recommendations")
        
    except Exception as e:
        print(f"❌ Error analyzing image: {e}")

def get_strategy_interactive(app):
    """Interactive content strategy generation"""
    profiles = app.list_artisan_profiles()
    
    if not profiles:
        print("\n📭 No artisan profiles found. Create a profile first.")
        return
    
    print("\n📋 Content Strategy Generation")
    print("-" * 40)
    
    # Show profiles
    for i, profile in enumerate(profiles):
        print(f"{i+1}. {profile['name']} ({profile['specialization']})")
    
    try:
        profile_choice = int(input("Select artisan profile (number): ").strip()) - 1
        profile_id = profiles[profile_choice]['id']
    except (ValueError, IndexError):
        print("❌ Invalid profile selection")
        return
    
    try:
        strategy = app.get_content_strategy(profile_id)
        
        print(f"\n📊 Content Strategy for {strategy['artisan_info']['name']}")
        print(f"Specialization: {strategy['artisan_info']['specialization'].title()}")
        print(f"Experience: {strategy['artisan_info']['experience_years']} years")
        
        print(f"\n📝 Recommendations Summary:")
        print(f"General: {len(strategy['recommendations']['general'])}")
        print(f"Specialized: {len(strategy['recommendations']['specialized'])}")
        print(f"Seasonal: {len(strategy['recommendations']['seasonal'])}")
        
        # Show top recommendations
        if strategy['recommendations']['general']:
            print(f"\n🔝 Top Recommendation:")
            top_rec = strategy['recommendations']['general'][0]
            print(f"Title: {top_rec['title_suggestion']}")
            print(f"Type: {top_rec['content_type'].title()}")
            print(f"Priority: {top_rec['priority_score']:.2f}")
            print(f"Reasoning: {top_rec['reasoning']}")
    
    except Exception as e:
        print(f"❌ Error generating strategy: {e}")

def get_technique_recommendations_interactive(app):
    """Interactive technique recommendations"""
    profiles = app.list_artisan_profiles()
    
    if not profiles:
        print("\n📭 No artisan profiles found. Create a profile first.")
        return
    
    print("\n🎯 Technique-Specific Recommendations")
    print("-" * 40)
    
    # Show profiles
    for i, profile in enumerate(profiles):
        print(f"{i+1}. {profile['name']} ({profile['specialization']})")
    
    try:
        profile_choice = int(input("Select artisan profile (number): ").strip()) - 1
        profile_id = profiles[profile_choice]['id']
    except (ValueError, IndexError):
        print("❌ Invalid profile selection")
        return
    
    technique = input("Enter technique name: ").strip()
    
    try:
        recommendations = app.get_technique_recommendations(profile_id, technique)
        
        if recommendations:
            for rec in recommendations:
                print(f"\n📝 {rec['title_suggestion']}")
                print(f"Description: {rec['description']}")
                print(f"Priority: {rec['priority_score']:.2f}")
        else:
            print("❌ No recommendations found for this technique")
    
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")

def get_market_recommendations_interactive(app):
    """Interactive market recommendations"""
    profiles = app.list_artisan_profiles()
    
    if not profiles:
        print("\n📭 No artisan profiles found. Create a profile first.")
        return
    
    print("\n🏪 Market-Specific Recommendations")
    print("-" * 40)
    
    # Show profiles
    for i, profile in enumerate(profiles):
        print(f"{i+1}. {profile['name']} ({profile['specialization']})")
    
    try:
        profile_choice = int(input("Select artisan profile (number): ").strip()) - 1
        profile_id = profiles[profile_choice]['id']
    except (ValueError, IndexError):
        print("❌ Invalid profile selection")
        return
    
    print("\nCommon Markets:")
    print("1. home decor")
    print("2. fashion") 
    print("3. art collectors")
    print("4. functional pottery")
    print("5. custom/other")
    
    market = input("Enter target market: ").strip()
    
    try:
        recommendations = app.get_market_recommendations(profile_id, market)
        
        if recommendations:
            for rec in recommendations:
                print(f"\n📝 {rec['title_suggestion']}")
                print(f"Description: {rec['description']}")
                print(f"Priority: {rec['priority_score']:.2f}")
        else:
            print("❌ No recommendations found for this market")
    
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")

def export_data_interactive(app):
    """Interactive data export"""
    profiles = app.list_artisan_profiles()
    
    if not profiles:
        print("\n📭 No artisan profiles found. Create a profile first.")
        return
    
    print("\n💾 Export Profile Data")
    print("-" * 40)
    
    # Show profiles
    for i, profile in enumerate(profiles):
        print(f"{i+1}. {profile['name']} ({profile['specialization']})")
    
    try:
        profile_choice = int(input("Select artisan profile (number): ").strip()) - 1
        profile_id = profiles[profile_choice]['id']
    except (ValueError, IndexError):
        print("❌ Invalid profile selection")
        return
    
    export_path = input("Export file path (optional): ").strip() or None
    
    try:
        exported_file = app.export_profile_data(profile_id, export_path)
        print(f"✅ Data exported successfully to: {exported_file}")
    except Exception as e:
        print(f"❌ Error exporting data: {e}")

def show_statistics_interactive(app):
    """Show system statistics"""
    try:
        stats = app.get_craft_statistics()
        
        print("\n📊 System Statistics")
        print("-" * 40)
        print(f"Total Artisans: {stats['total_artisans']}")
        
        print("\nCraft Distribution:")
        for craft, count in stats['craft_distribution'].items():
            print(f"  {craft.title()}: {count}")
        
        print("\nExperience Distribution:")
        for level, count in stats['experience_distribution'].items():
            print(f"  {level}: {count}")
    
    except Exception as e:
        print(f"❌ Error showing statistics: {e}")

if __name__ == "__main__":
    main()