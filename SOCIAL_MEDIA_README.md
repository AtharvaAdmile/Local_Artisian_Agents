# 🤖 Integrated AI Agent Manager

## Social Media Management + AI Storytelling System

This comprehensive system extends the A2A AI Agent with advanced social media management and AI-powered storytelling capabilities specifically designed for local artisans in India.

---

## 🌟 **System Overview**

The Integrated AI Agent Manager combines:
- **🎨 Original A2A AI Agent** - Craft analysis and content strategy
- **📱 Social Media Manager** - Multi-platform profile and content management
- **📖 AI Storytelling Engine** - Cultural storytelling for marketing and sales
- **🔗 Integration Layer** - Seamless workflow between all components

---

## 🎯 **Key Features**

### 📱 **Social Media Management**
- **Multi-Platform Support**: Instagram, Facebook, YouTube, Pinterest, Twitter, TikTok
- **Profile Management**: Complete social media profile setup and configuration
- **Content Asset Management**: Organize and manage all digital content
- **Performance Analytics**: Track engagement, reach, and growth metrics
- **Automated Scheduling**: Plan and schedule content across platforms

### 📖 **AI-Powered Storytelling**
- **Cultural Storytelling**: Stories rooted in Indian traditions and values
- **8 Story Types**: Origin stories, craft journeys, cultural heritage, customer stories, etc.
- **Platform Optimization**: Content adapted for each social media platform
- **Marketing Integration**: Stories designed to drive sales and brand awareness
- **Emotional Engagement**: Narratives that build trust and connection

### 🔗 **Complete Integration**
- **Workflow Chaining**: Craft analysis → Content strategy → Social media → Storytelling
- **Unified Dashboard**: Manage everything from one interface
- **Data Synchronization**: Seamless data flow between all components
- **Comprehensive Analytics**: Full-picture performance tracking

---

## 🏗️ **System Architecture**

### **Core Components**

1. **`ai_agent_manager.py`** - Main social media management system
2. **`storytelling_engine.py`** - AI-powered narrative generation
3. **`agent_integration.py`** - Integration layer connecting all systems
4. **`social_media_streamlit.py`** - Web interface for social media management

### **Data Models**

```python
# Social Media Profile
@dataclass
class SocialMediaProfile:
    platform: SocialMediaPlatform
    username: str
    followers_count: int
    engagement_rate: float
    posting_frequency: str
    best_posting_times: List[str]

# Story Content
@dataclass
class StoryContent:
    story_type: StoryType
    title: str
    narrative: str
    hook: str
    call_to_action: str
    platform_adaptations: Dict[str, str]

# Content Asset
@dataclass
class ContentAsset:
    asset_type: ContentAssetType
    title: str
    gcs_uri: str
    craft_analysis_id: str
```

---

## 🚀 **Getting Started**

### **1. Installation**

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Update .env file with your API keys and project settings
```

### **2. Run Applications**

```bash
# Social Media Manager Interface
streamlit run social_media_streamlit.py

# Original A2A AI Agent Interface  
streamlit run streamlit_app.py

# Complete System Demo
python integrated_demo.py
```

### **3. Access Applications**

- **Social Media Manager**: http://localhost:8501
- **Original A2A Agent**: http://localhost:8502 (if running both)

---

## 📋 **Usage Workflows**

### **Complete Artisan Onboarding**

1. **Artisan Setup**
   - Enter basic information (name, location, craft specialization)
   - Set experience level and signature style
   - Define target audience

2. **Social Media Configuration**
   - Setup profiles across platforms
   - Configure usernames and profile URLs
   - Set posting frequencies and optimal times

3. **Craft Image Analysis**
   - Upload craft images to Google Cloud Storage
   - AI analysis using Gemini multimodal
   - Extract colors, patterns, materials, and style

4. **Story Generation**
   - Generate AI-powered stories based on craft analysis
   - Create marketing story chains
   - Adapt content for different platforms

5. **Content Calendar**
   - Integrated calendar with recommendations and stories
   - Automated scheduling suggestions
   - Performance tracking setup

### **Story Generation Workflow**

```python
# Generate single story
story_content = storytelling_engine.generate_story_content(
    artisan_profile=profile,
    craft_analysis=analysis,
    story_type=StoryType.ORIGIN_STORY,
    target_platforms=['instagram', 'facebook']
)

