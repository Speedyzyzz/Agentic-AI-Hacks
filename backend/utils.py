"""
Utility functions for agent logging and error handling
"""
import logging
import json
from sqlalchemy.orm import Session
from models import AgentLog
from datetime import datetime
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_agent_decision(
    db: Session,
    campaign_id: str,
    agent_name: str,
    decision: str,
    reasoning: str,
    metadata: dict = None
):
    """
    Log agent decision for transparency and demo.
    
    Critical for showing judges the intelligence process.
    """
    try:
        log_entry = AgentLog(
            campaign_id=campaign_id,
            agent_name=agent_name,
            decision=decision,
            reasoning=reasoning,
            metadata_json=json.dumps(metadata) if metadata else None
        )
        db.add(log_entry)
        db.flush()
        
        logger.info(f"[{agent_name.upper()}] {decision}: {reasoning}")
        
        return log_entry.id
        
    except Exception as e:
        logger.error(f"Failed to log agent decision: {str(e)}")
        # Non-critical - don't fail the main operation
        return None


def get_agent_logs(db: Session, campaign_id: str) -> list:
    """
    Retrieve all agent logs for a campaign.
    
    Used for demo transparency.
    """
    try:
        logs = db.query(AgentLog).filter_by(campaign_id=campaign_id).order_by(AgentLog.timestamp).all()
        
        return [
            {
                "id": log.id,
                "agent_name": log.agent_name,
                "decision": log.decision,
                "reasoning": log.reasoning,
                "timestamp": log.timestamp.isoformat(),
                "metadata": json.loads(log.metadata_json) if log.metadata_json else None
            }
            for log in logs
        ]
        
    except Exception as e:
        logger.error(f"Failed to retrieve agent logs: {str(e)}")
        return []


def safe_llm_call(fallback_response=None):
    """
    Decorator for safe LLM calls with fallback logic.
    
    Ensures system never crashes on LLM failure.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"LLM call failed in {func.__name__}: {str(e)}")
                if fallback_response:
                    logger.warning(f"Using fallback response")
                    return fallback_response
                else:
                    raise
        return wrapper
    return decorator


def safe_api_call(fallback_response=None):
    """
    Decorator for safe API calls with fallback logic.
    
    Ensures system degrades gracefully.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"API call failed in {func.__name__}: {str(e)}")
                if fallback_response:
                    logger.warning(f"Using fallback response")
                    return fallback_response
                else:
                    # Return error dict instead of raising
                    return {"error": str(e), "fallback": True}
        return wrapper
    return decorator


def validate_campaign_data(campaign_id: str, db: Session) -> dict:
    """
    Validate campaign exists and has required data.
    
    Returns validation result with error details.
    """
    from models import Campaign
    
    result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    campaign = db.query(Campaign).filter_by(id=campaign_id).first()
    
    if not campaign:
        result["valid"] = False
        result["errors"].append("Campaign not found")
        return result
    
    if not campaign.segments or len(campaign.segments) == 0:
        result["valid"] = False
        result["errors"].append("No segments defined")
    
    if not campaign.variants or len(campaign.variants) == 0:
        result["valid"] = False
        result["errors"].append("No variants created")
    
    # Check for metrics (warning only)
    has_metrics = any(len(v.metrics) > 0 for v in campaign.variants)
    if not has_metrics:
        result["warnings"].append("No performance metrics available yet")
    
    return result


def safe_division(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safe division that never crashes on zero.
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except:
        return default


def format_percentage(value: float) -> str:
    """
    Format decimal as percentage for display.
    """
    try:
        return f"{value * 100:.1f}%"
    except:
        return "0.0%"


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp value between min and max.
    """
    return max(min_val, min(max_val, value))
