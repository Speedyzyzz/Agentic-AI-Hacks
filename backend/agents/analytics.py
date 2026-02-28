import logging
from typing import Dict, List
from sqlalchemy.orm import Session
from models import Campaign, Variant, PerformanceMetric
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_campaign_performance(campaign_id: str, db: Session) -> Dict:
    """
    Analyze campaign performance across variants and segments.
    
    Returns:
    - Best performing segment
    - Worst performing segment  
    - Improvement suggestions
    - Comparative metrics
    """
    logger.info(f"Analyzing performance for campaign: {campaign_id}")
    
    # Fetch campaign with all variants and metrics
    campaign = db.query(Campaign).filter_by(id=campaign_id).first()
    
    if not campaign:
        logger.error(f"Campaign {campaign_id} not found")
        return {"error": "Campaign not found"}
    
    if not campaign.variants:
        logger.warning(f"Campaign {campaign_id} has no variants")
        return {"error": "No variants found for analysis"}
    
    # Collect performance data per variant
    variant_performance = []
    
    for variant in campaign.variants:
        if not variant.metrics:
            logger.warning(f"Variant {variant.id} has no metrics yet")
            continue
        
        # Get latest metric
        latest_metric = variant.metrics[0]  # Assuming ordered by timestamp desc
        
        variant_performance.append({
            "variant_id": variant.id,
            "segment_name": variant.segment.segment_name if variant.segment else "unknown",
            "segment_id": variant.segment_id,
            "subject": variant.subject,
            "open_rate": latest_metric.open_rate,
            "click_rate": latest_metric.click_rate,
            "version": variant.version_number,
            "timestamp": latest_metric.timestamp
        })
    
    if not variant_performance:
        logger.warning("No performance metrics available for analysis")
        return {"error": "No metrics available", "status": "waiting_for_metrics"}
    
    # Sort by click rate (primary) and open rate (secondary)
    sorted_by_click = sorted(variant_performance, key=lambda x: (x['click_rate'], x['open_rate']), reverse=True)
    sorted_by_open = sorted(variant_performance, key=lambda x: x['open_rate'], reverse=True)
    
    best_variant = sorted_by_click[0]
    worst_variant = sorted_by_click[-1]
    
    # Calculate average performance
    avg_open_rate = sum(v['open_rate'] for v in variant_performance) / len(variant_performance)
    avg_click_rate = sum(v['click_rate'] for v in variant_performance) / len(variant_performance)
    
    # Calculate performance delta
    ctr_delta = best_variant['click_rate'] - worst_variant['click_rate']
    open_delta = best_variant['open_rate'] - worst_variant['open_rate']
    
    # Generate insights
    insights = _generate_insights(
        best_variant=best_variant,
        worst_variant=worst_variant,
        avg_open_rate=avg_open_rate,
        avg_click_rate=avg_click_rate,
        objective=campaign.objective
    )
    
    # Generate recommendations
    recommendations = _generate_recommendations(
        worst_variant=worst_variant,
        best_variant=best_variant,
        objective=campaign.objective,
        ctr_delta=ctr_delta
    )
    
    analysis = {
        "campaign_id": campaign_id,
        "campaign_objective": campaign.objective,
        "analyzed_at": datetime.utcnow().isoformat(),
        "total_variants": len(variant_performance),
        "best_performer": {
            "variant_id": best_variant['variant_id'],
            "segment": best_variant['segment_name'],
            "open_rate": best_variant['open_rate'],
            "click_rate": best_variant['click_rate'],
            "subject": best_variant['subject']
        },
        "worst_performer": {
            "variant_id": worst_variant['variant_id'],
            "segment": worst_variant['segment_name'],
            "open_rate": worst_variant['open_rate'],
            "click_rate": worst_variant['click_rate'],
            "subject": worst_variant['subject']
        },
        "averages": {
            "open_rate": avg_open_rate,
            "click_rate": avg_click_rate
        },
        "deltas": {
            "ctr_delta": ctr_delta,
            "open_delta": open_delta,
            "ctr_delta_percent": (ctr_delta / worst_variant['click_rate'] * 100) if worst_variant['click_rate'] > 0 else 0
        },
        "insights": insights,
        "recommendations": recommendations,
        "all_variants": variant_performance
    }
    
    logger.info(f"Analysis complete. Best: {best_variant['segment_name']} (CTR: {best_variant['click_rate']:.2%}), Worst: {worst_variant['segment_name']} (CTR: {worst_variant['click_rate']:.2%})")
    
    return analysis


