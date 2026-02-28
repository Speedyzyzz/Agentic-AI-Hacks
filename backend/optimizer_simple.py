"""
SIMPLIFIED OPTIMIZER - Under 150 lines
SURGICAL: Fix only what's broken
NO COMPLEXITY: Linear logic only
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


def optimize_campaign_simple(campaign_id: str, db: Session) -> Dict:
    """
    SIMPLIFIED OPTIMIZER
    1. Find worst variant
    2. Identify problem
    3. Fix surgically
    """
    try:
        logger.info(f"=== OPTIMIZER: Campaign {campaign_id} ===")
        
        # Get campaign
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            return {"optimized": False, "error": "Campaign not found"}
        
        # Get all variants with their latest metrics
        variants = db.query(Variant).filter(Variant.campaign_id == campaign_id).all()
        
        if not variants:
            return {"optimized": False, "reason": "No variants found"}
        
        # Find worst performer
        worst_variant = None
        worst_ctr = 999
        
        for variant in variants:
            if variant.metrics:
                latest_metric = variant.metrics[0]
                if latest_metric.click_rate < worst_ctr:
                    worst_ctr = latest_metric.click_rate
                    worst_variant = variant
        
        if not worst_variant or not worst_variant.metrics:
            return {"optimized": False, "reason": "No metrics available"}
        
        # Get metrics
        latest_metric = worst_variant.metrics[0]
        open_rate = latest_metric.open_rate
        click_rate = latest_metric.click_rate
        
        logger.info(f"Worst variant: {worst_variant.id} - Open={open_rate:.2%}, CTR={click_rate:.2%}")
        
        # DETERMINE PROBLEM TYPE
        problem_type = None
        actions = []
        
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
                "metrics": {"open_rate": open_rate, "click_rate": click_rate}
            }
        
        logger.info(f"Problem type: {problem_type} - Actions: {actions}")
        
        # Log optimization trigger
        log_agent_decision(
            db=db,
            campaign_id=campaign_id,
            agent_name="optimizer",
            decision=f"Optimization triggered: {problem_type}",
            reasoning=f"Open={open_rate:.2%} (need >{LOW_OPEN_THRESHOLD:.0%}), CTR={click_rate:.2%} (need >{LOW_CTR_THRESHOLD:.0%})"
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
            decision=f"Created v{new_version}",
            reasoning=f"Fixed {problem_type}: {', '.join(actions)}"
        )
        
        logger.info(f"✓ Optimization complete: v{worst_variant.version_number} → v{new_version}")
        
        return {
            "optimized": True,
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
