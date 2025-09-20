# A2A AI Agent for Local Artisans in India

## Content Strategist and Management System

This AI agent helps local artisans in India by providing intelligent content strategy recommendations and craft analysis capabilities.

### Features

🎨 **Craft Image Analysis with Google Cloud Storage**
- Upload images directly through web interface
- Automatic storage in Google Cloud Storage buckets
- AI-powered image analysis using Gemini multimodal
- Real-time confidence scoring and detailed craft insights
- Cultural context recognition for Indian crafts

📱 **Streamlit Web Application**
- Modern, responsive web interface
- Real-time dashboard with statistics
- Interactive profile management
- Drag-and-drop image uploads
- Visual content recommendations display

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

**Option A: Streamlit Web Application (Recommended)**
```bash
python run_streamlit.py
```
Or directly:
```bash
streamlit run streamlit_app.py
```

**Option B: Command Line Interface**
```bash
python main_application.py
```

**Option C: Demo Script**
```bash
python demo.py
```

### Usage

#### Creating an Artisan Profile
```python
from main_application import ArtisanContentManager

app = ArtisanContentManager()

profile_id = app.create_artisan_profile(
    name="Ravi Kumar",
    location="Jaipur, Rajasthan",
    specialization="pottery",
    experience_years=15,
    target_audience="Home decor enthusiasts",
    social_media_platforms=["instagram", "youtube"]
)
```

#### Analyzing Craft Images
```python
# Analyze a craft image and get content recommendations
result = app.analyze_craft_image(profile_id, "pottery_image.jpg")

print(f"Detected craft: {result['analysis']['craft_type']}")
print(f"Complexity: {result['analysis']['complexity_level']}")
print(f"Colors: {result['analysis']['colors']}")
```

#### Getting Content Strategy
```python
# Get comprehensive content strategy
strategy = app.get_content_strategy(profile_id)

print(f"General recommendations: {len(strategy['recommendations']['general'])}")
print(f"Specialized recommendations: {len(strategy['recommendations']['specialized'])}")
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

### File Structure

```
├── main_application.py          # Main application interface
├── artisan_ai_agent.py         # Core data models and base agent
├── profile_manager.py          # Artisan profile management
├── image_analyzer.py           # AI-powered craft image analysis
├── content_strategist.py       # Content strategy engine
├── specialized_recommendations.py # Craft-specific recommendations
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables
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

### Future Enhancements

- **Web Interface** - Browser-based user interface
- **Social Media Integration** - Direct posting to platforms
- **Performance Analytics** - Track content engagement
- **Multi-language Support** - Regional language support
- **Mobile App** - Smartphone application
- **Marketplace Integration** - E-commerce platform connections

### Support

For support and questions, please refer to the documentation or create an issue in the project repository.

### License

This project is designed to support local artisans in India and promote traditional crafts through digital content strategies.