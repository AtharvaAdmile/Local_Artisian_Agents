# A2A AI Agent API - Usage Guide

## Base URL
```
https://local-artisian-agents.onrender.com
```

## Interactive Documentation
- **Swagger UI**: https://local-artisian-agents.onrender.com/docs
- **ReDoc**: https://local-artisian-agents.onrender.com/redoc

---

## 📋 API Endpoints Reference

### 🏠 **Core Endpoints**

#### 1. **API Information**
```http
GET /
```

**Response:**
```json
{
  "message": "🎨 A2A AI Agent - Artisan Content Strategist API",
  "description": "Empowering Local Artisans in India with AI-powered Content Strategy",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

**Example:**
```bash
curl https://local-artisian-agents.onrender.com/
```

---

#### 2. **Health Check**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-21T18:34:32.210775"
}
```

**Example:**
```bash
curl https://local-artisian-agents.onrender.com/health
```

---

### 👤 **Profile Management**

#### 3. **Create Artisan Profile**
```http
POST /api/profiles
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Ravi Kumar",
  "location": "Jaipur, Rajasthan",
  "specialization": "pottery",
  "experience_years": 15,
  "signature_style": "Traditional terracotta pottery with modern designs",
  "target_audience": "Home decor enthusiasts and functional pottery users",
  "social_media_platforms": ["instagram", "youtube", "facebook"]
}
```

**Response:**
```json
{
  "profile_id": "ravi_kumar_1",
  "message": "Profile created successfully"
}
```

**Available Specializations:**
- `pottery`
- `textiles`
- `jewelry`
- `woodwork`
- `metalwork`
- `painting`
- `embroidery`
- `leather`
- `bamboo`
- `stonework`
- `glasswork`

**Example:**
```javascript
const response = await fetch('https://local-artisian-agents.onrender.com/api/profiles', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: "Priya Sharma",
    location: "Mumbai, Maharashtra",
    specialization: "textiles",
    experience_years: 8,
    signature_style: "Handwoven silk sarees with traditional patterns",
    target_audience: "Fashion enthusiasts and cultural wear buyers",
    social_media_platforms: ["instagram", "pinterest"]
  })
});
const data = await response.json();
```

---

#### 4. **List All Profiles**
```http
GET /api/profiles
```

**Response:**
```json
[
  {
    "id": "ravi_kumar_1",
    "name": "Ravi Kumar",
    "location": "Jaipur, Rajasthan",
    "specialization": "pottery",
    "experience_years": 15,
    "created_at": "2025-09-21T18:30:00.000000"
  }
]
```

**Example:**
```bash
curl https://local-artisian-agents.onrender.com/api/profiles
```

---

#### 5. **Get Specific Profile**
```http
GET /api/profiles/{profile_id}
```

**Response:**
```json
{
  "id": "ravi_kumar_1",
  "name": "Ravi Kumar",
  "location": "Jaipur, Rajasthan",
  "specialization": "pottery",
  "experience_years": 15,
  "signature_style": "Traditional terracotta pottery with modern designs",
  "target_audience": "Home decor enthusiasts and functional pottery users",
  "social_media_platforms": ["instagram", "youtube", "facebook"],
  "created_at": "2025-09-21T18:30:00.000000"
}
```

**Example:**
```bash
curl https://local-artisian-agents.onrender.com/api/profiles/ravi_kumar_1
```

---

#### 6. **Delete Profile**
```http
DELETE /api/profiles/{profile_id}
```

**Response:**
```json
{
  "message": "Profile deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE https://local-artisian-agents.onrender.com/api/profiles/ravi_kumar_1
```

---

### 📊 **Dashboard & Statistics**

#### 7. **Dashboard Overview**
```http
GET /api/dashboard
```

**Response:**
```json
{
  "total_artisans": 5,
  "craft_types": 3,
  "active_profiles": 5,
  "system_status": "online",
  "craft_distribution": {
    "pottery": 2,
    "textiles": 2,
    "jewelry": 1
  },
  "recent_profiles": [
    {
      "id": "ravi_kumar_1",
      "name": "Ravi Kumar",
      "location": "Jaipur, Rajasthan",
      "specialization": "pottery",
      "experience_years": 15,
      "created_at": "2025-09-21T18:30:00.000000"
    }
  ]
}
```

**Example:**
```javascript
const dashboard = await fetch('https://local-artisian-agents.onrender.com/api/dashboard')
  .then(res => res.json());
```

---

#### 8. **System Statistics**
```http
GET /api/statistics
```

**Response:**
```json
{
  "craft_statistics": {
    "pottery": 2,
    "textiles": 2,
    "jewelry": 1
  },
  "experience_distribution": {
    "beginner (0-2 years)": 1,
    "intermediate (3-7 years)": 2,
    "experienced (8-15 years)": 1,
    "expert (15+ years)": 1
  }
}
```

---

#### 9. **Available Craft Types**
```http
GET /api/craft-types
```

