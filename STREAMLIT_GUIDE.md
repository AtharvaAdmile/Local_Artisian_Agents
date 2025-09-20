# A2A AI Agent - Streamlit Web Application Guide

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   Update `.env` file with your credentials:
   ```env
   GOOGLE_API_KEY=your_google_ai_api_key
   GOOGLE_CLOUD_PROJECT_ID=your-gcp-project-id
   GCS_BUCKET_NAME=your-bucket-name
   ```

3. **Run Application**
   ```bash
   streamlit run streamlit_app.py
   ```
   
   Application will be available at: http://localhost:8501

## 📋 Features Overview

### 🏠 Dashboard
- **System Statistics**: View total artisans, craft types, and active profiles
- **Craft Distribution**: Visual chart showing artisan specializations
- **Recent Profiles**: Quick overview of newly created profiles
- **Quick Actions**: Direct navigation to key features

### 👤 Artisan Profiles
**Create Profile Tab:**
- Enter artisan details (name, location, specialization)
- Set experience level and signature style
- Configure target audience and social media platforms
- Auto-suggestions based on craft type

**View Profiles Tab:**
- Browse all registered artisan profiles
- Search by name or location
- Filter by craft specialization
- Quick actions for each profile

### 🖼️ Image Analysis
**AI-Powered Craft Analysis:**
1. Select artisan profile
2. Upload craft image (JPG, PNG, WEBP supported)
3. Image automatically uploaded to Google Cloud Storage
4. AI analysis using Gemini multimodal model
5. Detailed results including:
   - Craft type identification
   - Complexity level assessment
   - Color and pattern analysis
   - Material identification
   - Confidence scoring
   - Content recommendations

**Analysis Results Display:**
- Visual metrics and confidence scores
- Detailed craft characteristics
- AI-generated content recommendations
- Platform-specific suggestions

### 📋 Content Strategy
**Strategy Generation:**
1. Select artisan profile
2. Generate comprehensive content strategy
3. View recommendations in organized tabs:
   - **General**: Universal content ideas
   - **Specialized**: Craft-specific recommendations
   - **Seasonal**: Time-relevant content
   - **Calendar**: 7-day content planning

**Recommendation Details:**
- Content type and priority scoring
- Optimal posting times
- Platform-specific strategies
- Hashtag suggestions
- Detailed reasoning for each recommendation

## 🔧 Configuration

### Google Cloud Setup
```bash
# Install Google Cloud SDK
gcloud auth application-default login

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
```

### Environment Variables
```env
# Required for AI functionality
GOOGLE_API_KEY=your_gemini_api_key

# Required for image upload and analysis
GOOGLE_CLOUD_PROJECT_ID=your-gcp-project
GCS_BUCKET_NAME=your-storage-bucket
GOOGLE_CLOUD_LOCATION=us-central1

# Optional Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

## 🎯 Usage Workflow

### For New Users:
1. **Start with Dashboard** - Get system overview
2. **Create Artisan Profile** - Set up your artisan information
3. **Upload Craft Image** - Get AI analysis and recommendations
4. **Generate Content Strategy** - Get personalized content plan

### For Existing Users:
1. **View Dashboard** - Check recent activity and statistics
2. **Upload New Images** - Analyze latest craft work
3. **Generate Updated Strategy** - Get fresh content recommendations
4. **Export Data** - Save strategies for external use

## 💡 Tips for Best Results

### Image Upload:
- Use high-quality, well-lit images
- Show clear details of the craft work
- Include multiple angles if possible
- Ensure good color representation

### Profile Setup:
- Provide detailed signature style description
- Accurately set experience level
- Select relevant social media platforms
- Define clear target audience

### Content Strategy:
- Review recommendations regularly
- Adapt suggestions to your style
- Track performance of implemented content
- Update strategy based on results

## 🛠️ Troubleshooting

### Common Issues:

**"Failed to initialize system"**
- Check Google Cloud credentials
- Verify API keys in .env file
- Ensure required APIs are enabled

**"Image upload failed"**
- Check GCS bucket permissions
- Verify project ID and bucket name
- Ensure sufficient storage quota

**"No recommendations generated"**
- Check API quota limits
- Verify Gemini API access
- Try with different image or profile

### Support:
- Check application logs for detailed error messages
- Verify all environment variables are set correctly
- Ensure Google Cloud authentication is working

## 🔒 Security Notes

- Keep API keys secure and never commit to version control
- Use IAM roles with minimal required permissions
- Regularly rotate access keys
- Monitor usage and costs in Google Cloud Console

## 🚀 Performance Tips

- Use images under 10MB for faster uploads
- Cache frequently accessed data
- Monitor API usage to stay within quotas
- Optimize image formats (JPEG recommended)