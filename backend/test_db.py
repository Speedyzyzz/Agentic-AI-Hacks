#!/usr/bin/env python
"""
Database Test Script
Tests insert and retrieve operations for all tables
"""

from db import init_db, get_db_session
from models import Campaign, Segment, Variant, PerformanceMetric
from datetime import datetime


def test_database():
    """Test database operations"""
    print("=" * 60)
    print("DATABASE TEST SUITE")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing database...")
    init_db()
    print("   ✓ Database initialized")
    
    # Create session
    db = get_db_session()
    
    try:
        # Test 1: Create Campaign
        print("\n2. Creating campaign...")
        campaign = Campaign(
            product_name="XDeposit",
            objective="optimize for click rate",
            status="draft"
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        print(f"   ✓ Campaign created: {campaign}")
        
        # Test 2: Create Segments
        print("\n3. Creating segments...")
        segments_data = [
            {
                "campaign_id": campaign.id,
                "segment_name": "female senior citizens",
                "reasoning": "Special bonus targets this demographic"
            },
            {
                "campaign_id": campaign.id,
                "segment_name": "general customers",
                "reasoning": "Base bonus for all other customers"
            }
        ]
        
        segments = []
        for seg_data in segments_data:
            segment = Segment(**seg_data)
            db.add(segment)
            segments.append(segment)
        
        db.commit()
        for segment in segments:
            db.refresh(segment)
            print(f"   ✓ Segment created: {segment}")
        
        # Test 3: Create Variants
        print("\n4. Creating variants...")
        variants_data = [
            {
                "campaign_id": campaign.id,
                "segment_id": segments[0].id,
                "subject": "🎉 Special Rate Just for You - 1.25% Extra Returns!",
                "body": "Dear Valued Customer,\n\nWe're excited to offer you an exclusive bonus on XDeposit...",
                "send_time": "2026-03-01 10:00:00",
                "version_number": 1
            },
            {
                "campaign_id": campaign.id,
                "segment_id": segments[1].id,
                "subject": "Introducing XDeposit - 1% Higher Returns",
                "body": "Dear Customer,\n\nDiscover XDeposit with attractive returns...",
                "send_time": "2026-03-01 10:00:00",
                "version_number": 1
            }
        ]
        
        variants = []
        for var_data in variants_data:
            variant = Variant(**var_data)
            db.add(variant)
            variants.append(variant)
        
        db.commit()
        for variant in variants:
            db.refresh(variant)
            print(f"   ✓ Variant created: {variant}")
        
        # Test 4: Create Performance Metrics
        print("\n5. Creating performance metrics...")
        metrics_data = [
            {
                "variant_id": variants[0].id,
                "open_rate": 0.35,
                "click_rate": 0.12
            },
            {
                "variant_id": variants[1].id,
                "open_rate": 0.28,
                "click_rate": 0.08
            }
        ]
        
        metrics = []
        for metric_data in metrics_data:
            metric = PerformanceMetric(**metric_data)
            db.add(metric)
            metrics.append(metric)
        
        db.commit()
        for metric in metrics:
            db.refresh(metric)
            print(f"   ✓ Metric created: {metric}")
        
        # Test 5: Retrieve and Display Full Campaign
        print("\n6. Retrieving full campaign data...")
        retrieved_campaign = db.query(Campaign).filter_by(id=campaign.id).first()
        
        print(f"\n   Campaign: {retrieved_campaign.product_name}")
        print(f"   Objective: {retrieved_campaign.objective}")
        print(f"   Status: {retrieved_campaign.status}")
        print(f"   Created: {retrieved_campaign.created_at}")
        
        print(f"\n   Segments ({len(retrieved_campaign.segments)}):")
        for seg in retrieved_campaign.segments:
            print(f"     - {seg.segment_name}: {seg.reasoning}")
        
        print(f"\n   Variants ({len(retrieved_campaign.variants)}):")
        for var in retrieved_campaign.variants:
            print(f"     - Subject: {var.subject}")
            print(f"       Send Time: {var.send_time}")
            if var.metrics:
                for m in var.metrics:
                    print(f"       Performance: Open={m.open_rate:.2%}, Click={m.click_rate:.2%}")
        
        # Test 6: Query Performance Comparison
        print("\n7. Performance comparison...")
        all_variants = db.query(Variant).filter_by(campaign_id=campaign.id).all()
        for var in all_variants:
            if var.metrics:
                latest_metric = var.metrics[0]
                print(f"   {var.segment.segment_name}:")
                print(f"     Open: {latest_metric.open_rate:.2%} | Click: {latest_metric.click_rate:.2%}")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()


if __name__ == "__main__":
    success = test_database()
    exit(0 if success else 1)
