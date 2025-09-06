#!/usr/bin/env python3
# examples/basic_usage.py
# Basic usage example for UK Capital Recommender System

"""
Basic usage example demonstrating the complete recommendation system.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import CapitalRecommenderOrchestrator

def main():
    print("UK Capital Recommender - Advanced Usage Example")
    print("=" * 60)
    
    # Initialize the system
    orchestrator = CapitalRecommenderOrchestrator()
    
    # Example business profiles
    businesses = [
        {
            "company_name": "TechStart Solutions Ltd",
            "sector": "technology", 
            "annual_revenue": 450000,
            "employees": 12,
            "location": "london",
            "business_age": 3,
            "funding_amount": 250000,
            "funding_purpose": "expansion",
            "timeline": "3_months"
        },
        {
            "company_name": "Manchester Manufacturing Co",
            "sector": "manufacturing",
            "annual_revenue": 1200000,
            "employees": 35,
            "location": "north_west", 
            "business_age": 8,
            "funding_amount": 500000,
            "funding_purpose": "equipment",
            "timeline": "1_month"
        }
    ]
    
    for i, business in enumerate(businesses):
        print(f"\n--- EXAMPLE {i+1}: {business['company_name']} ---")
        
        # Process recommendation
        result = orchestrator.process_recommendation_request(business)
        
        if result["success"]:
            print(f"✅ Generated {len(result['recommendations'])} recommendations")
            print(f"⏱️  Processing time: {result['execution_time']}s")
            print(f"🎯 Confidence: {result['confidence_level']}")
            
            # Show top recommendation
            if result["recommendations"]:
                top_rec = result["recommendations"][0]
                print(f"\n🏆 TOP RECOMMENDATION:")
                print(f"   Source: {top_rec['funding_source']}")
                print(f"   Type: {top_rec['type'].replace('_', ' ').title()}")
                print(f"   Match Score: {top_rec['match_score']}")
                print(f"   Success Probability: {top_rec['success_probability']}")
                print(f"   Commission: {top_rec['broker_commission']}")
        else:
            print(f"❌ Error: {result.get('errors', ['Unknown error'])}")
    
    print(f"\n{'='*60}")
    print("🚀 System ready for production deployment!")
    print("📚 See docs/README.md for complete documentation")

if __name__ == "__main__":
    main()