**Response:**
```json
{
  "craft_types": [
    "pottery",
    "textiles",
    "jewelry",
    "woodwork",
    "metalwork",
    "painting",
    "embroidery",
    "leather",
    "bamboo",
    "stonework",
    "glasswork"
  ]
}
```

---

### 🤖 **AI-Powered Content Strategy** *(Requires API Keys)*

#### 10. **Generate Content Strategy**
```http
GET /api/content-strategy/{profile_id}
```

**Response:**
```json
{
  "recommendations": [
    {
      "content_type": "process_video",
      "title_suggestion": "Master the Pottery Wheel - Behind the Scenes of Traditional Terracotta",
      "description": "Show your pottery creation process from clay preparation to final glazing",
      "best_time_to_post": "6-8 PM",
      "hashtags": ["#pottery", "#handmade", "#ceramics", "#indiancrafts", "#terracotta"],
      "target_platforms": ["instagram", "youtube"],
      "priority_score": 0.95,
      "reasoning": "Process videos are highly engaging for pottery content and showcase expertise"
    },
    {
      "content_type": "finished_product",
      "title_suggestion": "Latest Pottery Creation - Handcrafted Terracotta Vase",
      "description": "Showcase your finished masterpiece with detailed shots and cultural context",
      "best_time_to_post": "6-8 PM",
      "hashtags": ["#pottery", "#handmade", "#ceramics", "#homedecor"],
      "target_platforms": ["instagram", "facebook"],
      "priority_score": 0.88,
      "reasoning": "Finished product photos drive sales interest and showcase quality"
    }
  ]
}
```

**Error Response (No API Key):**
```json
{
  "detail": "Content strategy service unavailable - missing Google API credentials"
}
```

---

#### 11. **Get Specialized Recommendations**
```http
GET /api/specialized-recommendations/{profile_id}
```

**Response:**
```json
{
  "recommendations": [
    {
      "content_type": "tutorial",
      "title_suggestion": "Pottery Wheel Throwing Techniques for Beginners",
      "description": "Step-by-step tutorial on wheel throwing techniques specific to pottery",
      "best_time_to_post": "6-8 PM",
      "hashtags": ["#pottery", "#tutorial", "#wheelthrowning", "#ceramics"],
      "target_platforms": ["youtube", "instagram"],
      "priority_score": 0.92,
      "reasoning": "Educational content builds authority in pottery and attracts learning audience"
    }
  ]
}
```

---

#### 12. **Get Seasonal Recommendations**
```http
GET /api/seasonal-recommendations/{profile_id}?season=festival
```

**Query Parameters:**
- `season` (optional): `festival`, `monsoon`, `summer`, `winter`

**Response:**
```json
{
  "recommendations": [
    {
      "content_type": "seasonal_content",
      "title_suggestion": "Perfect Festival Pottery - Diwali Diyas and Decorations",
      "description": "Diwali diyas, festival decorations",
      "best_time_to_post": "6-8 PM",
      "hashtags": ["#pottery", "#handmade", "#ceramics", "#indiancrafts", "#festival"],
      "target_platforms": ["instagram", "facebook"],
      "priority_score": 0.95,
      "reasoning": "Seasonal relevance increases engagement during festival"
    }
  ]
}
```

---

#### 13. **Generate Content Calendar**
```http
GET /api/content-calendar/{profile_id}?days=30
```

**Query Parameters:**
- `days` (optional): Number of days for calendar (default: 30)

**Response:**
```json
{
  "calendar": {
    "2025-09-21": [
      {
        "content_type": "process_video",
        "title_suggestion": "Master the Pottery Wheel - Behind the Scenes",
        "description": "Show your pottery creation process",
        "best_time_to_post": "6-8 PM",
        "hashtags": ["#pottery", "#handmade"],
        "target_platforms": ["instagram", "youtube"],
        "priority_score": 0.9,
        "reasoning": "Process videos are highly engaging"
      }
    ],
    "2025-09-22": [],
    "2025-09-23": [
      {
        "content_type": "finished_product",
        "title_suggestion": "Latest Pottery Creation",
        "description": "Showcase your finished masterpiece",
        "best_time_to_post": "6-8 PM",
        "hashtags": ["#pottery", "#handmade"],
        "target_platforms": ["instagram", "facebook"],
        "priority_score": 0.8,
        "reasoning": "Finished product photos drive sales"
      }
    ]
  }
}
```

---

### 🖼️ **Image Analysis** *(Requires Google Cloud Credentials)*

#### 14. **Analyze Craft Image**
```http
POST /api/analyze-image/{profile_id}
Content-Type: multipart/form-data
```

**Request:**
- Form data with `file` field containing image

