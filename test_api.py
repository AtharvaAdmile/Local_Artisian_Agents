#!/usr/bin/env python3
"""
Simple test script for A2A AI Agent FastAPI
Tests basic functionality without requiring full setup
"""

import requests
import json
import time
from typing import Dict, Any

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health(self) -> bool:
        """Test health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
    
    def test_root(self) -> bool:
        """Test root endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            return response.status_code == 200 and "A2A AI Agent" in response.text
        except Exception as e:
            print(f"Root endpoint failed: {e}")
            return False
    
    def test_craft_types(self) -> bool:
        """Test craft types endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/craft-types")
            if response.status_code == 200:
                data = response.json()
                return "craft_types" in data and len(data["craft_types"]) > 0
            return False
        except Exception as e:
            print(f"Craft types test failed: {e}")
            return False
    
    def test_create_profile(self) -> str:
        """Test profile creation"""
        try:
            profile_data = {
                "name": "Test Artisan",
                "location": "Mumbai, India",
                "specialization": "pottery",
                "experience_years": 5,
                "signature_style": "Traditional terracotta pottery",
                "target_audience": "Home decor enthusiasts",
                "social_media_platforms": ["instagram", "facebook"]
            }
            
            response = self.session.post(
                f"{self.base_url}/api/profiles",
                json=profile_data
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("profile_id")
            else:
                print(f"Profile creation failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Profile creation test failed: {e}")
            return None
    
    def test_list_profiles(self) -> bool:
        """Test profile listing"""
        try:
            response = self.session.get(f"{self.base_url}/api/profiles")
            return response.status_code == 200
        except Exception as e:
            print(f"Profile listing test failed: {e}")
            return False
    
    def test_dashboard(self) -> bool:
        """Test dashboard endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/dashboard")
            if response.status_code == 200:
                data = response.json()
                required_keys = ["total_artisans", "craft_types", "system_status"]
                return all(key in data for key in required_keys)
            return False
        except Exception as e:
            print(f"Dashboard test failed: {e}")
            return False
    
    def test_content_strategy(self, profile_id: str) -> bool:
        """Test content strategy generation"""
        if not profile_id:
            return False
        
        try:
            response = self.session.get(f"{self.base_url}/api/content-strategy/{profile_id}")
            if response.status_code == 200:
                data = response.json()
                return "recommendations" in data
            return False
        except Exception as e:
            print(f"Content strategy test failed: {e}")
            return False
    
    def cleanup_profile(self, profile_id: str) -> bool:
        """Clean up test profile"""
        if not profile_id:
            return True
        
        try:
            response = self.session.delete(f"{self.base_url}/api/profiles/{profile_id}")
            return response.status_code == 200
        except Exception as e:
            print(f"Profile cleanup failed: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all tests and return results"""
        results = {}
        profile_id = None
        
        print("🧪 Running API Tests...")
        print("=" * 50)
        
        # Basic connectivity tests
        print("Testing basic endpoints...")
        results["health"] = self.test_health()
        print(f"  Health check: {'✅' if results['health'] else '❌'}")
        
        results["root"] = self.test_root()
        print(f"  Root endpoint: {'✅' if results['root'] else '❌'}")
        
        results["craft_types"] = self.test_craft_types()
        print(f"  Craft types: {'✅' if results['craft_types'] else '❌'}")
        
        # Profile management tests
        print("\nTesting profile management...")
        profile_id = self.test_create_profile()
        results["create_profile"] = profile_id is not None
        print(f"  Create profile: {'✅' if results['create_profile'] else '❌'}")
        
        results["list_profiles"] = self.test_list_profiles()
        print(f"  List profiles: {'✅' if results['list_profiles'] else '❌'}")
        
        # Dashboard test
        print("\nTesting dashboard...")
        results["dashboard"] = self.test_dashboard()
        print(f"  Dashboard: {'✅' if results['dashboard'] else '❌'}")
        
        # Content strategy test (requires AI services)
        print("\nTesting AI features...")
        results["content_strategy"] = self.test_content_strategy(profile_id)
        print(f"  Content strategy: {'✅' if results['content_strategy'] else '❌'}")
        
        # Cleanup
        print("\nCleaning up...")
        cleanup_success = self.cleanup_profile(profile_id)
        print(f"  Cleanup: {'✅' if cleanup_success else '❌'}")
        
        # Summary
        print("\n" + "=" * 50)
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        print(f"Tests passed: {passed}/{total}")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed. Check the logs above.")
        
        return results

def main():
    """Main test function"""
    import sys
    
    # Get base URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"Testing API at: {base_url}")
    
    # Wait for server to be ready
    tester = APITester(base_url)
    
    print("Waiting for server to be ready...")
    for i in range(30):  # Wait up to 30 seconds
        if tester.test_health():
            print("✅ Server is ready!")
            break
        time.sleep(1)
        print(f"  Waiting... ({i+1}/30)")
    else:
        print("❌ Server not responding. Make sure it's running.")
        sys.exit(1)
    
    # Run tests
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()