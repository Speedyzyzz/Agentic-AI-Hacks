import logging
from typing import List, Dict
from llm import call_llm
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def determine_content_strategy(objective: str, segment_name: str) -> Dict:
    """
    Deterministic strategy rules BEFORE LLM call.
    
    LLM does NOT decide strategy - it only fills creative text.
    """
    strategy = {
        "tone": "professional",
        "subject_style": "benefit-first",
        "cta_placement": "mid-body",
        "emphasis": "standard"
    }
    
    # Rule 1: Objective-based strategy
    objective_lower = objective.lower()
    
    if "click" in objective_lower or "ctr" in objective_lower:
        strategy.update({
            "tone": "urgent, action-driven",
            "subject_style": "short, numeric, benefit-first",
            "language": "scarcity and urgency",
            "cta_placement": "early in body",
            "subject_length": "max 60 characters",
            "urgency_level": "high"
        })
    elif "open" in objective_lower:
        strategy.update({
            "tone": "curiosity-driven",
            "subject_style": "question format or teaser",
            "language": "intrigue and benefit tease",
            "cta_placement": "mid-body",
            "subject_length": "max 70 characters",
            "urgency_level": "medium"
        })
    elif "conversion" in objective_lower:
        strategy.update({
            "tone": "persuasive, trust-building",
            "subject_style": "value proposition clear",
            "language": "benefit and proof",
            "cta_placement": "end of body with clear action",
            "urgency_level": "medium"
        })
    
    # Rule 2: Segment-based adjustments
    segment_lower = segment_name.lower()
    
    if "female" in segment_lower:
        strategy["emphasis"] = "exclusive benefit highlight"
        strategy["personalization"] = "emphasize special treatment"
    
    if "senior" in segment_lower or "elderly" in segment_lower:
        strategy["emphasis"] = "stability and trust"
        strategy["language_modifier"] = "clear, reassuring, no jargon"
        strategy["tone_modifier"] = "respectful and professional"
    
    if "high-net-worth" in segment_lower or "premium" in segment_lower or "platinum" in segment_lower:
        strategy["emphasis"] = "premium positioning and exclusivity"
        strategy["tone_modifier"] = "sophisticated, elite"
    
    if "inactive" in segment_lower or "dormant" in segment_lower:
        strategy["urgency_level"] = "very high"
        strategy["language_modifier"] = "re-engagement focused"
    
    if "tier 2" in segment_lower or "tier 3" in segment_lower:
        strategy["emphasis"] = "accessibility and growth opportunity"
    
    logger.info(f"Strategy determined for '{segment_name}' + '{objective}': {strategy}")
    return strategy


def generate_subject_lines(
    product_name: str,
    segment: Dict,
    objective: str,
    base_bonus: float,
    special_bonus: float = None,
    strategy: Dict = None
) -> List[str]:
    """
    Generate 2 subject line variants per segment using deterministic strategy.
    """
    
    if not strategy:
        strategy = determine_content_strategy(objective, segment["name"])
    
    # Build strategic prompt
    prompt = f"""
Generate 2 email subject line variants for a banking campaign.

STRATEGIC CONSTRAINTS (MUST FOLLOW):
- Tone: {strategy['tone']}
- Style: {strategy['subject_style']}
- Max length: {strategy.get('subject_length', '70 characters')}
{'- Extra emphasis: ' + strategy.get('emphasis', '') if strategy.get('emphasis') != 'standard' else ''}
{'- Language modifier: ' + strategy.get('language_modifier', '') if 'language_modifier' in strategy else ''}

CAMPAIGN DETAILS:
- Product: {product_name}
- Target segment: {segment['name']}
- Base bonus: {base_bonus}%
{f"- Special bonus for this segment: {special_bonus}%" if special_bonus else ""}
- Objective: {objective}

ALLOWED:
- Text only
- Emojis (use sparingly, only if it fits tone)
- Numbers for bonuses

NOT ALLOWED:
- No HTML
- No links in subject

Generate exactly 2 variants labeled as:
VARIANT_A: [subject line]
VARIANT_B: [subject line]

Both should follow the strategic constraints but differ in approach.
"""

    try:
        response = call_llm(prompt)
        
        # Parse variants
        variants = []
        for line in response.split('\n'):
            if 'VARIANT_A:' in line:
                variants.append(line.split('VARIANT_A:')[1].strip())
            elif 'VARIANT_B:' in line:
                variants.append(line.split('VARIANT_B:')[1].strip())
        
        # Ensure we have exactly 2 variants
        if len(variants) < 2:
            # Fallback generation
            logger.warning("LLM didn't return 2 variants, using fallback")
            variants = [
                f"🎯 {product_name}: {base_bonus}% Returns - Limited Time!",
                f"Exclusive Offer: {product_name} with {base_bonus}% Bonus"
            ]
            if special_bonus:
                variants[0] = f"🎯 Special: {base_bonus + special_bonus}% Returns for {segment['name']}!"
        
        return variants[:2]  # Ensure exactly 2
        
    except Exception as e:
        logger.error(f"Subject generation failed: {str(e)}")
        # Fallback
        return [
            f"{product_name} - {base_bonus}% Bonus Inside",
            f"Your {product_name} Offer: {base_bonus}% Returns"
        ]


