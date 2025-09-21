# A2A AI Agent - Artisan Content Strategist API

## FastAPI-based Content Strategy System for Local Artisans in India

This AI-powered API helps local artisans in India create engaging social media content and grow their businesses through intelligent content strategy recommendations and craft analysis capabilities. Optimized for deployment on Render and frontend integration.

### Features

🎨 **Craft Image Analysis with Google Cloud Storage**
- Upload images directly through web interface
- Automatic storage in Google Cloud Storage buckets
- AI-powered image analysis using Gemini multimodal
- Real-time confidence scoring and detailed craft insights
- Cultural context recognition for Indian crafts

🚀 **FastAPI RESTful API**
- High-performance async API with automatic documentation
- Interactive Swagger UI at `/docs`
- CORS-enabled for frontend integration
- Health checks and monitoring endpoints
- Optimized for cloud deployment (Render, Heroku, etc.)

📋 **Content Strategy Recommendations**
- Personalized content suggestions based on artisan specialization
- Platform-specific recommendations (Instagram, YouTube, Facebook)
- Optimal posting times and hashtag suggestions
- AI-generated content calendars

👤 **Artisan Profile Management**
- Comprehensive profile system with craft specialization tracking
- Experience level assessment and skill development guidance
- Social media platform optimization
- Profile statistics and analytics

🎯 **Specialized Recommendations**
- Craft-specific content strategies (pottery, textiles, jewelry, woodwork, etc.)
- Technique-focused tutorials and process videos
- Market-specific content for different target audiences
- Seasonal and festival-aligned content strategies

🗓️ **Content Calendar & Planning**
- Automated content planning and scheduling
- Seasonal content recommendations
- Festival and cultural event integration
- Weekly content calendar generation

### Supported Craft Types

- **Pottery** - Traditional ceramics and terracotta
- **Textiles** - Handloom weaving and natural dyeing
- **Jewelry** - Traditional and contemporary designs
- **Woodwork** - Furniture and decorative items
- **Metalwork** - Brass, copper, and silver crafts
- **Painting** - Traditional and folk art
- **Embroidery** - Regional needlework traditions
- **Leather** - Traditional leather crafts
- **Bamboo** - Sustainable bamboo products
- **Stonework** - Stone carving and sculpture
- **Glasswork** - Traditional glass crafts

### Installation and Setup

#### 1. Prerequisites
- Python 3.8 or higher
- Google Cloud Platform account
- Google AI API key

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure Environment Variables
Update the `.env` file with your credentials:
```env
# Google AI API Configuration
GOOGLE_API_KEY=your_google_ai_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=True

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID=your-gcp-project-id
GCS_BUCKET_NAME=your-gcs-bucket-name
GOOGLE_CLOUD_LOCATION=us-central1
```

#### 4. Google Cloud Setup
```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth application-default login

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
```

#### 5. Run the Application

**Option A: Development Server (Recommended)**
```bash
python start_dev.py
```

**Option B: Direct FastAPI**
```bash
python main.py
```

**Option C: With Uvicorn**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option D: Docker**
```bash
docker build -t a2a-ai-agent .
docker run -p 8000:8000 --env-file .env a2a-ai-agent
```

## 📋 API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /health` - Health check for monitoring
- `GET /docs` - Interactive API documentation (Swagger UI)

### Profile Management
- `POST /api/profiles` - Create artisan profile
- `GET /api/profiles` - List all profiles
- `GET /api/profiles/{profile_id}` - Get specific profile
- `DELETE /api/profiles/{profile_id}` - Delete profile

### Content Strategy
- `GET /api/content-strategy/{profile_id}` - Generate content strategy
- `GET /api/specialized-recommendations/{profile_id}` - Get specialized recommendations
- `GET /api/seasonal-recommendations/{profile_id}` - Get seasonal content ideas
- `GET /api/content-calendar/{profile_id}` - Generate content calendar

### Image Analysis
- `POST /api/analyze-image/{profile_id}` - Analyze craft image with AI

### Utilities
- `GET /api/craft-types` - Available craft specializations
- `GET /api/dashboard` - Dashboard overview data
- `GET /api/statistics` - System statistics

## 🌐 Deployment on Render

### Quick Deploy
1. Fork this repository
2. Connect to Render.com
3. The `render.yaml` file will automatically configure the service
4. Set environment variables in Render dashboard
5. Deploy!

### Environment Variables for Render
```bash
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CLOUD_PROJECT_ID=your_gcp_project_id
GCS_BUCKET_NAME=your_storage_bucket_name
GOOGLE_CLOUD_LOCATION=us-central1
```

### Usage

#### Creating an Artisan Profile via API
```javascript
// Create profile via API
const createProfile = async (profileData) => {
  const response = await fetch('/api/profiles', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: "Ravi Kumar",
      location: "Jaipur, Rajasthan",
      specialization: "pottery",
      experience_years: 15,
      target_audience: "Home decor enthusiasts",
      social_media_platforms: ["instagram", "youtube"]
    })
  });
  return response.json();
};
```