# Generate marketing chain
story_chain = storytelling_engine.generate_marketing_story_chain(
    artisan_profile=profile,
    craft_analysis=analysis,
    content_recommendations=recommendations
)
```

---

## 📖 **Storytelling Framework**

### **Story Types**

1. **🏺 Origin Story** - Heritage and family traditions
2. **🛠️ Craft Journey** - Learning and skill development
3. **🏛️ Cultural Heritage** - Traditional methods and cultural significance
4. **👥 Customer Story** - Client experiences and testimonials
5. **🎭 Behind Scenes** - Workshop life and daily processes
6. **🌺 Seasonal Story** - Festival and seasonal connections
7. **⚙️ Process Story** - Detailed craft creation process
8. **💡 Inspiration Story** - Creative vision and artistic inspiration

### **Cultural Elements**

- **Regional Context**: State-specific cultural elements
- **Festival Integration**: Diwali, Holi, regional celebrations
- **Traditional Values**: Family legacy, guru-shishya parampara
- **Cultural Symbols**: Lotus, peacock, mandala, rangoli patterns
- **Authentic Language**: Hindi/regional terms with English explanations

### **Platform Adaptations**

- **Instagram**: Visual, concise, hashtag-optimized
- **Facebook**: Community-focused, discussion-worthy
- **YouTube**: Educational, comprehensive narratives
- **Pinterest**: Inspirational, DIY-focused

---

## 📱 **Platform Configurations**

### **Instagram Optimization**
- Max caption: 2,200 characters
- Max hashtags: 30
- Optimal times: 6-9 AM, 12-2 PM, 5-7 PM
- Content types: Photos, videos, carousels, reels, stories

### **Facebook Strategy**
- Max caption: 63,206 characters
- Max hashtags: 10 (recommended)
- Optimal times: 9-10 AM, 1-3 PM, 3-4 PM
- Content types: Photos, videos, carousels, events, live

### **YouTube Focus**
- Max title: 100 characters
- Max description: 5,000 characters
- Optimal times: 2-4 PM, 6-9 PM
- Content types: Videos, shorts, live streams, premieres

---

## 📊 **Analytics & Performance**

### **Tracked Metrics**
- Follower growth rates
- Engagement rates by platform
- Story performance metrics
- Content asset utilization
- Posting frequency analysis

### **Performance Targets**
- **Follower Growth**: 5-10% monthly
- **Engagement Rate**: 3-5% minimum
- **Content Reach**: 20% monthly increase
- **Story Engagement**: Above average post performance
- **Sales Inquiries**: 2-5 per month through social media

---

## 🔧 **Configuration**

### **Environment Variables**

```env
# Google AI API
GOOGLE_API_KEY=your_google_ai_api_key

# Google Cloud Platform
GOOGLE_CLOUD_PROJECT_ID=your-gcp-project-id
GCS_BUCKET_NAME=artisan-craft-images
GOOGLE_CLOUD_LOCATION=us-central1

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### **Data Files**

- `social_media_profiles.json` - Social media profile configurations
- `content_assets.json` - Digital content asset registry
- `story_contents.json` - Generated story content database
- `scheduled_posts.json` - Content scheduling information

---

## 🎨 **Sample Generated Content**

### **Origin Story Example**

**Title**: "The Legacy of Blue Pottery: Priya's Journey from Heritage to Innovation"

**Hook**: "In the ancient lanes of Jaipur, where tradition meets artistry, one woman carries forward a 300-year-old legacy..."

**Narrative**: A compelling story weaving together family tradition, cultural significance, and modern innovation in blue pottery craft.

