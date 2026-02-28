import json
import logging
from llm import call_llm

logger = logging.getLogger(__name__)

def parse_campaign_brief(brief: str):
    prompt = f"""
You are an AI campaign parser.

Extract structured campaign details from the following brief.
Return ONLY valid JSON. No explanation. No markdown.

Brief:
{brief}

Required fields:
- product_name (string)
- base_bonus (number or null)
- special_segment (string or null)
- special_bonus (number or null)
- objective (string)
"""

    try:
        response = call_llm(prompt)
        logger.info(f"LLM response: {response}")
        
        # Clean potential markdown code blocks
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()
        
        return json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return {"error": "Invalid JSON from LLM", "raw_output": response}
    except Exception as e:
        logger.error(f"Error parsing brief: {str(e)}")
        return {"error": str(e), "brief": brief}
