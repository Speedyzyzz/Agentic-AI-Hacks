#!/usr/bin/env python3
"""
CampaignX API Signup Script
Run this ONCE to register your team and get your API key
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.api_agent import APIAgent

def main():
    print("🔐 CampaignX API Signup")
    print("=" * 50)
    
    team_name = input("Enter your team name: ").strip()
    team_email = input("Enter your team email: ").strip()
    
    if not team_name or not team_email:
        print("❌ Team name and email are required")
        return
    
    print(f"\n📝 Registering team: {team_name}")
    print(f"📧 Email: {team_email}")
    print("\n⏳ Contacting API...")
    
    # Create API agent (no key needed for signup)
    agent = APIAgent()
    agent.api_key = None  # Signup doesn't need API key
    
    # Call signup
    response = agent.signup(team_name, team_email)
    
    if "error" in response:
        print(f"\n❌ Signup failed: {response['error']}")
        print(f"   Message: {response.get('message', 'Unknown error')}")
        return
    
    api_key = response.get("api_key")
    if not api_key:
        print(f"\n❌ No API key received")
        print(f"Response: {response}")
        return
    
    print(f"\n✅ Signup successful!")
    print(f"\n🔑 YOUR API KEY (save this - shown only once):")
    print(f"   {api_key}")
    
    # Write to .env file
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    
    with open(env_path, "w") as f:
        f.write(f"# CampaignX API Configuration\n")
        f.write(f"# Generated: {response.get('created_at', 'now')}\n\n")
        f.write(f"CAMPAIGNX_API_BASE_URL=https://campaignx.inxiteout.ai\n")
        f.write(f"CAMPAIGNX_API_KEY={api_key}\n")
        f.write(f"CAMPAIGNX_TEAM_NAME={team_name}\n")
        f.write(f"CAMPAIGNX_TEAM_EMAIL={team_email}\n")
    
    print(f"\n💾 Configuration saved to: {env_path}")
    print(f"\n✨ You're ready to use the CampaignX API!")
    print(f"\n⚠️  IMPORTANT:")
    print(f"   - Rate limit: 100 calls/day")
    print(f"   - API key was also sent to {team_email}")
    print(f"   - Keep your API key secure")

if __name__ == "__main__":
    main()
