#!/usr/bin/env python3
"""
Test Real CampaignX API Integration
Verifies API client works with real endpoints
"""

import os
import sys
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.api_agent import APIAgent

def test_api_discovery():
    """Test OpenAPI spec discovery"""
    print("\n🔍 Test 1: API Discovery")
    print("=" * 50)
    
    agent = APIAgent()
    endpoints = agent.discover_endpoints()
    
    print(f"✅ Discovered {len(endpoints)} endpoints:")
    for ep in endpoints:
        print(f"   - {ep}")
    
    return len(endpoints) > 0

def test_get_customer_cohort():
    """Test customer cohort fetching"""
    print("\n👥 Test 2: Get Customer Cohort")
    print("=" * 50)
    
    agent = APIAgent()
    
    if not agent.api_key:
        print("⚠️  No API key found. Run signup.py first.")
        return False
    
    print(f"🔑 Using API key: {agent.api_key[:10]}...")
    print("⏳ Fetching customer cohort...")
    
    response = agent.get_customer_cohort()
    
    if "error" in response:
        print(f"❌ Error: {response['error']}")
        return False
    
    count = response.get("total_count", 0)
    print(f"✅ Success! Fetched {count} customers")
    
    if response.get("data"):
        sample = response["data"][0]
        print(f"\n📋 Sample customer:")
        print(json.dumps(sample, indent=2))
    
    return True

def test_send_time_generation():
    """Test send time formatting"""
    print("\n⏰ Test 3: Send Time Generation")
    print("=" * 50)
    
    agent = APIAgent()
    send_time = agent.generate_future_send_time(minutes=10)
    
    print(f"✅ Generated send time (10 min from now): {send_time}")
    print(f"   Format: DD:MM:YY HH:MM:SS (IST)")
    
    return True

def test_send_campaign():
    """Test campaign sending (dry run - don't actually send)"""
    print("\n📧 Test 4: Send Campaign Format")
    print("=" * 50)
    
    agent = APIAgent()
    
    # Get cohort first
    cohort = agent.get_customer_cohort()
    if "error" in cohort or not cohort.get("data"):
        print("⚠️  Cannot test send without valid cohort")
        return False
    
    # Get first 5 customer IDs
    customer_ids = [c["customer_id"] for c in cohort["data"][:5]]
    
    print(f"📝 Would send to {len(customer_ids)} customers:")
    print(f"   Customer IDs: {customer_ids}")
    
    send_time = agent.generate_future_send_time(minutes=10)
    print(f"   Send time: {send_time}")
    print(f"   Subject: 'Test Campaign'")
    print(f"   Body: 'This is a test campaign body'")
    
    print(f"\n⚠️  Not actually sending (remove this check to send)")
    print(f"   To send: agent.send_campaign(subject, body, customer_ids, send_time)")
    
    return True

def main():
    print("🧪 CampaignX API Integration Tests")
    print("=" * 50)
    
    tests = [
        ("API Discovery", test_api_discovery),
        ("Get Customer Cohort", test_get_customer_cohort),
        ("Send Time Generation", test_send_time_generation),
        ("Send Campaign Format", test_send_campaign),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    print(f"\n🎯 Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! API integration ready.")
    else:
        print("\n⚠️  Some tests failed. Check API key and configuration.")

if __name__ == "__main__":
    main()
