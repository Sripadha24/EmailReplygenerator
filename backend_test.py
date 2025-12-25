import requests
import sys
import json
from datetime import datetime

class EmailReplyGeneratorTester:
    def __init__(self, base_url="https://replybuddy-4.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

    def test_api_root(self):
        """Test API root endpoint"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Response: {response.text[:100]}"
            self.log_test("API Root Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("API Root Endpoint", False, str(e))
            return False

    def test_generate_reply_valid_input(self):
        """Test generate reply with valid input"""
        test_data = {
            "email_situation": "I received a meeting invitation for next Tuesday but I have a conflict. I need to politely decline and suggest an alternative time.",
            "tone": "formal"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/generate-reply",
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                has_reply = 'reply' in data and len(data['reply'].strip()) > 0
                success = has_reply
                details = f"Status: {response.status_code}, Reply length: {len(data.get('reply', ''))}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Generate Reply - Valid Input", success, details)
            return success
        except Exception as e:
            self.log_test("Generate Reply - Valid Input", False, str(e))
            return False

    def test_generate_reply_empty_input(self):
        """Test generate reply with empty input - should return 400"""
        test_data = {
            "email_situation": "",
            "tone": "formal"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/generate-reply",
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            success = response.status_code == 400
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Generate Reply - Empty Input Validation", success, details)
            return success
        except Exception as e:
            self.log_test("Generate Reply - Empty Input Validation", False, str(e))
            return False

    def test_generate_reply_different_tones(self):
        """Test generate reply with different tones"""
        tones = ["formal", "semi-formal", "friendly"]
        all_passed = True
        
        for tone in tones:
            test_data = {
                "email_situation": "Thank you for your email. I wanted to follow up on our previous discussion.",
                "tone": tone
            }
            
            try:
                response = requests.post(
                    f"{self.api_url}/generate-reply",
                    json=test_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                success = response.status_code == 200
                if success:
                    data = response.json()
                    has_reply = 'reply' in data and len(data['reply'].strip()) > 0
                    success = has_reply
                
                details = f"Tone: {tone}, Status: {response.status_code}"
                self.log_test(f"Generate Reply - {tone.title()} Tone", success, details)
                
                if not success:
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Generate Reply - {tone.title()} Tone", False, str(e))
                all_passed = False
        
        return all_passed

    def test_generate_reply_invalid_tone(self):
        """Test generate reply with invalid tone - should still work with default"""
        test_data = {
            "email_situation": "Test email situation",
            "tone": "invalid_tone"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/generate-reply",
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            # Should still work, just use default tone
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            self.log_test("Generate Reply - Invalid Tone Handling", success, details)
            return success
        except Exception as e:
            self.log_test("Generate Reply - Invalid Tone Handling", False, str(e))
            return False

    def test_cors_headers(self):
        """Test CORS headers are present"""
        try:
            response = requests.options(f"{self.api_url}/generate-reply", timeout=10)
            cors_headers = [
                'access-control-allow-origin',
                'access-control-allow-methods',
                'access-control-allow-headers'
            ]
            
            has_cors = any(header in response.headers for header in cors_headers)
            details = f"Status: {response.status_code}, CORS headers present: {has_cors}"
            self.log_test("CORS Headers", has_cors, details)
            return has_cors
        except Exception as e:
            self.log_test("CORS Headers", False, str(e))
            return False

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Email Reply Generator Backend Tests")
        print(f"Testing against: {self.base_url}")
        print("=" * 60)
        
        # Test API availability first
        if not self.test_api_root():
            print("❌ API is not accessible. Stopping tests.")
            return False
        
        # Run all tests
        self.test_generate_reply_valid_input()
        self.test_generate_reply_empty_input()
        self.test_generate_reply_different_tones()
        self.test_generate_reply_invalid_tone()
        self.test_cors_headers()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return True
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed")
            return False

def main():
    tester = EmailReplyGeneratorTester()
    success = tester.run_all_tests()
    
    # Save detailed results
    with open('/app/backend_test_results.json', 'w') as f:
        json.dump({
            'summary': {
                'total_tests': tester.tests_run,
                'passed_tests': tester.tests_passed,
                'success_rate': f"{(tester.tests_passed/tester.tests_run)*100:.1f}%" if tester.tests_run > 0 else "0%",
                'timestamp': datetime.now().isoformat()
            },
            'test_results': tester.test_results
        }, f, indent=2)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())