def generate_body_content(
    product_name: str,
    segment: Dict,
    objective: str,
    base_bonus: float,
    special_bonus: float = None,
    strategy: Dict = None,
    cta_url: str = "https://bank.example.com/offers"
) -> List[str]:
    """
    Generate 2 body variants per segment using deterministic strategy.
    """
    
    if not strategy:
        strategy = determine_content_strategy(objective, segment["name"])
    
    prompt = f"""
Generate 2 email body text variants for a banking campaign.

STRATEGIC CONSTRAINTS (MUST FOLLOW):
- Tone: {strategy['tone']}
- CTA placement: {strategy['cta_placement']}
- Urgency level: {strategy.get('urgency_level', 'medium')}
{'- Emphasis: ' + strategy.get('emphasis', '') if strategy.get('emphasis') != 'standard' else ''}
{'- Language modifier: ' + strategy.get('language_modifier', '') if 'language_modifier' in strategy else ''}
{'- Personalization: ' + strategy.get('personalization', '') if 'personalization' in strategy else ''}

CAMPAIGN DETAILS:
- Product: {product_name}
- Target segment: {segment['name']}
- Segment reasoning: {segment.get('reasoning', '')}
- Base bonus: {base_bonus}%
{f"- Special bonus for this segment: {special_bonus}%" if special_bonus else ""}
- Objective: {objective}

REQUIRED ELEMENTS:
- Greeting line
- Value proposition
- Bonus details
- Call to action with URL: {cta_url}
- Sign off

ALLOWED FORMATTING:
- Plain text
- Line breaks for readability
- Emojis (2-3 max, if appropriate)
- Bold concepts using **text** (will be rendered in email client)

NOT ALLOWED:
- No HTML tags
- No other URLs except {cta_url}

Generate exactly 2 variants labeled as:

VARIANT_A:
[body text]

VARIANT_B:
[body text]

Both should follow strategic constraints but differ in message structure.
Keep each variant 150-250 words.
"""

    try:
        response = call_llm(prompt)
        
        # Parse variants
        variants = []
        current_variant = None
        current_text = []
        
        for line in response.split('\n'):
            if 'VARIANT_A:' in line:
                if current_variant and current_text:
                    variants.append('\n'.join(current_text).strip())
                current_variant = 'A'
                current_text = []
            elif 'VARIANT_B:' in line:
                if current_variant and current_text:
                    variants.append('\n'.join(current_text).strip())
                current_variant = 'B'
                current_text = []
            elif current_variant:
                current_text.append(line)
        
        # Add last variant
        if current_text:
            variants.append('\n'.join(current_text).strip())
        
        # Ensure we have 2 variants
        if len(variants) < 2:
            logger.warning("LLM didn't return 2 body variants, using fallback")
            bonus_text = f"{base_bonus + special_bonus}%" if special_bonus else f"{base_bonus}%"
            variants = [
                f"Dear Valued Customer,\n\nWe're excited to introduce {product_name} with {bonus_text} returns!\n\nClick here to learn more: {cta_url}\n\nBest regards,\nYour Bank",
                f"Hello,\n\n{product_name} is now available with an exclusive {bonus_text} bonus.\n\nGet started: {cta_url}\n\nThank you!"
            ]
        
        return variants[:2]
        
    except Exception as e:
        logger.error(f"Body generation failed: {str(e)}")
        # Fallback
        bonus_text = f"{base_bonus + special_bonus}%" if special_bonus else f"{base_bonus}%"
        return [
            f"Dear Customer,\n\nIntroducing {product_name} with {bonus_text} returns.\n\nLearn more: {cta_url}\n\nRegards,\nYour Bank",
            f"Hello,\n\n{product_name} offers {bonus_text} bonus.\n\nDetails: {cta_url}\n\nThank you!"
        ]


def generate_content_for_campaign(
    parsed_brief: Dict,
    segments: List[Dict],
    objective: str,
    cta_url: str = "https://bank.example.com/offers"
) -> List[Dict]:
    """
    Main content generation function.
    
    Returns structured variants ready for DB storage.
    """
    logger.info(f"Generating content for {len(segments)} segments")
    
    all_variants = []
    
    for segment in segments:
        logger.info(f"Generating content for segment: {segment['name']}")
        
        # Determine strategy for this segment
        strategy = determine_content_strategy(objective, segment['name'])
        
        # Determine bonuses
        base_bonus = parsed_brief.get('base_bonus', 0)
        special_bonus = None
        
        # Check if this segment gets special bonus
        if segment['name'].lower() == parsed_brief.get('special_segment', '').lower():
            special_bonus = parsed_brief.get('special_bonus', 0)
        
        # Generate subject lines
        subjects = generate_subject_lines(
            product_name=parsed_brief['product_name'],
            segment=segment,
            objective=objective,
            base_bonus=base_bonus,
            special_bonus=special_bonus,
            strategy=strategy
        )
        
        # Generate body content
        bodies = generate_body_content(
            product_name=parsed_brief['product_name'],
            segment=segment,
            objective=objective,
            base_bonus=base_bonus,
            special_bonus=special_bonus,
            strategy=strategy,
            cta_url=cta_url
        )
        
        # Create variants (2 per segment)
        for i in range(2):
            variant = {
                "segment_name": segment['name'],
                "segment_id": segment.get('id'),
                "subject": subjects[i] if i < len(subjects) else subjects[0],
                "body": bodies[i] if i < len(bodies) else bodies[0],
                "version_number": 1,
                "strategy": strategy,
                "variant_label": f"{segment['name']}_v{i+1}"
            }
            all_variants.append(variant)
            logger.info(f"Created variant: {variant['variant_label']}")
    
    logger.info(f"Generated {len(all_variants)} total variants")
    return all_variants
