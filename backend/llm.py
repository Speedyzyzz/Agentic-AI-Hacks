import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY", "YOUR_API_KEY")

def call_llm(prompt: str):
    if API_KEY == "YOUR_API_KEY":
        logger.warning("No API key set. Set OPENROUTER_API_KEY environment variable.")
        # Return mock response for testing
        return '{"product_name": "XDeposit", "base_bonus": 1.0, "special_segment": "female senior citizens", "special_bonus": 0.25, "objective": "optimize for click rate"}'
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()

        # Extract actual message content
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"LLM call failed: {str(e)}")
        raise
