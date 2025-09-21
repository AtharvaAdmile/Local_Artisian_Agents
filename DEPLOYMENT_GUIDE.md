# A2A AI Agent - FastAPI Deployment Guide

## Overview
This guide covers deploying the A2A AI Agent FastAPI application to Render.com for production use.

## Prerequisites
1. Google Cloud Platform account with:
   - Vertex AI API enabled
   - Cloud Storage bucket created
   - Service account with appropriate permissions
2. Render.com account
3. Environment variables configured

## Environment Variables
Set these in your Render dashboard:

```bash
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CLOUD_PROJECT_ID=your_gcp_project_id
GCS_BUCKET_NAME=your_storage_bucket_name
GOOGLE_CLOUD_LOCATION=us-central1
```

## Render Deployment

### Option 1: Using render.yaml (Recommended)
1. Connect your GitHub repository to Render
2. The `render.yaml` file will automatically configure the service
3. Set environment variables in Render dashboard
4. Deploy!

### Option 2: Manual Setup
1. Create a new Web Service on Render
2. Connect your repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Environment**: Python 3.11
4. Add environment variables
5. Deploy

## Local Development

### Setup
```bash
# Clone repository
git clone <your-repo>
cd <your-repo>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your values

# Run locally
python main.py
```

### Testing
```bash
# API will be available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
# Health check at http://localhost:8000/health
```

## API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Dashboard
- `GET /api/dashboard` - Dashboard overview

### Profile Management
- `POST /api/profiles` - Create artisan profile
- `GET /api/profiles` - List all profiles
- `GET /api/profiles/{profile_id}` - Get specific profile
- `DELETE /api/profiles/{profile_id}` - Delete profile

### Image Analysis
- `POST /api/analyze-image/{profile_id}` - Analyze craft image

### Content Strategy
- `GET /api/content-strategy/{profile_id}` - Generate content strategy
- `GET /api/specialized-recommendations/{profile_id}` - Get specialized recommendations
- `GET /api/seasonal-recommendations/{profile_id}` - Get seasonal recommendations
- `GET /api/content-calendar/{profile_id}` - Generate content calendar

### Utilities
- `GET /api/craft-types` - Available craft types
- `GET /api/statistics` - System statistics

## Frontend Integration

### Example API Calls

#### Create Profile
```javascript
const createProfile = async (profileData) => {
  const response = await fetch('/api/profiles', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(profileData)
  });
  return response.json();
};
```

#### Analyze Image
```javascript
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

#### Get Content Strategy
```javascript
const getContentStrategy = async (profileId) => {
  const response = await fetch(`/api/content-strategy/${profileId}`);
  return response.json();
};
```

## Performance Optimization

### Caching
- Profile data is cached in memory
- Consider Redis for production scaling

### Rate Limiting
- Implement rate limiting for production
- Use nginx or Cloudflare for additional protection

### Monitoring
- Use Render's built-in monitoring
- Consider adding Sentry for error tracking
- Monitor API response times and usage

## Security Considerations

### Environment Variables
- Never commit API keys to version control
- Use Render's environment variable management
- Rotate keys regularly

### CORS
- Configure CORS origins for production
- Remove wildcard (*) origins in production

### Authentication
- Consider adding API key authentication
- Implement user authentication if needed

## Scaling

### Horizontal Scaling
- Render automatically handles scaling
- Monitor resource usage and upgrade plan as needed

### Database
- Current implementation uses JSON files
- Consider PostgreSQL for production scaling
- Implement proper database migrations

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are in requirements.txt
2. **Google Cloud Auth**: Verify service account permissions
3. **Memory Issues**: Monitor memory usage, upgrade Render plan if needed
4. **Timeout Issues**: Optimize AI model calls, implement async processing

### Logs
- Check Render logs for deployment issues
- Use structured logging for better debugging
- Monitor error rates and response times

## Support
For issues and questions:
1. Check the logs in Render dashboard
2. Verify environment variables are set correctly
3. Test endpoints using the interactive docs at `/docs`