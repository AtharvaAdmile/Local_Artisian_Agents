#!/usr/bin/env python3
"""
Development startup script for A2A AI Agent FastAPI
Handles environment setup and starts the server with hot reload
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_environment():
    """Check if environment is properly set up"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("📝 Creating .env from template...")
        
        example_file = Path(".env.example")
        if example_file.exists():
            import shutil
            shutil.copy(example_file, env_file)
            print("✅ .env file created from template")
            print("🔧 Please edit .env file with your configuration")
        else:
            print("❌ .env.example not found")
            return False
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except ImportError:
        print("⚠️  python-dotenv not installed, skipping .env loading")
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_server(port=8000, reload=True):
    """Start the FastAPI server"""
    print(f"🚀 Starting A2A AI Agent API server on port {port}...")
    print(f"📖 API docs will be available at: http://localhost:{port}/docs")
    print(f"🏥 Health check at: http://localhost:{port}/health")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", str(port)
        ]
        
        if reload:
            cmd.extend(["--reload", "--reload-dir", "."])
        
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def run_tests():
    """Run API tests"""
    print("🧪 Running API tests...")
    try:
        subprocess.run([sys.executable, "test_api.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Some tests failed")
    except FileNotFoundError:
        print("❌ test_api.py not found")

def main():
    """Main development startup function"""
    print("🎨 A2A AI Agent - Development Server")
    print("=" * 60)
    
    # Check Python version
    check_python_version()
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="A2A AI Agent Development Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run server on")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--test", action="store_true", help="Run tests instead of starting server")
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install:
        if not install_dependencies():
            sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run tests if requested
    if args.test:
        run_tests()
        return
    
    # Start server
    start_server(port=args.port, reload=not args.no_reload)

if __name__ == "__main__":
    main()