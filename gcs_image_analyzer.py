"""
Google Cloud Storage Image Analysis Module for Craft Identification
Integrates with GCS for image storage and Gemini multimodal for analysis
"""

import os
import io
import uuid
from datetime import datetime
from typing import Dict, List, Optional, BinaryIO
import logging
from google.cloud import storage
from google.cloud.storage import Blob
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from dotenv import load_dotenv
import json

from artisan_ai_agent import CraftAnalysis, CraftType
from profile_manager import ProfileManager

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class GCSCraftImageAnalyzer:
    """AI-powered image analyzer with Google Cloud Storage integration"""
    
    def __init__(self):
        # Initialize Vertex AI
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID', 'your-project-id')
        self.bucket_name = os.getenv('GCS_BUCKET_NAME', 'artisan-craft-images')
        self.location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us (multiple regions in United States)')
        
        try:
            vertexai.init(project=self.project_id, location=self.location)
            self.model = GenerativeModel("gemini-1.5-pro")
            logger.info("Vertex AI initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Vertex AI: {e}")
            raise
        
        # Initialize GCS client
        try:
            self.storage_client = storage.Client(project=self.project_id)
            self.bucket = self.storage_client.bucket(self.bucket_name)
            logger.info(f"GCS client initialized for bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"Error initializing GCS client: {e}")
            raise
        
        # Initialize profile manager for enhanced analysis
        self.profile_manager = ProfileManager()
        
        # Traditional Indian craft knowledge base
        self.craft_characteristics = {
            CraftType.POTTERY: {
                "materials": ["clay", "terracotta", "ceramic", "earthenware"],
                "colors": ["earth tones", "brown", "red", "orange", "black"],
                "patterns": ["geometric", "floral", "tribal", "mandala"],
                "styles": ["traditional", "contemporary", "rustic", "glazed"]
            },
            CraftType.TEXTILES: {
                "materials": ["cotton", "silk", "wool", "hemp", "jute"],
                "colors": ["vibrant", "natural dyes", "indigo", "red", "yellow"],
                "patterns": ["ikat", "block print", "embroidered", "woven"],
                "styles": ["traditional", "contemporary", "ethnic", "modern"]
            },
            CraftType.JEWELRY: {
                "materials": ["gold", "silver", "copper", "brass", "beads", "stones"],
                "colors": ["metallic", "colorful beads", "precious stones"],
                "patterns": ["intricate", "filigree", "engraved", "studded"],
                "styles": ["traditional", "contemporary", "tribal", "royal"]
            },
            CraftType.WOODWORK: {
                "materials": ["teak", "rosewood", "sandalwood", "bamboo"],
                "colors": ["natural wood", "brown", "carved"],
                "patterns": ["carved", "inlay", "geometric", "floral"],
                "styles": ["traditional", "contemporary", "rustic", "polished"]
            }
        }
    
    def upload_image_to_gcs(self, image_file: BinaryIO, profile_id: str) -> str:
        """
        Upload image to Google Cloud Storage and return GCS URI
        """
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = image_file.name.split('.')[-1].lower()
            filename = f"{profile_id}/{timestamp}_{uuid.uuid4().hex[:8]}.{file_extension}"
            
            # Create blob and upload
            blob = self.bucket.blob(filename)
            
            # Reset file pointer
            image_file.seek(0)
            
            # Upload file
            blob.upload_from_file(image_file, content_type=f"image/{file_extension}")
            
            # Make blob publicly readable (optional, depending on your security needs)
            # blob.make_public()
            
            # Return GCS URI
            gcs_uri = f"gs://{self.bucket_name}/{filename}"
            logger.info(f"Image uploaded to GCS: {gcs_uri}")
            
            return gcs_uri
            
        except Exception as e:
            logger.error(f"Error uploading image to GCS: {e}")
            raise
    
    def analyze_craft_image_from_gcs(self, gcs_uri: str, profile_id: str) -> CraftAnalysis:
        """
        Analyze craft image from GCS URI using Gemini multimodal
        """
        try:
            # Get artisan profile for context
            profile = self.profile_manager.get_profile(profile_id)
            profile_context = ""
            if profile:
                profile_context = f"""
                Artisan Context:
                - Name: {profile.name}
                - Specialization: {profile.specialization.value}
                - Experience: {profile.experience_years} years
                - Location: {profile.location}
                - Style: {profile.signature_style}
                """
            
            # Create analysis prompt for Indian crafts
            analysis_prompt = f"""
            Analyze this Indian craft image and provide detailed information in JSON format.
            
            {profile_context}
            
            Please analyze the image and return a JSON response with the following structure:
            {{
                "colors": ["list of dominant colors detected"],
                "patterns": ["list of visible patterns like geometric, floral, tribal, etc."],
                "materials": ["identified materials like clay, wood, metal, fabric, etc."],
                "style": "overall style description",
                "craft_type": "pottery/textiles/jewelry/woodwork/metalwork/painting/embroidery/leather/bamboo/stonework/glasswork",
                "complexity_level": "beginner/intermediate/advanced/master",
                "estimated_time": "estimated creation time",
                "cultural_significance": "brief description of cultural context",
                "confidence_score": 0.95,
                "techniques_observed": ["specific techniques visible in the craft"],
                "market_appeal": "assessment of commercial viability",
                "improvement_suggestions": ["suggestions for enhancement"],
                "content_angles": ["suggested content creation angles"]
            }}
            
            Focus on traditional Indian craft characteristics and provide accurate identification.
            Consider the artisan's specialization and experience level in your analysis.
            """
            
            # Create image part from GCS URI
            image_part = Part.from_uri(gcs_uri, mime_type="image/jpeg")
            
            # Generate content using Gemini multimodal
            response = self.model.generate_content([analysis_prompt, image_part])
            
            # Parse the response
            response_text = response.text
            logger.info(f"Gemini analysis response received")
            
            # Extract JSON from response
            try:
                # Find JSON in the response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                json_str = response_text[start_idx:end_idx]
                analysis_data = json.loads(json_str)
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Failed to parse JSON response: {e}")
                # Fallback to manual parsing or default values
                analysis_data = self._create_fallback_analysis(response_text, profile)
            
            # Create CraftAnalysis object
            craft_analysis = CraftAnalysis(
                colors=analysis_data.get('colors', ['unknown']),
                patterns=analysis_data.get('patterns', ['unknown']),
                materials=analysis_data.get('materials', ['unknown']),
                style=analysis_data.get('style', 'traditional'),
                craft_type=self._determine_craft_type(analysis_data.get('craft_type', 'unknown')),
                complexity_level=analysis_data.get('complexity_level', 'intermediate'),
                estimated_time=analysis_data.get('estimated_time', '2-4 hours'),
                confidence_score=float(analysis_data.get('confidence_score', 0.8))
            )
            
            # Store additional analysis data for enhanced recommendations
            craft_analysis.cultural_significance = analysis_data.get('cultural_significance', '')
            craft_analysis.techniques_observed = analysis_data.get('techniques_observed', [])
            craft_analysis.market_appeal = analysis_data.get('market_appeal', '')
            craft_analysis.improvement_suggestions = analysis_data.get('improvement_suggestions', [])
            craft_analysis.content_angles = analysis_data.get('content_angles', [])
            
            logger.info(f"Successfully analyzed craft image: {craft_analysis.craft_type}")
            return craft_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing craft image from GCS: {e}")
            # Return default analysis
            return self._create_default_analysis(profile)
    
    def analyze_uploaded_image(self, uploaded_file: BinaryIO, profile_id: str) -> Dict:
        """
        Complete workflow: Upload image to GCS and analyze with recommendations
        """
        try:
            logger.info(f"Starting image analysis workflow for profile {profile_id}")
            
            # Upload image to GCS
            gcs_uri = self.upload_image_to_gcs(uploaded_file, profile_id)
            
            # Analyze image
            craft_analysis = self.analyze_craft_image_from_gcs(gcs_uri, profile_id)
            
            # Get insights
            insights = self.get_craft_insights(craft_analysis)
            
            # Generate content recommendations (import here to avoid circular imports)
            from content_strategist import ContentStrategist
            from specialized_recommendations import SpecializedRecommendationEngine
            
            content_strategist = ContentStrategist()
            specialized_engine = SpecializedRecommendationEngine()
            
            profile = self.profile_manager.get_profile(profile_id)
            if profile:
                general_recommendations = content_strategist.generate_content_strategy(profile, craft_analysis)
                specialized_recommendations = specialized_engine.get_specialized_recommendations(profile, craft_analysis)
            else:
                general_recommendations = []
                specialized_recommendations = []
            
            result = {
                'gcs_uri': gcs_uri,
                'analysis': {
                    'colors': craft_analysis.colors,
                    'patterns': craft_analysis.patterns,
                    'materials': craft_analysis.materials,
                    'style': craft_analysis.style,
                    'craft_type': craft_analysis.craft_type.value,
                    'complexity_level': craft_analysis.complexity_level,
                    'estimated_time': craft_analysis.estimated_time,
                    'confidence_score': craft_analysis.confidence_score,
                    'cultural_significance': getattr(craft_analysis, 'cultural_significance', ''),
                    'techniques_observed': getattr(craft_analysis, 'techniques_observed', []),
                    'market_appeal': getattr(craft_analysis, 'market_appeal', ''),
                    'improvement_suggestions': getattr(craft_analysis, 'improvement_suggestions', []),
                    'content_angles': getattr(craft_analysis, 'content_angles', [])
                },
                'insights': insights,
                'content_recommendations': {
                    'general': [self._recommendation_to_dict(rec) for rec in general_recommendations],
                    'specialized': [self._recommendation_to_dict(rec) for rec in specialized_recommendations]
                }
            }
            
            logger.info("Image analysis workflow completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error in image analysis workflow: {e}")
            raise
    
    def _determine_craft_type(self, craft_type_str: str) -> CraftType:
        """Convert string to CraftType enum"""
        try:
            return CraftType(craft_type_str.lower())
        except ValueError:
            return CraftType.UNKNOWN
    
    def _create_fallback_analysis(self, response_text: str, profile) -> Dict:
        """Create fallback analysis when JSON parsing fails"""
        craft_type = profile.specialization.value if profile else "unknown"
        return {
            'colors': ['traditional'],
            'patterns': ['handcrafted'],
            'materials': ['natural'],
            'style': 'traditional Indian craft',
            'craft_type': craft_type,
            'complexity_level': 'intermediate',
            'estimated_time': '2-4 hours',
            'confidence_score': 0.6,
            'cultural_significance': 'Traditional Indian handicraft',
            'techniques_observed': ['handmade'],
            'market_appeal': 'Good market potential',
            'improvement_suggestions': ['Continue refining technique'],
            'content_angles': ['Process video', 'Cultural story']
        }
    
    def _create_default_analysis(self, profile) -> CraftAnalysis:
        """Create default analysis when all else fails"""
        craft_type = profile.specialization if profile else CraftType.UNKNOWN
        
        return CraftAnalysis(
            colors=['traditional'],
            patterns=['handcrafted'],
            materials=['natural'],
            style='traditional Indian craft',
            craft_type=craft_type,
            complexity_level='intermediate',
            estimated_time='2-4 hours',
            confidence_score=0.5
        )
    
    def get_craft_insights(self, analysis: CraftAnalysis) -> Dict[str, str]:
        """Generate insights based on craft analysis"""
        insights = {
            "market_appeal": self._assess_market_appeal(analysis),
            "target_audience": self._identify_target_audience(analysis),
            "seasonal_relevance": self._check_seasonal_relevance(analysis),
            "uniqueness_factor": self._evaluate_uniqueness(analysis),
            "content_potential": self._assess_content_potential(analysis)
        }
        return insights
    
    def _assess_market_appeal(self, analysis: CraftAnalysis) -> str:
        """Assess market appeal based on craft characteristics"""
        if analysis.complexity_level == "master":
            return "High premium market appeal - perfect for luxury collections"
        elif analysis.complexity_level == "advanced":
            return "Strong market appeal - suitable for mid to high-end market"
        else:
            return "Good market appeal - accessible to broad audience"
    
    def _identify_target_audience(self, analysis: CraftAnalysis) -> str:
        """Identify target audience based on craft analysis"""
        audiences = {
            CraftType.JEWELRY: "Fashion enthusiasts, gift buyers, collectors",
            CraftType.TEXTILES: "Home decor enthusiasts, fashion lovers, cultural appreciators",
            CraftType.POTTERY: "Home decor buyers, art collectors, functional pottery users",
            CraftType.WOODWORK: "Furniture buyers, art collectors, home decorators"
        }
        return audiences.get(analysis.craft_type, "Art enthusiasts and cultural appreciators")
    
    def _check_seasonal_relevance(self, analysis: CraftAnalysis) -> str:
        """Check seasonal relevance for marketing"""
        if "festival" in analysis.style.lower():
            return "Perfect for festival seasons and celebrations"
        elif analysis.craft_type == CraftType.TEXTILES:
            return "Year-round appeal with seasonal color variations"
        else:
            return "Consistent year-round appeal"
    
    def _evaluate_uniqueness(self, analysis: CraftAnalysis) -> str:
        """Evaluate uniqueness factor"""
        if analysis.confidence_score > 0.9:
            return "Highly distinctive craft with clear traditional elements"
        elif analysis.confidence_score > 0.7:
            return "Good uniqueness with recognizable craft characteristics"
        else:
            return "Unique handmade appeal with artistic value"
    
    def _assess_content_potential(self, analysis: CraftAnalysis) -> str:
        """Assess content creation potential"""
        if analysis.complexity_level in ["advanced", "master"]:
            return "Excellent content potential - complex process showcases expertise"
        else:
            return "Good content potential - educational and inspiring for audience"
    
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
    
    def delete_image_from_gcs(self, gcs_uri: str) -> bool:
        """Delete image from GCS"""
        try:
            # Extract blob name from GCS URI
            blob_name = gcs_uri.replace(f"gs://{self.bucket_name}/", "")
            blob = self.bucket.blob(blob_name)
            blob.delete()
            
            logger.info(f"Image deleted from GCS: {gcs_uri}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting image from GCS: {e}")
            return False
    
    def list_profile_images(self, profile_id: str) -> List[str]:
        """List all images for a specific profile"""
        try:
            prefix = f"{profile_id}/"
            blobs = self.storage_client.list_blobs(self.bucket, prefix=prefix)
            
            gcs_uris = []
            for blob in blobs:
                gcs_uri = f"gs://{self.bucket_name}/{blob.name}"
                gcs_uris.append(gcs_uri)
            
            return gcs_uris
            
        except Exception as e:
            logger.error(f"Error listing profile images: {e}")
            return []

if __name__ == "__main__":
    # Test the GCS image analyzer
    analyzer = GCSCraftImageAnalyzer()
    print("🔍 GCS Craft Image Analyzer initialized successfully")