**Response:**
```json
{
  "gcs_uri": "gs://artisan-craft-images/ravi_kumar_1/20250921_183000_abc123.jpg",
  "analysis": {
    "colors": ["terracotta", "brown", "earth tones"],
    "patterns": ["geometric", "traditional"],
    "materials": ["clay", "natural glazes"],
    "style": "traditional Indian pottery",
    "craft_type": "pottery",
    "complexity_level": "intermediate",
    "estimated_time": "2-4 hours",
    "confidence_score": 0.92,
    "cultural_significance": "Traditional Indian handicraft with regional influences",
    "techniques_observed": ["wheel throwing", "hand glazing"],
    "market_appeal": "Strong market appeal for traditional pottery",
    "improvement_suggestions": ["Consider adding decorative patterns", "Experiment with natural dyes"],
    "content_angles": ["Process video", "Cultural story", "Technique tutorial"]
  },
  "insights": {
    "market_appeal": "Strong market appeal for traditional pottery",
    "target_audience": "Home decor enthusiasts and collectors",
    "seasonal_relevance": "Perfect for festival decorations",
    "uniqueness_factor": "Highly distinctive craft with clear traditional elements",
    "content_potential": "Good content potential - educational and inspiring for audience"
  },
  "content_recommendations": {
    "general": [
      {
        "title_suggestion": "Traditional Pottery Making Process",
        "content_type": "process_video",
        "description": "Show the complete pottery making process",
        "best_time_to_post": "6-8 PM",
        "target_platforms": ["instagram", "youtube"]
      }
    ],
    "specialized": [
      {
        "title_suggestion": "Master Potter's Wheel Throwing Technique",
        "content_type": "tutorial",
        "description": "Advanced wheel throwing techniques for pottery",
        "best_time_to_post": "6-8 PM",
        "target_platforms": ["youtube", "instagram"]
      }
    ]
  }
}
```

**Error Response (No Credentials):**
```json
{
  "detail": "Image analysis service unavailable - missing Google Cloud credentials"
}
```

**Example:**
```javascript
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('https://local-artisian-agents.onrender.com/api/analyze-image/ravi_kumar_1', {
  method: 'POST',
  body: formData
});
const analysis = await response.json();
```

---

## 🔧 **Error Responses**

### **Common HTTP Status Codes:**

- **200**: Success
- **400**: Bad Request (invalid data)
- **404**: Not Found (profile doesn't exist)
- **422**: Validation Error (invalid input format)
- **500**: Internal Server Error
- **503**: Service Unavailable (missing API credentials)

### **Error Response Format:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## 💻 **Code Examples**

### **JavaScript/Node.js**

```javascript
// Create a profile
async function createProfile(profileData) {
  const response = await fetch('https://local-artisian-agents.onrender.com/api/profiles', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(profileData)
  });
  return response.json();
}

// Get content strategy
async function getContentStrategy(profileId) {
  const response = await fetch(`https://local-artisian-agents.onrender.com/api/content-strategy/${profileId}`);
  return response.json();
}

// Analyze image
async function analyzeImage(profileId, imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch(`https://local-artisian-agents.onrender.com/api/analyze-image/${profileId}`, {
    method: 'POST',
    body: formData
  });
  return response.json();
}
```

### **Python**

```python
import requests

BASE_URL = "https://local-artisian-agents.onrender.com"

# Create profile
def create_profile(profile_data):
    response = requests.post(f"{BASE_URL}/api/profiles", json=profile_data)
    return response.json()

# Get profiles
def get_profiles():
    response = requests.get(f"{BASE_URL}/api/profiles")
    return response.json()

# Get content strategy
def get_content_strategy(profile_id):
    response = requests.get(f"{BASE_URL}/api/content-strategy/{profile_id}")
    return response.json()

# Analyze image
def analyze_image(profile_id, image_path):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/api/analyze-image/{profile_id}", files=files)
    return response.json()
```

### **cURL**

```bash
# Create profile
curl -X POST https://local-artisian-agents.onrender.com/api/profiles \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Artisan Name",
    "location": "City, State",
    "specialization": "pottery",
    "experience_years": 10,
    "signature_style": "Traditional style",
    "target_audience": "Art lovers",
    "social_media_platforms": ["instagram"]
  }'

# Get profiles
curl https://local-artisian-agents.onrender.com/api/profiles

# Get content strategy
curl https://local-artisian-agents.onrender.com/api/content-strategy/profile_id

# Analyze image
curl -X POST https://local-artisian-agents.onrender.com/api/analyze-image/profile_id \
  -F "file=@image.jpg"
```

---

## 🚀 **Getting Started**

1. **Test the API**: Start with the health check endpoint
2. **Create a Profile**: Use the profile creation endpoint
3. **Explore Features**: Try dashboard and statistics endpoints
4. **AI Features**: Requires valid Google API keys for full functionality

## 📚 **Additional Resources**

- **Interactive Documentation**: https://local-artisian-agents.onrender.com/docs
- **GitHub Repository**: [Your Repository Link]
- **Deployment Guide**: See `DEPLOYMENT_GUIDE.md`

---

## 🔑 **API Key Requirements**

For full AI functionality, the following environment variables must be set on the server:

- `GOOGLE_API_KEY`: For content strategy generation
- `GOOGLE_CLOUD_PROJECT_ID`: For image analysis
- `GCS_BUCKET_NAME`: For image storage

Without these keys, the API will return `503 Service Unavailable` for AI-powered endpoints, but all profile management and basic features will work perfectly.