def _generate_insights(
    best_variant: Dict,
    worst_variant: Dict,
    avg_open_rate: float,
    avg_click_rate: float,
    objective: str
) -> List[str]:
    """
    Generate actionable insights from performance data.
    
    Rule-based intelligence, not random observations.
    """
    insights = []
    
    # Insight 1: Best performer analysis
    if best_variant['click_rate'] > avg_click_rate * 1.2:
        insights.append(
            f"The {best_variant['segment_name']} segment significantly outperforms "
            f"average CTR by {((best_variant['click_rate'] / avg_click_rate - 1) * 100):.1f}%. "
            f"Subject line pattern: '{best_variant['subject']}' resonates strongly."
        )
    
    # Insight 2: Worst performer analysis
    if worst_variant['click_rate'] < avg_click_rate * 0.8:
        insights.append(
            f"The {worst_variant['segment_name']} segment underperforms average CTR by "
            f"{((1 - worst_variant['click_rate'] / avg_click_rate) * 100):.1f}%. "
            f"Requires optimization intervention."
        )
    
    # Insight 3: Open vs Click discrepancy
    if best_variant['open_rate'] > 0.3 and best_variant['click_rate'] < 0.1:
        insights.append(
            "High open rate but low click rate indicates subject line works but body content needs improvement."
        )
    
    if worst_variant['open_rate'] < 0.2:
        insights.append(
            f"Low open rate for {worst_variant['segment_name']} suggests subject line lacks appeal or arrives at wrong time."
        )
    
    # Insight 4: Objective alignment
    if "click" in objective.lower() and avg_click_rate < 0.10:
        insights.append(
            f"Campaign objective is click optimization but average CTR ({avg_click_rate:.2%}) is below industry benchmark (10%). Urgency and CTA need strengthening."
        )
    
    if "open" in objective.lower() and avg_open_rate < 0.25:
        insights.append(
            f"Campaign objective is open rate optimization but average open rate ({avg_open_rate:.2%}) is below benchmark (25%). Subject lines need more intrigue."
        )
    
    return insights


def _generate_recommendations(
    worst_variant: Dict,
    best_variant: Dict,
    objective: str,
    ctr_delta: float
) -> List[Dict]:
    """
    Generate specific, actionable recommendations for optimization.
    
    These drive the Optimizer Agent decisions.
    """
    recommendations = []
    
    # Recommendation 1: Subject line optimization
    if worst_variant['click_rate'] < 0.08:
        recommendations.append({
            "action": "regenerate_subject",
            "target_segment": worst_variant['segment_name'],
            "reasoning": f"CTR {worst_variant['click_rate']:.2%} below acceptable threshold. Increase urgency and clarity.",
            "priority": "high"
        })
    
    # Recommendation 2: Body content optimization
    if worst_variant['open_rate'] > 0.25 and worst_variant['click_rate'] < 0.10:
        recommendations.append({
            "action": "regenerate_body",
            "target_segment": worst_variant['segment_name'],
            "reasoning": "Open rate acceptable but clicks low. CTA placement and messaging need improvement.",
            "priority": "high"
        })
    
    # Recommendation 3: Send time adjustment
    if "click" in objective.lower() and worst_variant['click_rate'] < best_variant['click_rate'] * 0.7:
        recommendations.append({
            "action": "adjust_send_time",
            "target_segment": worst_variant['segment_name'],
            "reasoning": f"Significant CTR gap ({ctr_delta:.2%}). Test evening send time for better engagement.",
            "priority": "medium"
        })
    
    # Recommendation 4: Segment-specific messaging
    if "inactive" in worst_variant['segment_name'].lower() or "dormant" in worst_variant['segment_name'].lower():
        recommendations.append({
            "action": "increase_urgency",
            "target_segment": worst_variant['segment_name'],
            "reasoning": "Inactive segment requires higher urgency and re-engagement tactics.",
            "priority": "high"
        })
    
    # Recommendation 5: Learn from best performer
    if ctr_delta > 0.05:  # 5% or more difference
        recommendations.append({
            "action": "apply_winning_pattern",
            "target_segment": worst_variant['segment_name'],
            "reasoning": f"Apply subject line patterns from {best_variant['segment_name']} (CTR: {best_variant['click_rate']:.2%}) to underperforming segments.",
            "priority": "high"
        })
    
    return recommendations


def compare_variant_performance(variant_ids: List[int], db: Session) -> Dict:
    """
    Compare specific variants for A/B testing analysis.
    """
    logger.info(f"Comparing variants: {variant_ids}")
    
    variants_data = []
    
    for vid in variant_ids:
        variant = db.query(Variant).filter_by(id=vid).first()
        if not variant or not variant.metrics:
            continue
        
        latest_metric = variant.metrics[0]
        variants_data.append({
            "variant_id": vid,
            "subject": variant.subject,
            "segment": variant.segment.segment_name if variant.segment else "unknown",
            "open_rate": latest_metric.open_rate,
            "click_rate": latest_metric.click_rate,
            "version": variant.version_number
        })
    
    if len(variants_data) < 2:
        return {"error": "Need at least 2 variants with metrics for comparison"}
    
    # Determine winner
    winner = max(variants_data, key=lambda x: (x['click_rate'], x['open_rate']))
    loser = min(variants_data, key=lambda x: (x['click_rate'], x['open_rate']))
    
    improvement = ((winner['click_rate'] - loser['click_rate']) / loser['click_rate'] * 100) if loser['click_rate'] > 0 else 0
    
    return {
        "comparison": "A/B Test Results",
        "winner": winner,
        "loser": loser,
        "improvement_percent": improvement,
        "recommendation": f"Variant {winner['variant_id']} outperforms by {improvement:.1f}%. Apply winning elements to other segments."
    }
