#!/usr/bin/env python3
"""
Setup and Run Script for A2A AI Agent Streamlit Application
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import streamlit
        import google.cloud.storage
        import vertexai
        import google.generativeai
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required packages: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_environment():
    """Check if environment variables are configured"""
    required_vars = [
        'GOOGLE_API_KEY',
        'GOOGLE_CLOUD_PROJECT_ID', 
        'GCS_BUCKET_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please configure these in your .env file")
        return False
    
    print("✅ Environment variables configured")
    return True

def setup_gcs_bucket():
    """Setup Google Cloud Storage bucket"""
    try:
        from google.cloud import storage
        
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
        bucket_name = os.getenv('GCS_BUCKET_NAME')
        location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
        
        client = storage.Client(project=project_id)
        
        # Check if bucket exists
        bucket = client.bucket(bucket_name)
        if bucket.exists():
            print(f"✅ GCS bucket '{bucket_name}' already exists")
        else:
            # Create bucket
            bucket = client.create_bucket(bucket_name, location=location)
            print(f"✅ Created GCS bucket '{bucket_name}' in {location}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up GCS bucket: {e}")
        print("Please ensure you have:")
        print("1. Google Cloud SDK installed")
        print("2. Authenticated with: gcloud auth application-default login")
        print("3. Enabled Cloud Storage API")
        return False

def run_streamlit():
    """Run the Streamlit application"""
    try:
        print("🚀 Starting Streamlit application...")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("👋 Streamlit application stopped")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

def main():
    """Main setup and run function"""
    print("🎨 A2A AI Agent - Streamlit Setup & Run")
    print("=" * 50)
    
    # Check current directory
    if not Path("streamlit_app.py").exists():
        print("❌ streamlit_app.py not found. Please run from the correct directory.")
        return
    
    # Check requirements
    if not check_requirements():
        return
    
    # Check environment
    if not check_environment():
        return
    
    # Setup GCS bucket
    print("\n🪣 Setting up Google Cloud Storage...")
    if not setup_gcs_bucket():
        print("⚠️  GCS setup failed, but you can still run the app")
        input("Press Enter to continue or Ctrl+C to exit...")
    
    # Run Streamlit
    print("\n🎨 Starting A2A AI Agent Streamlit Application...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("⚠️  Make sure to configure your .env file with correct values")
    print("🛑 Press Ctrl+C to stop the application")
    print("-" * 50)
    
    run_streamlit()

if __name__ == "__main__":
    main()