#### Analyzing Craft Images via API
```javascript
// Analyze image via API
const analyzeImage = async (profileId, imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch(`/api/analyze-image/${profileId}`, {
    method: 'POST',
    body: formData
  });
  return response.json();
};
```

#### Getting Content Strategy via API
```javascript
// Get content strategy via API
const getContentStrategy = async (profileId) => {
  const response = await fetch(`/api/content-strategy/${profileId}`);
  const data = await response.json();
  
  console.log(`Recommendations: ${data.recommendations.length}`);
  return data;
};
```

### API Structure

#### Core Classes

- **`ArtisanProfile`** - Artisan information and preferences
- **`CraftAnalysis`** - Image analysis results
- **`ContentRecommendation`** - Content strategy suggestions
- **`ProfileManager`** - Profile CRUD operations
- **`CraftImageAnalyzer`** - AI-powered image analysis
- **`ContentStrategist`** - General content recommendations
- **`SpecializedRecommendationEngine`** - Craft-specific recommendations

#### Content Types

- Process Videos
- Finished Product Showcases
- Behind-the-Scenes Content
- Tutorials and How-tos
- Story Telling and Cultural Context
- Customer Testimonials
- Time-lapse Creation Videos
- Comparison and Educational Content
- Seasonal and Festival Content

### Configuration

The system uses environment variables for configuration:

- `GOOGLE_API_KEY` - Google Generative AI API key for image analysis and content generation
- `GOOGLE_GENAI_USE_VERTEXAI` - Optional: Use Vertex AI instead of AI Studio

## 🧪 Testing

```bash
# Run API tests
python test_api.py

# Test with custom URL
python test_api.py https://your-api-url.com

# Run with development server
python start_dev.py --test
```

## 💻 Frontend Integration

Check out `frontend_example.html` for a complete frontend integration example.

### File Structure

```
├── main.py                     # FastAPI application
├── artisan_ai_agent.py         # Core data models and base agent
├── profile_manager.py          # Artisan profile management
├── gcs_image_analyzer.py       # AI-powered craft image analysis
├── content_strategist.py       # Content strategy engine
├── specialized_recommendations.py # Craft-specific recommendations
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment config
├── Dockerfile                  # Docker configuration
├── start_dev.py               # Development server script
├── test_api.py                # API testing script
├── frontend_example.html      # Frontend integration example
├── DEPLOYMENT_GUIDE.md        # Detailed deployment guide
├── .env.example               # Environment variables template
└── README.md                  # This file
```

### Examples

#### Sample Content Recommendations

**For Pottery Artisan:**
- "Master the Pottery Wheel - Behind the Scenes of Traditional Terracotta"
- "From Clay to Art - Complete Pottery Making Process"
- "Glazing Techniques for Perfect Finish"

**For Textile Artisan:**
- "Natural Dyeing Secrets - Colors from Nature"
- "Handloom Weaving Process - Traditional Patterns"
- "Sustainable Fashion - Eco-friendly Textiles"

#### Image Analysis Output

```json
{
  "analysis": {
    "craft_type": "pottery",
    "colors": ["terracotta", "brown", "earth tones"],
    "patterns": ["geometric", "traditional"],
    "materials": ["clay", "natural glazes"],
    "complexity_level": "intermediate",
    "confidence_score": 0.92
  },
  "insights": {
    "market_appeal": "Strong market appeal for traditional pottery",
    "target_audience": "Home decor enthusiasts and collectors",
    "seasonal_relevance": "Perfect for festival decorations"
  }
}
```

## 📚 Documentation

- **Interactive API Docs**: Visit `/docs` when running the server
- **Deployment Guide**: See `DEPLOYMENT_GUIDE.md` for detailed instructions
- **Frontend Example**: Open `frontend_example.html` for integration examples
- **Testing**: Use `test_api.py` for comprehensive API testing

## 🚀 Quick Start Commands

```bash
# Development setup
python start_dev.py --install    # Install dependencies
python start_dev.py              # Start development server
python start_dev.py --test       # Run tests

# Production deployment
docker build -t a2a-ai-agent .   # Build Docker image
docker run -p 8000:8000 a2a-ai-agent  # Run container
```

### Future Enhancements

- **Database Integration** - PostgreSQL for production scaling
- **Authentication** - User authentication and API keys
- **Social Media Integration** - Direct posting to platforms
- **Performance Analytics** - Track content engagement
- **Multi-language Support** - Regional language support
- **Mobile App** - React Native or Flutter app
- **Marketplace Integration** - E-commerce platform connections

### Support

For support and questions, please refer to the documentation or create an issue in the project repository.

### License

This project is designed to support local artisans in India and promote traditional crafts through digital content strategies.