"""
Image Analysis Module for Craft Identification
Analyzes uploaded craft images to identify colors, patterns, materials, and style
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import HttpOptions
import base64
from typing import Dict, List, Tuple
import json
import logging
from artisan_ai_agent import CraftAnalysis, CraftType

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class CraftImageAnalyzer:
    """AI-powered image analyzer for craft identification"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.client = genai.Client(
            api_key=self.api_key, 
            http_options=HttpOptions(api_version="v1")
        )
        
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
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Error encoding image: {e}")
            return None
    
    def analyze_craft_image(self, image_path: str) -> CraftAnalysis:
        """
        Analyze craft image using AI to identify characteristics
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Create analysis prompt for Indian crafts
            analysis_prompt = """
            Analyze this Indian craft image and provide detailed information in JSON format:
            
            {
                "colors": ["list of dominant colors"],
                "patterns": ["list of visible patterns like geometric, floral, tribal, etc."],
                "materials": ["identified materials like clay, wood, metal, fabric, etc."],
                "style": "overall style description",
                "craft_type": "pottery/textiles/jewelry/woodwork/metalwork/painting/embroidery/leather/bamboo/stonework/glasswork",
                "complexity_level": "beginner/intermediate/advanced/master",
                "estimated_time": "estimated creation time",
                "cultural_significance": "brief description of cultural context",
                "confidence_score": 0.95
            }
            
            Focus on traditional Indian craft characteristics and provide accurate identification.
            """
            
            # Use Google's Gemini for image analysis
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[
                    analysis_prompt,
                    {
                        "mime_type": "image/jpeg",
                        "data": image_data
                    }
                ]
            )
            
            # Parse the response
            response_text = response.text
            logger.info(f"AI Analysis Response: {response_text}")
            
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
                analysis_data = self._create_fallback_analysis(response_text)
            
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
            
            logger.info(f"Successfully analyzed craft image: {craft_analysis.craft_type}")
            return craft_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing craft image: {e}")
            # Return default analysis
            return CraftAnalysis(
                colors=['unknown'],
                patterns=['traditional'],
                materials=['handmade'],
                style='traditional Indian craft',
                craft_type=CraftType.UNKNOWN,
                complexity_level='intermediate',
                estimated_time='2-4 hours',
                confidence_score=0.5
            )
    
    def _determine_craft_type(self, craft_type_str: str) -> CraftType:
        """Convert string to CraftType enum"""
        try:
            return CraftType(craft_type_str.lower())
        except ValueError:
            return CraftType.UNKNOWN
    
    def _create_fallback_analysis(self, response_text: str) -> Dict:
        """Create fallback analysis when JSON parsing fails"""
        return {
            'colors': ['traditional'],
            'patterns': ['handcrafted'],
            'materials': ['natural'],
            'style': 'traditional Indian craft',
            'craft_type': 'unknown',
            'complexity_level': 'intermediate',
            'estimated_time': '2-4 hours',
            'confidence_score': 0.6
        }
    
    def get_craft_insights(self, analysis: CraftAnalysis) -> Dict[str, str]:
        """Generate insights based on craft analysis"""
        insights = {
            "market_appeal": self._assess_market_appeal(analysis),
            "target_audience": self._identify_target_audience(analysis),
            "seasonal_relevance": self._check_seasonal_relevance(analysis),
            "uniqueness_factor": self._evaluate_uniqueness(analysis)
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
        if "festival" in analysis.style.lower() or "celebration" in analysis.style.lower():
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

if __name__ == "__main__":
    # Test the image analyzer
    analyzer = CraftImageAnalyzer()
    print("🔍 Craft Image Analyzer initialized successfully")