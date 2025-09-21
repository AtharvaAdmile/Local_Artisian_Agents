#!/usr/bin/env python3
"""
FastAPI Application for A2A AI Agent
Local Artisan Content Strategist System for India
Optimized for Render deployment
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging
import os
from datetime import datetime
import json

# Import modules
from artisan_ai_agent import ArtisanProfile, CraftType, ContentType
from profile_manager import ProfileManager
from gcs_image_analyzer import GCSCraftImageAnalyzer
from content_strategist import ContentStrategist
from specialized_recommendations import SpecializedRecommendationEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="A2A AI Agent - Artisan Content Strategist API",
    description="AI-powered content strategy API for local artisans in India",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global components
profile_manager = None
image_analyzer = None
content_strategist = None
specialized_engine = None

@app.on_event("startup")
async def startup_event():
    """Initialize system components on startup"""
    global profile_manager, image_analyzer, content_strategist, specialized_engine
    
    try:
        logger.info("Initializing A2A AI Agent system...")
        profile_manager = ProfileManager()
        
        # Try to initialize AI components, but continue if they fail
        try:
            image_analyzer = GCSCraftImageAnalyzer()
            logger.info("✅ Image analyzer initialized")
        except Exception as e:
            logger.warning(f"⚠️ Image analyzer failed to initialize: {e}")
            image_analyzer = None
        
        try:
            content_strategist = ContentStrategist()
            logger.info("✅ Content strategist initialized")
        except Exception as e:
            logger.warning(f"⚠️ Content strategist failed to initialize: {e}")
            content_strategist = None
        
        try:
            specialized_engine = SpecializedRecommendationEngine()
            logger.info("✅ Specialized engine initialized")
        except Exception as e:
            logger.warning(f"⚠️ Specialized engine failed to initialize: {e}")
            specialized_engine = None
        
        logger.info("✅ System initialized (some components may be unavailable without proper credentials)")
    except Exception as e:
        logger.error(f"❌ Failed to initialize system: {e}")
        raise

# Pydantic models for request/response
class ProfileCreateRequest(BaseModel):
    name: str = Field(..., description="Artisan name")
    location: str = Field(..., description="Location")
    specialization: str = Field(..., description="Craft specialization")
    experience_years: int = Field(..., ge=0, le=80, description="Years of experience")
    signature_style: Optional[str] = Field(None, description="Signature style")
    target_audience: Optional[str] = Field(None, description="Target audience")
    social_media_platforms: Optional[List[str]] = Field(default=["instagram", "facebook"], description="Social media platforms")

class ProfileResponse(BaseModel):
    id: str
    name: str
    location: str
    specialization: str
    experience_years: int
    created_at: str

class ContentRecommendationResponse(BaseModel):
    content_type: str
    title_suggestion: str
    description: str
    best_time_to_post: str
    hashtags: List[str]
    target_platforms: List[str]
    priority_score: float
    reasoning: str

class ImageAnalysisResponse(BaseModel):
    gcs_uri: str
    analysis: Dict[str, Any]
    insights: Dict[str, str]
    content_recommendations: Dict[str, List[Dict[str, Any]]]

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Render deployment"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🎨 A2A AI Agent - Artisan Content Strategist API",
        "description": "Empowering Local Artisans in India with AI-powered Content Strategy",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Dashboard endpoints
@app.get("/api/dashboard")
async def get_dashboard():
    """Get dashboard overview data"""
    try:
        profiles = profile_manager.list_profiles()
        craft_stats = profile_manager.get_craft_statistics()
        
        return {
            "total_artisans": len(profiles),
            "craft_types": len(craft_stats),
            "active_profiles": len(profiles),
            "system_status": "online",
            "craft_distribution": craft_stats,
            "recent_profiles": profiles[-3:] if profiles else []
        }
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Profile management endpoints
@app.post("/api/profiles", response_model=dict)
async def create_profile(profile_data: ProfileCreateRequest):
    """Create a new artisan profile"""
    try:
        # Convert specialization string to CraftType
        try:
            craft_type = CraftType(profile_data.specialization.lower())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid specialization: {profile_data.specialization}")
        
        profile_id = profile_manager.create_profile(
            name=profile_data.name,
            location=profile_data.location,
            specialization=craft_type,
            experience_years=profile_data.experience_years,
            signature_style=profile_data.signature_style,
            target_audience=profile_data.target_audience,
            social_media_platforms=profile_data.social_media_platforms
        )
        
        return {"profile_id": profile_id, "message": "Profile created successfully"}
        
    except Exception as e:
        logger.error(f"Error creating profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/profiles", response_model=List[ProfileResponse])
async def list_profiles():
    """List all artisan profiles"""
    try:
        profiles = profile_manager.list_profiles()
        return profiles
    except Exception as e:
        logger.error(f"Error listing profiles: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/profiles/{profile_id}")
async def get_profile(profile_id: str):
    """Get specific artisan profile"""
    try:
        profile = profile_manager.get_profile(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return {
            "id": profile_id,
            "name": profile.name,
            "location": profile.location,
            "specialization": profile.specialization.value,
            "experience_years": profile.experience_years,
            "signature_style": profile.signature_style,
            "target_audience": profile.target_audience,
            "social_media_platforms": profile.social_media_platforms,
            "created_at": profile.created_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/profiles/{profile_id}")
async def delete_profile(profile_id: str):
    """Delete artisan profile"""
    try:
        success = profile_manager.delete_profile(profile_id)
        if not success:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return {"message": "Profile deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Image analysis endpoints
@app.post("/api/analyze-image/{profile_id}")
async def analyze_image(profile_id: str, file: UploadFile = File(...)):
    """Analyze craft image and get recommendations"""
    try:
        if not image_analyzer:
            raise HTTPException(status_code=503, detail="Image analysis service unavailable - missing Google Cloud credentials")
        
        # Validate profile exists
        profile = profile_manager.get_profile(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Analyze image
        result = image_analyzer.analyze_uploaded_image(file.file, profile_id)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Content strategy endpoints
@app.get("/api/content-strategy/{profile_id}")
async def generate_content_strategy(profile_id: str):
    """Generate content strategy for artisan"""
    try:
        if not content_strategist:
            raise HTTPException(status_code=503, detail="Content strategy service unavailable - missing Google API credentials")
        
        profile = profile_manager.get_profile(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Generate general strategy
        general_strategy = content_strategist.generate_content_strategy(profile)
        
        # Convert to response format
        recommendations = []
        for rec in general_strategy[:5]:  # Limit to top 5
            recommendations.append({
                "content_type": rec.content_type.value,
                "title_suggestion": rec.title_suggestion,
                "description": rec.description,
                "best_time_to_post": rec.best_time_to_post,
                "hashtags": rec.hashtags,
                "target_platforms": rec.target_platforms,
                "priority_score": rec.priority_score,
                "reasoning": rec.reasoning
            })
        
        return {"recommendations": recommendations}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating content strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/specialized-recommendations/{profile_id}")
async def get_specialized_recommendations(profile_id: str):
    """Get specialized recommendations for artisan"""
    try:
        if not specialized_engine:
            raise HTTPException(status_code=503, detail="Specialized recommendations service unavailable - missing Google API credentials")
        
        profile = profile_manager.get_profile(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Generate specialized recommendations
        specialized_recs = specialized_engine.get_specialized_recommendations(profile)
        
        # Convert to response format
        recommendations = []
        for rec in specialized_recs:
            recommendations.append({
                "content_type": rec.content_type.value,
                "title_suggestion": rec.title_suggestion,
                "description": rec.description,
                "best_time_to_post": rec.best_time_to_post,
                "hashtags": rec.hashtags,
                "target_platforms": rec.target_platforms,
                "priority_score": rec.priority_score,
                "reasoning": rec.reasoning
            })
        
        return {"recommendations": recommendations}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting specialized recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/seasonal-recommendations/{profile_id}")
async def get_seasonal_recommendations(profile_id: str, season: Optional[str] = None):
    """Get seasonal content recommendations"""
    try:
        if not specialized_engine:
            raise HTTPException(status_code=503, detail="Seasonal recommendations service unavailable - missing Google API credentials")
        
        profile = profile_manager.get_profile(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Generate seasonal recommendations
        seasonal_recs = specialized_engine.get_seasonal_craft_recommendations(profile, season)
        
        # Convert to response format
        recommendations = []
        for rec in seasonal_recs:
            recommendations.append({
                "content_type": rec.content_type.value,
                "title_suggestion": rec.title_suggestion,
                "description": rec.description,
                "best_time_to_post": rec.best_time_to_post,
                "hashtags": rec.hashtags,
                "target_platforms": rec.target_platforms,
                "priority_score": rec.priority_score,
                "reasoning": rec.reasoning
            })
        
        return {"recommendations": recommendations}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting seasonal recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/content-calendar/{profile_id}")
async def generate_content_calendar(profile_id: str, days: int = 30):
    """Generate content calendar for artisan"""
    try:
        if not content_strategist:
            raise HTTPException(status_code=503, detail="Content calendar service unavailable - missing Google API credentials")
        
        profile = profile_manager.get_profile(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Generate content calendar
        calendar = content_strategist.generate_content_calendar(profile, days)
        
        # Convert recommendations to dict format
        formatted_calendar = {}
        for date, recommendations in calendar.items():
            formatted_calendar[date] = [
                {
                    "content_type": rec.content_type.value,
                    "title_suggestion": rec.title_suggestion,
                    "description": rec.description,
                    "best_time_to_post": rec.best_time_to_post,
                    "hashtags": rec.hashtags,
                    "target_platforms": rec.target_platforms,
                    "priority_score": rec.priority_score,
                    "reasoning": rec.reasoning
                } for rec in recommendations
            ]
        
        return {"calendar": formatted_calendar}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating content calendar: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Utility endpoints
@app.get("/api/craft-types")
async def get_craft_types():
    """Get available craft types"""
    craft_types = [craft.value for craft in CraftType if craft != CraftType.UNKNOWN]
    return {"craft_types": craft_types}

@app.get("/api/statistics")
async def get_statistics():
    """Get system statistics"""
    try:
        craft_stats = profile_manager.get_craft_statistics()
        experience_dist = profile_manager.get_experience_distribution()
        
        return {
            "craft_statistics": craft_stats,
            "experience_distribution": experience_dist
        }
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)