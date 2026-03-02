"""
API Agent - Real CampaignX API Integration
Implements OpenAPI-based dynamic discovery with header authentication
"""

import json
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load OpenAPI Spec (source of truth)
OPENAPI_SPEC_PATH = os.path.join(os.path.dirname(__file__), "..", "openapi.json")
with open(OPENAPI_SPEC_PATH, "r") as f:
    OPENAPI_SPEC = json.load(f)

# Base URL - Replace with real URL once confirmed
BASE_URL = os.getenv("CAMPAIGNX_API_BASE_URL", "https://campaignx.inxiteout.ai")

# API Key from environment
API_KEY = os.getenv("CAMPAIGNX_API_KEY")


class APIAgent:
    """Real CampaignX API Client with dynamic endpoint discovery"""
    
    def __init__(self):
        """Initialize API Agent with OpenAPI specification"""
        self.spec = OPENAPI_SPEC
        self.base_url = BASE_URL
        self.api_key = API_KEY
        
    def discover_endpoints(self) -> List[str]:
        """
        Discover available API endpoints from OpenAPI spec
        
        Returns:
            List of endpoint paths
        """
        return list(self.spec.get('paths', {}).keys())
    
    def get_endpoint_details(self, endpoint: str) -> Dict:
        """
        Get details about a specific endpoint
        
        Args:
            endpoint: Endpoint path (e.g., '/api/v1/signup')
            
        Returns:
            Endpoint details including methods, parameters, schemas
        """
        return self.spec.get('paths', {}).get(endpoint, {})
    
    # ============================================
    # AUTHENTICATION
    # ============================================
    
    def signup(self, team_name: str, team_email: str) -> Dict:
        """
        Register team and generate API key (call once)
        
        Args:
            team_name: Team name (3-100 alphanumeric chars)
            team_email: Valid email address
            
        Returns:
            Response with api_key (shown only once)
        """
        url = f"{self.base_url}/api/v1/signup"
        payload = {
            "team_name": team_name,
            "team_email": team_email
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "message": "Signup failed"
            }
    
    # ============================================
    # CUSTOMER DATA
    # ============================================
    
    def get_customer_cohort(self) -> Dict:
        """
        Retrieve customer cohort data (MUST be called before every send)
        
        Rate limit: 100 calls/day
        Requires: Valid API key
        
        Returns:
            CustomerCohortResponse with data array
        """
        url = f"{self.base_url}/api/v1/get_customer_cohort"
        headers = {
            "x-api-key": self.api_key
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "message": "Failed to fetch customer cohort",
                "data": [],
                "total_count": 0
            }
    
    def fetch_customer_cohort(self) -> Dict:
        """Alias for backward compatibility"""
        return self.get_customer_cohort()
    
    # ============================================
    # CAMPAIGNS
    # ============================================
    
    def send_campaign(
        self,
        subject: str,
        body: str,
        customer_ids: List[str],
        send_time: str
    ) -> Dict:
        """
        Submit marketing campaign to targeted customer cohort
        
        Args:
            subject: Email subject (max 200 chars, supports emoji)
            body: Campaign message (1-5000 chars, supports emoji + URLs)
            customer_ids: List of customer IDs (must be from cohort, max 5000)
            send_time: Send time in format "DD:MM:YY HH:MM:SS" (IST, future)
        
        Rate limit: 100 calls/day
        Requires: Valid API key
        
        Returns:
            SendCampaignResponse with campaign_id
        """
        url = f"{self.base_url}/api/v1/send_campaign"
        headers = {
            "x-api-key": self.api_key
        }
        payload = {
            "subject": subject,
            "body": body,
            "list_customer_ids": customer_ids,
            "send_time": send_time
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "message": "Failed to send campaign",
                "campaign_id": None
            }
    
    def schedule_campaign(
        self,
        campaign_id: str,
        customer_ids: List[str],
        send_time: str
    ) -> Dict:
        """Alias for backward compatibility"""
        # Note: Real API doesn't have separate schedule endpoint
        # Use send_campaign instead
        return {
            "status": "use_send_campaign_instead",
            "message": "Call send_campaign() with subject, body, customer_ids, send_time"
        }
    
    # ============================================
    # REPORTS
    # ============================================
    
    def get_report(self, campaign_id: str) -> Dict:
        """
        Retrieve campaign performance report
        
        Args:
            campaign_id: Campaign ID from send_campaign response
        
        Rate limit: 100 calls/day
        Requires: Valid API key
        
        Returns:
            GetReportResponse with data array including EO/EC flags
        """
        url = f"{self.base_url}/api/v1/get_report"
        headers = {
            "x-api-key": self.api_key
        }
        params = {
            "campaign_id": campaign_id
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "message": "Failed to fetch report",
                "data": [],
                "total_rows": 0
            }
    
    def fetch_metrics(self, campaign_id: str) -> Dict:
        """
        Fetch campaign metrics from report data
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            Computed metrics (open_rate, click_rate) from real data
        """
        report = self.get_report(campaign_id)
        
        if "error" in report or not report.get("data"):
            return {
                "campaign_id": campaign_id,
                "error": report.get("error", "No data available"),
                "open_rate": 0.0,
                "click_rate": 0.0,
                "total_sent": 0
            }
        
        return self.compute_metrics(report)
    
    # ============================================
    # METRICS COMPUTATION (REAL DATA)
    # ============================================
    
    def compute_metrics(self, report_data: Dict) -> Dict:
        """
        Compute real performance metrics from report data
        
        Args:
            report_data: GetReportResponse from get_report()
        
        Returns:
            Computed metrics with open_rate and click_rate
        """
        rows = report_data.get("data", [])
        total = len(rows)
        
        if total == 0:
            return {
                "open_rate": 0.0,
                "click_rate": 0.0,
                "total_sent": 0,
                "opens": 0,
                "clicks": 0
            }
        
        opens = sum(1 for r in rows if r.get("EO") == "Y")
        clicks = sum(1 for r in rows if r.get("EC") == "Y")
        
        open_rate = opens / total
        click_rate = clicks / total
        
        return {
            "campaign_id": report_data.get("campaign_id"),
            "total_sent": total,
            "opens": opens,
            "clicks": clicks,
            "open_rate": open_rate,
            "click_rate": click_rate,
            "ctr": click_rate  # Click-through rate
        }
    
    # ============================================
    # UTILITIES
    # ============================================
    
    @staticmethod
    def generate_future_send_time(minutes: int = 5) -> str:
        """
        Generate future send time in required format
        
        Args:
            minutes: Minutes from now (default 5)
        
        Returns:
            Formatted time string "DD:MM:YY HH:MM:SS" (IST)
        """
        future = datetime.now() + timedelta(minutes=minutes)
        return future.strftime("%d:%m:%y %H:%M:%S")


# Global API agent instance
_api_agent = None

def get_api_agent() -> APIAgent:
    """Get singleton API agent instance"""
    global _api_agent
    if _api_agent is None:
        _api_agent = APIAgent()
    return _api_agent