**Platform Adaptations**:
- **Instagram**: Visual storytelling with behind-the-scenes photos
- **Facebook**: Detailed narrative with community engagement
- **YouTube**: Documentary-style video content

### **Marketing Story Chain**

1. **Behind Scenes** → Build authenticity and trust
2. **Process Story** → Showcase expertise and skill
3. **Cultural Heritage** → Connect with cultural values
4. **Customer Story** → Provide social proof
5. **Origin Story** → Create emotional connection

---

## 🚀 **Advanced Features**

### **AI Story Optimization**
- **Sales Integration**: Stories optimized for conversion
- **Cultural Authenticity**: Rooted in Indian traditions
- **Emotional Engagement**: Designed to build trust and connection
- **SEO Optimization**: Hashtags and keywords for discoverability

### **Content Calendar Intelligence**
- **Automated Scheduling**: AI-suggested optimal posting times
- **Story Integration**: Stories woven into regular content flow
- **Seasonal Awareness**: Festival and cultural event alignment
- **Performance Learning**: Adapts based on engagement metrics

### **Multi-Platform Synchronization**
- **Cross-Platform Consistency**: Unified brand voice across platforms
- **Platform-Specific Optimization**: Content adapted for each platform's strengths
- **Automated Formatting**: Content automatically formatted for platform requirements

---

## 🔄 **Integration Benefits**

### **For Artisans**
- **Complete Solution**: Everything needed for digital presence
- **Cultural Authenticity**: Stories that resonate with Indian audiences
- **Sales Growth**: Content designed to drive business results
- **Time Savings**: Automated content generation and scheduling

### **For the Market**
- **Craft Preservation**: Digital documentation of traditional arts
- **Cultural Promotion**: Spreading awareness of Indian crafts globally
- **Economic Impact**: Helping artisans reach wider markets
- **Educational Value**: Teaching craft techniques and cultural significance

---

## 🎯 **Success Metrics**

### **Engagement Metrics**
- Story completion rates
- Comment and share volumes
- Profile visits and follows
- Direct message inquiries

### **Business Metrics**
- Sales inquiry increase
- Custom order requests
- Brand recognition growth
- Market reach expansion

### **Cultural Impact**
- Traditional craft awareness
- Cultural story sharing
- Heritage preservation
- Community building

---

## 🛠️ **Technical Specifications**

### **AI Models Used**
- **Google Gemini 2.0 Flash**: Story generation and content optimization
- **Vertex AI**: Image analysis and craft identification
- **Google Cloud Storage**: Media asset management

### **Performance Requirements**
- **Response Time**: <3 seconds for story generation
- **Image Analysis**: <5 seconds for craft identification
- **Calendar Generation**: <2 seconds for 30-day calendar
- **Data Synchronization**: Real-time across all components

---

## 📞 **Support & Documentation**

### **Quick Start Guide**
1. Run `python integrated_demo.py` for complete system demonstration
2. Access Streamlit interfaces for hands-on experience
3. Review generated stories and content recommendations
4. Explore platform-specific adaptations

### **Troubleshooting**
- Check Google Cloud authentication
- Verify API key configurations
- Ensure required permissions for GCS buckets
- Monitor API usage quotas

### **Community & Feedback**
- Designed specifically for Indian artisan communities
- Culturally sensitive and authentic content generation
- Continuous improvement based on artisan feedback
- Support for traditional craft preservation

---

## 🎊 **Conclusion**

The Integrated AI Agent Manager represents a complete digital transformation solution for local artisans in India. By combining advanced AI storytelling with comprehensive social media management, it empowers artisans to:

- **Preserve and promote** traditional crafts through digital storytelling
- **Reach global audiences** while maintaining cultural authenticity  
- **Grow their businesses** through strategic social media presence
- **Connect with customers** through compelling narratives and engaging content

**🚀 Ready to transform your craft into compelling digital stories that drive sales and preserve cultural heritage!**