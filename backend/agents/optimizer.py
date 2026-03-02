"""
SIMPLIFIED OPTIMIZER - Under 150 lines
SURGICAL: Fix only what's broken
NO COMPLEXITY: Linear logic only
FLEXIBLE: Optimization objective driven by campaign goal
"""
import logging
from typing import Dict
from sqlalchemy.orm import Session
from models import Campaign, Variant, PerformanceMetric
from datetime import datetime
from utils import log_agent_decision

logger = logging.getLogger(__name__)

# Thresholds
LOW_OPEN_THRESHOLD = 0.25
LOW_CTR_THRESHOLD = 0.08


def optimize_campaign_simple(campaign_id: str, db: Session, optimization_objective: str = None) -> Dict:
    """
    SIMPLIFIED OPTIMIZER - OBJECTIVE-AWARE
    1. Find worst variant (based on campaign objective)
    2. Identify problem
    3. Fix surgically
    
    Args:
        campaign_id: Campaign to optimize
        db: Database session
        optimization_objective: Override campaign objective (e.g., "open_rate", "click_rate", "both")
    """
    try:
        logger.info(f"=== OPTIMIZER: Campaign {campaign_id} ===")
        
        # Get campaign
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            return {"optimized": False, "error": "Campaign not found"}
        
        # Determine optimization objective from campaign or override
        if optimization_objective:
            objective = optimization_objective.lower()
        elif campaign.objective:
            # Parse campaign objective
            obj_lower = campaign.objective.lower()
            if "open" in obj_lower:
                objective = "open_rate"
            elif "click" in obj_lower or "ctr" in obj_lower:
                objective = "click_rate"
            else:
                objective = "both"  # Default: optimize both
        else:
            objective = "click_rate"  # Fallback default
        
        logger.info(f"Optimization objective: {objective}")
        
        # Get all variants with their latest metrics
        variants = db.query(Variant).filter(Variant.campaign_id == campaign_id).all()
        
        if not variants:
            return {"optimized": False, "reason": "No variants found"}
        
        # Find worst performer BASED ON OBJECTIVE
        worst_variant = None
        worst_score = 999
        
        for variant in variants:
            if variant.metrics:
                latest_metric = variant.metrics[0]
                
                # Calculate score based on objective
                if objective == "open_rate":
                    score = latest_metric.open_rate
                elif objective == "click_rate":
                    score = latest_metric.click_rate
                else:  # both
                    score = (latest_metric.open_rate + latest_metric.click_rate) / 2
                
                if score < worst_score:
                    worst_score = score
                    worst_variant = variant
        
        if not worst_variant or not worst_variant.metrics:
            return {"optimized": False, "reason": "No metrics available"}
        
        # Get metrics
        latest_metric = worst_variant.metrics[0]
        open_rate = latest_metric.open_rate
        click_rate = latest_metric.click_rate
        
        logger.info(f"Worst variant (for {objective}): {worst_variant.id} - Open={open_rate:.2%}, CTR={click_rate:.2%}")
        
        # DETERMINE PROBLEM TYPE BASED ON OBJECTIVE
        problem_type = None
        actions = []
        
        if objective == "open_rate":
            # Only care about open rate
            if open_rate < LOW_OPEN_THRESHOLD:
                problem_type = "low_open"
                actions = ["regenerate_subject"]
            else:
                log_agent_decision(
                    db=db,
                    campaign_id=campaign_id,
                    agent_name="optimizer",
                    decision="No optimization needed",
                    reasoning=f"Open rate acceptable: {open_rate:.2%} (target: {LOW_OPEN_THRESHOLD:.0%})"
                )
                return {
                    "optimized": False,
                    "reason": "Open rate meets threshold",
                    "objective": objective,
                    "metrics": {"open_rate": open_rate}
                }
        
        elif objective == "click_rate":
            # Only care about CTR
            if click_rate < LOW_CTR_THRESHOLD:
                problem_type = "low_click"
                actions = ["regenerate_body"]
            else:
                log_agent_decision(
                    db=db,
                    campaign_id=campaign_id,
                    agent_name="optimizer",
                    decision="No optimization needed",
                    reasoning=f"Click rate acceptable: {click_rate:.2%} (target: {LOW_CTR_THRESHOLD:.0%})"
                )
                return {
                    "optimized": False,
                    "reason": "Click rate meets threshold",
                    "objective": objective,
                    "metrics": {"click_rate": click_rate}
                }
        
        else:  # both
            # Care about both metrics
            if open_rate < LOW_OPEN_THRESHOLD and click_rate < LOW_CTR_THRESHOLD:
                problem_type = "both_low"
                actions = ["regenerate_subject", "regenerate_body"]
            elif open_rate < LOW_OPEN_THRESHOLD:
                problem_type = "low_open"
                actions = ["regenerate_subject"]
            elif click_rate < LOW_CTR_THRESHOLD:
                problem_type = "low_click"
                actions = ["regenerate_body"]
            else:
                # Performance acceptable
                log_agent_decision(
                    db=db,
                    campaign_id=campaign_id,
                    agent_name="optimizer",
                    decision="No optimization needed",
                    reasoning=f"Performance acceptable: Open={open_rate:.2%}, CTR={click_rate:.2%}"
                )
                return {
                    "optimized": False,
                    "reason": "Performance meets thresholds",
                    "objective": objective,
                    "metrics": {"open_rate": open_rate, "click_rate": click_rate}
                }
        
        logger.info(f"Problem type: {problem_type} - Actions: {actions} (Objective: {objective})")
        
        # Log optimization trigger
        log_agent_decision(
            db=db,
            campaign_id=campaign_id,
            agent_name="optimizer",
            decision=f"Optimization triggered: {problem_type} (objective: {objective})",
            reasoning=f"Optimizing for {objective} - Open={open_rate:.2%}, CTR={click_rate:.2%}"
        )
        
        # APPLY SURGICAL FIX
        new_subject = worst_variant.subject
        new_body = worst_variant.body
        
        if "regenerate_subject" in actions:
            # Add numeric hook and question
            product = campaign.product_name
            new_subject = f"🎯 {product}: Get 15% More Returns - Limited Time?"
            logger.info(f"New subject: {new_subject}")
        
        if "regenerate_body" in actions:
            # Add urgency and early CTA
            product = campaign.product_name
            new_body = f"""URGENT: Exclusive Offer Inside

Click here to activate your {product} benefits NOW.

Limited time: 15% bonus returns for early applicants.

This offer expires in 48 hours. Don't miss out.

[APPLY NOW] → Get Started

Why wait? Join thousands who've already upgraded."""
            logger.info("New body generated with early CTA")
        
        # Create new variant
        new_version = worst_variant.version_number + 1
        
        new_variant = Variant(
            campaign_id=campaign_id,
            segment_id=worst_variant.segment_id,
            subject=new_subject,
            body=new_body,
            send_time=worst_variant.send_time,
            version_number=new_version
        )
        
        db.add(new_variant)
        db.flush()
        
        campaign.status = "optimized"
        db.commit()
        db.refresh(new_variant)
        
        # Log success
        log_agent_decision(
            db=db,
            campaign_id=campaign_id,
            agent_name="optimizer",
            decision=f"Created v{new_version} (objective: {objective})",
            reasoning=f"Fixed {problem_type}: {', '.join(actions)}"
        )
        
        logger.info(f"✓ Optimization complete: v{worst_variant.version_number} → v{new_version} (objective: {objective})")
        
        return {
            "optimized": True,
            "objective": objective,
            "problem_type": problem_type,
            "actions": actions,
            "original_variant_id": worst_variant.id,
            "new_variant_id": new_variant.id,
            "version": {
                "from": worst_variant.version_number,
                "to": new_version
            },
            "original_metrics": {
                "open_rate": open_rate,
                "click_rate": click_rate
            }
        }
        
    except Exception as e:
        logger.error(f"Optimizer failed: {str(e)}")
        db.rollback()
        return {"optimized": False, "error": str(e)}
