import logging
from datetime import datetime, timedelta
from llm import call_llm
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def determine_send_time(objective: str) -> str:
    """
    Deterministic logic for optimal send time based on objective.
    
    Rules:
    - click_rate optimization: Evening (6 PM) when users are more engaged
    - open_rate optimization: Morning (9 AM) for inbox visibility
    - conversion optimization: Afternoon (2 PM) during decision-making hours
    """
    now = datetime.utcnow()
    
    # Calculate next optimal day (skip weekends for B2B campaigns)
    next_day = now + timedelta(days=1)
    while next_day.weekday() >= 5:  # Skip Saturday (5) and Sunday (6)
        next_day += timedelta(days=1)
    
    objective_lower = objective.lower()
    
    if "click" in objective_lower or "ctr" in objective_lower:
        # Evening send for higher engagement
        send_time = next_day.replace(hour=18, minute=0, second=0, microsecond=0)
        reasoning = "Evening send (6 PM) optimizes for click engagement"
    elif "open" in objective_lower:
        # Morning send for inbox visibility
        send_time = next_day.replace(hour=9, minute=0, second=0, microsecond=0)
        reasoning = "Morning send (9 AM) maximizes open rate visibility"
    elif "conversion" in objective_lower or "deposit" in objective_lower:
        # Afternoon send for decision-making
        send_time = next_day.replace(hour=14, minute=0, second=0, microsecond=0)
        reasoning = "Afternoon send (2 PM) targets decision-making window"
    else:
        # Default: mid-morning
        send_time = next_day.replace(hour=10, minute=0, second=0, microsecond=0)
        reasoning = "Standard send time for general campaigns"
    
    return send_time.isoformat(), reasoning


def extract_segments(parsed_brief: dict) -> list:
    """
    Deterministic segment extraction from parsed brief.
    
    Always explicit, never random.
    """
    segments = []
    
    # Rule 1: If special segment exists, create it explicitly
    special_segment = parsed_brief.get("special_segment")
    special_bonus = parsed_brief.get("special_bonus")
    
    if special_segment and special_segment.lower() != "null":
        segments.append({
            "name": special_segment,
            "criteria": f"Customers matching: {special_segment}",
            "reasoning": f"Special bonus of {special_bonus} mentioned explicitly in brief",
            "priority": "high"
        })
    
    # Rule 2: Always create general fallback segment
    segments.append({
        "name": "general_customers",
        "criteria": "All other eligible customers",
        "reasoning": "Default base segment for standard campaign reach",
        "priority": "standard"
    })
    
    return segments


def generate_strategy_reasoning(parsed_brief: dict, segments: list, send_time_info: dict) -> str:
    """
    Use LLM to generate high-level strategy reasoning.
    
    This is where LLM adds value: synthesizing the plan into strategic narrative.
    """
    prompt = f"""
You are a campaign strategy advisor.

Given this campaign plan, provide strategic reasoning for the approach.

Campaign Details:
- Product: {parsed_brief.get('product_name')}
- Objective: {parsed_brief.get('objective')}
- Base Bonus: {parsed_brief.get('base_bonus')}
- Special Segment: {parsed_brief.get('special_segment')}
- Special Bonus: {parsed_brief.get('special_bonus')}

Planned Segments:
{json.dumps(segments, indent=2)}

Send Time: {send_time_info['time']}
Reasoning: {send_time_info['reasoning']}

Provide a 2-3 sentence strategic reasoning that explains:
1. Why this segmentation approach maximizes {parsed_brief.get('objective')}
2. How the timing and targeting work together

Be specific and actionable. No fluff.
"""

    try:
        reasoning = call_llm(prompt)
        return reasoning.strip()
    except Exception as e:
        logger.error(f"LLM strategy reasoning failed: {str(e)}")
        # Fallback to deterministic reasoning
        return f"Multi-segment approach targeting {len(segments)} distinct cohorts with optimized send time to maximize {parsed_brief.get('objective')}."


def plan_campaign(parsed_brief: dict) -> dict:
    """
    Main campaign planning function.
    
    Combines:
    - Deterministic segmentation logic
    - Strategic send time calculation
    - LLM-powered reasoning
    
    Returns structured campaign plan.
    """
    logger.info(f"Planning campaign for: {parsed_brief.get('product_name')}")
    
    # Step 1: Extract segments deterministically
    segments = extract_segments(parsed_brief)
    logger.info(f"Extracted {len(segments)} segments")
    
    # Step 2: Determine optimal send time
    objective = parsed_brief.get("objective", "engagement")
    send_time, send_time_reasoning = determine_send_time(objective)
    logger.info(f"Optimal send time: {send_time}")
    
    # Step 3: Determine A/B variant count
    # More segments = more variants for testing
    ab_variants = min(len(segments) * 2, 4)  # Cap at 4 variants
    
    # Step 4: Generate strategic reasoning via LLM
    send_time_info = {
        "time": send_time,
        "reasoning": send_time_reasoning
    }
    
    strategy_reasoning = generate_strategy_reasoning(
        parsed_brief, 
        segments, 
        send_time_info
    )
    logger.info("Strategy reasoning generated")
    
    # Return structured plan
    plan = {
        "segments": segments,
        "send_time": send_time,
        "send_time_reasoning": send_time_reasoning,
        "ab_variants": ab_variants,
        "strategy_reasoning": strategy_reasoning,
        "objective": objective,
        "product_name": parsed_brief.get("product_name")
    }
    
    logger.info("Campaign plan completed")
    return plan


def validate_plan(plan: dict) -> bool:
    """
    Validate that plan meets quality standards.
    
    Ensures no shallow outputs.
    """
    required_fields = ["segments", "send_time", "strategy_reasoning", "objective"]
    
    for field in required_fields:
        if field not in plan:
            logger.error(f"Plan missing required field: {field}")
            return False
    
    if len(plan["segments"]) < 1:
        logger.error("Plan must have at least 1 segment")
        return False
    
    if len(plan["strategy_reasoning"]) < 50:
        logger.error("Strategy reasoning too shallow")
        return False
    
    return True
