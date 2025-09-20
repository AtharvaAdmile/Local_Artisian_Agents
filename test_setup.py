#!/usr/bin/env python3
"""
Test script to verify A2A AI Agent setup
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test environment configuration"""
    print("🔧 Testing Environment Configuration")
    print("-" * 40)
    
    # Check .env loading
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print(f"✅ GOOGLE_API_KEY: {api_key[:10]}...")
    else:
        print("❌ GOOGLE_API_KEY not found")
    
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID', 'your-project-id')
    print(f"📋 GOOGLE_CLOUD_PROJECT_ID: {project_id}")
    
    bucket_name = os.getenv('GCS_BUCKET_NAME', 'artisan-craft-images')
    print(f"🪣 GCS_BUCKET_NAME: {bucket_name}")
    
    return api_key is not None

def test_imports():
    """Test required imports"""
    print("\n📦 Testing Required Imports")
    print("-" * 40)
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import error: {e}")
        return False
    
    try:
        from artisan_ai_agent import ArtisanProfile, CraftType
        print("✅ Core agent modules imported successfully")
    except ImportError as e:
        print(f"❌ Core module import error: {e}")
        return False
    
    try:
        from profile_manager import ProfileManager
        print("✅ Profile manager imported successfully")
    except ImportError as e:
        print(f"❌ Profile manager import error: {e}")
        return False
    
    # Note: GCS modules will fail without proper credentials, but that's expected
    try:
        from gcs_image_analyzer import GCSCraftImageAnalyzer
        print("✅ GCS image analyzer imported successfully")
    except ImportError as e:
        print(f"⚠️  GCS image analyzer import warning: {e}")
        print("   This is expected without proper GCS setup")
    
    return True

def main():
    """Main test function"""
    print("🎨 A2A AI Agent - Setup Test")
    print("=" * 50)
    
    env_ok = test_environment()
    imports_ok = test_imports()
    
    print("\n" + "=" * 50)
    if env_ok and imports_ok:
        print("✅ Setup test completed successfully!")
        print("🚀 Ready to run Streamlit application")
        print("\nTo start the app, run:")
        print("   streamlit run streamlit_app.py")
    else:
        print("❌ Setup test failed")
        print("Please check the errors above and fix them")
    
    return env_ok and imports_ok

if __name__ == "__main__":
    main()