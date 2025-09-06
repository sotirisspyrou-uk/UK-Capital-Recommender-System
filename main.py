#!/usr/bin/env python3
# main.py
# [Version 06-09-2025 17:50:00]
# Capital Recommender System - Main Orchestrator
# Authored by: Sotiris Spyrou, CEO, VerityAI

"""
Main orchestrator for the UK Capital Recommender System.
Coordinates multi-agent workflow for intelligent funding recommendations.
"""

import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import local modules
from config import (
    CONFIG, SCORING_WEIGHTS, FUNDING_TYPES, UK_SECTORS, 
    UK_REGIONS, ERROR_CODES, ERROR_MESSAGES
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BusinessProfile:
    """Standardized business profile data structure"""
    def __init__(self, data: Dict):
        self.company_name = data['company_name']
        self.sector = data['sector']
        self.annual_revenue = float(data['annual_revenue'])
        self.employees = int(data['employees'])
        self.location = data['location']
        self.business_age = data.get('business_age', 1)
        self.funding_amount = float(data['funding_amount'])
        self.funding_purpose = data.get('funding_purpose', 'expansion')
        self.timeline = data.get('timeline', '3_months')
        self.financials = data.get('financials', {})

class CapitalRecommenderOrchestrator:
    """
    Main orchestrator class for the Capital Recommender System.
    Coordinates business analysis, funding research, and intelligent matching.
    """
    
    def __init__(self):
        self.session_id = self._generate_session_id()
        logger.info(f"Capital Recommender Orchestrator initialized - Session: {self.session_id}")
    
    def _generate_session_id(self) -> str:
        """Generate unique session identifier"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"CR_{timestamp}_{hash(time.time()) % 10000:04d}"
    
    def process_recommendation_request(self, business_data: Dict) -> Dict:
        """
        Main entry point for processing funding recommendations.
        """
        start_time = time.time()
        business_id = business_data.get('company_name', 'unknown').replace(' ', '_').lower()
        
        try:
            logger.info(f"Processing recommendation request for: {business_id}")
            
            # Step 1: Validate input data
            if not self._validate_input(business_data):
                return self._create_error_result(business_id, ERROR_CODES["INVALID_INPUT"])
            
            # Step 2: Parse business profile
            business_profile = BusinessProfile(business_data)
            
            # Step 3: Business Analysis (Simulated)
            logger.info("Executing business analysis...")
            business_intelligence = self._simulate_business_analysis(business_profile)
            
            # Step 4: Funding Source Research (Simulated)
            logger.info("Researching funding sources...")
            available_sources = self._simulate_funding_research(business_profile, business_intelligence)
            
            # Step 5: Intelligent Matching (Simulated)
            logger.info("Executing recommendation matching...")
            matches = self._simulate_recommendation_matching(business_intelligence, available_sources, business_profile)
            
            # Step 6: Format recommendations
            recommendations = self._format_recommendations(matches, business_profile)
            
            execution_time = time.time() - start_time
            
            result = {
                "business_id": business_id,
                "recommendations": recommendations,
                "total_processed": len(available_sources),
                "execution_time": round(execution_time, 2),
                "confidence_level": self._calculate_confidence_level(recommendations),
                "success": True
            }
            
            logger.info(f"Recommendation completed successfully in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error processing recommendation: {str(e)}")
            execution_time = time.time() - start_time
            return {
                "business_id": business_id,
                "recommendations": [],
                "total_processed": 0,
                "execution_time": round(execution_time, 2),
                "confidence_level": "low",
                "success": False,
                "errors": [str(e)]
            }
    
    def _validate_input(self, data: Dict) -> bool:
        """Validate input business data"""
        required_fields = ['company_name', 'sector', 'annual_revenue', 'employees', 'location', 'funding_amount']
        return all(field in data and data[field] is not None for field in required_fields)
    
    def _simulate_business_analysis(self, profile: BusinessProfile) -> Dict:
        """Simulate sophisticated business analysis"""
        # Determine business stage
        if profile.business_age <= 2:
            stage = "startup"
        elif profile.business_age <= 7:
            stage = "growth"
        else:
            stage = "mature"
        
        # Calculate risk level
        sector_risk = UK_SECTORS.get(profile.sector, {}).get("risk_level", "medium")
        region_risk = "low" if profile.location.lower() == "london" else "medium"
        
        # Calculate creditworthiness
        revenue_score = min(profile.annual_revenue / 1000000, 1.0)
        age_score = min(profile.business_age / 10, 1.0)
        creditworthiness = (revenue_score * 0.6 + age_score * 0.4)
        
        # Calculate funding readiness
        funding_ratio = profile.funding_amount / max(profile.annual_revenue, 1)
        readiness_base = 0.8 if funding_ratio <= 0.5 else 0.6 if funding_ratio <= 1.0 else 0.4
        
        return {
            "business_profile": {
                "risk_level": sector_risk,
                "stage": stage,
                "creditworthiness": creditworthiness,
                "growth_trajectory": "accelerating" if stage == "startup" else "stable",
                "funding_readiness": readiness_base,
                "sector_attractiveness": UK_SECTORS.get(profile.sector, {}).get("growth_potential", "medium")
            },
            "funding_indicators": {
                "amount_justification": "reasonable" if funding_ratio <= 1.0 else "optimistic",
                "repayment_capacity": creditworthiness,
                "asset_backing": 0.7 if profile.sector in ["manufacturing", "construction"] else 0.4,
                "management_strength": 0.75
            },
            "matching_tags": [profile.sector, stage, profile.location.lower()],
            "red_flags": ["high_funding_ratio"] if funding_ratio > 2.0 else [],
            "recommended_funding_types": ["bank_loan", "asset_finance"] if stage == "mature" else ["angel_investment", "vc"]
        }
    
    def _simulate_funding_research(self, profile: BusinessProfile, intelligence: Dict) -> List[Dict]:
        """Simulate funding source research"""
        sources = [
            {
                "source_id": "barclays_business_loan",
                "name": "Barclays Business Loan",
                "type": "bank_loan",
                "amount_range": {"min": 5000, "max": 250000},
                "broker_commission": {"min": 1.5, "max": 3.0},
                "timeline": "2-4 weeks",
                "current_appetite": "selective",
                "sectors": ["all"],
                "min_trading_years": 2
            },
            {
                "source_id": "uk_angel_network",
                "name": "UK Angel Investment Network",
                "type": "angel_investment",
                "amount_range": {"min": 25000, "max": 500000},
                "broker_commission": {"min": 3.0, "max": 7.0},
                "timeline": "4-12 weeks",
                "current_appetite": "aggressive",
                "sectors": ["technology", "healthcare"],
                "min_trading_years": 0
            },
            {
                "source_id": "lloyds_asset_finance",
                "name": "Lloyds Asset Finance",
                "type": "asset_finance",
                "amount_range": {"min": 10000, "max": 2000000},
                "broker_commission": {"min": 2.0, "max": 5.0},
                "timeline": "1-3 weeks",
                "current_appetite": "aggressive",
                "sectors": ["manufacturing", "construction", "transport"],
                "min_trading_years": 1
            },
            {
                "source_id": "crowdcube",
                "name": "Crowdcube Equity Crowdfunding",
                "type": "crowdfunding",
                "amount_range": {"min": 10000, "max": 1000000},
                "broker_commission": {"min": 3.0, "max": 8.0},
                "timeline": "2-8 weeks",
                "current_appetite": "neutral",
                "sectors": ["consumer_products", "technology"],
                "min_trading_years": 1
            }
        ]
        
        # Filter by basic eligibility
        eligible_sources = []
        for source in sources:
            # Check amount range
            if (source["amount_range"]["min"] <= profile.funding_amount <= source["amount_range"]["max"]):
                # Check trading years
                if profile.business_age >= source["min_trading_years"]:
                    # Check sector
                    if source["sectors"] == ["all"] or profile.sector in source["sectors"]:
                        eligible_sources.append(source)
        
        return eligible_sources
    
    def _simulate_recommendation_matching(self, intelligence: Dict, sources: List[Dict], profile: BusinessProfile) -> List[Dict]:
        """Simulate 4D recommendation matching"""
        matches = []
        
        for source in sources:
            # Calculate 4D scores
            compatibility = self._calculate_compatibility(source, profile, intelligence)
            probability = self._calculate_probability(source, intelligence)
            commercial = self._calculate_commercial_value(source, profile)
            strategic = self._calculate_strategic_fit(source, profile)
            
            # Overall score
            overall_score = (
                compatibility * SCORING_WEIGHTS["compatibility"] +
                probability * SCORING_WEIGHTS["approval_probability"] +
                commercial * SCORING_WEIGHTS["commercial_value"] +
                strategic * SCORING_WEIGHTS["strategic_fit"]
            )
            
            if overall_score >= CONFIG.MIN_MATCH_SCORE:
                matches.append({
                    "source": source,
                    "overall_score": overall_score,
                    "compatibility": compatibility,
                    "probability": probability,
                    "commercial": commercial,
                    "strategic": strategic,
                    "success_probability": (probability * 0.7 + compatibility * 0.3)
                })
        
        # Sort by score
        matches.sort(key=lambda x: x["overall_score"], reverse=True)
        return matches[:CONFIG.MAX_RECOMMENDATIONS]
    
    def _calculate_compatibility(self, source: Dict, profile: BusinessProfile, intelligence: Dict) -> float:
        """Calculate compatibility score"""
        score = 0.8  # Base score for eligible sources
        
        # Sector bonus
        if profile.sector in source.get("sectors", []):
            score += 0.1
        
        # Amount fit
        mid_point = (source["amount_range"]["min"] + source["amount_range"]["max"]) / 2
        if abs(profile.funding_amount - mid_point) < (mid_point * 0.5):
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_probability(self, source: Dict, intelligence: Dict) -> float:
        """Calculate approval probability"""
        base_rates = {
            "bank_loan": 0.65,
            "asset_finance": 0.75,
            "angel_investment": 0.25,
            "venture_capital": 0.15,
            "crowdfunding": 0.45
        }
        
        base_rate = base_rates.get(source["type"], 0.5)
        creditworthiness = intelligence["business_profile"]["creditworthiness"]
        
        # Adjust for current appetite
        appetite_multiplier = {
            "aggressive": 1.2,
            "neutral": 1.0,
            "selective": 0.8,
            "cautious": 0.6
        }
        
        multiplier = appetite_multiplier.get(source.get("current_appetite", "neutral"), 1.0)
        
        return min(base_rate * creditworthiness * multiplier, 1.0)
    
    def _calculate_commercial_value(self, source: Dict, profile: BusinessProfile) -> float:
        """Calculate commercial value for broker"""
        commission = source.get("broker_commission", {})
        if isinstance(commission, dict):
            avg_commission = (commission.get("min", 0) + commission.get("max", 0)) / 2
            potential_revenue = (avg_commission / 100) * profile.funding_amount
            return min(potential_revenue / 10000, 1.0)
        return 0.5
    
    def _calculate_strategic_fit(self, source: Dict, profile: BusinessProfile) -> float:
        """Calculate strategic fit"""
        if source["type"] in ["angel_investment", "venture_capital"]:
            return 0.8  # High strategic value
        elif source["type"] in ["bank_loan", "asset_finance"]:
            return 0.6  # Medium strategic value
        else:
            return 0.4  # Lower strategic value
    
    def _format_recommendations(self, matches: List[Dict], profile: BusinessProfile) -> List[Dict]:
        """Format recommendations for output"""
        recommendations = []
        
        for i, match in enumerate(matches):
            source = match["source"]
            
            # Format amount range
            amount_range = f"£{source['amount_range']['min']:,} - £{source['amount_range']['max']:,}"
            
            # Format commission
            commission = source.get("broker_commission", {})
            if isinstance(commission, dict):
                broker_commission = f"{commission.get('min', 0):.1f}%-{commission.get('max', 0):.1f}%"
            else:
                broker_commission = "Contact for details"
            
            recommendation = {
                "rank": i + 1,
                "funding_source": source["name"],
                "type": source["type"],
                "match_score": round(match["overall_score"], 2),
                "success_probability": round(match["success_probability"], 2),
                "amount_range": amount_range,
                "timeline": source["timeline"],
                "broker_commission": broker_commission,
                "requirements": [f"Minimum {source.get('min_trading_years', 0)} years trading"],
                "contact_info": {"type": "simulated"},
                "next_steps": ["Prepare business plan", "Gather financial documents"],
                "reasoning": f"Strong match based on {source['type'].replace('_', ' ')} criteria"
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def _calculate_confidence_level(self, recommendations: List[Dict]) -> str:
        """Calculate overall confidence"""
        if not recommendations:
            return "none"
        
        avg_score = sum(r['match_score'] for r in recommendations) / len(recommendations)
        
        if avg_score >= 0.85:
            return "very_high"
        elif avg_score >= 0.75:
            return "high"
        elif avg_score >= 0.65:
            return "medium"
        else:
            return "low"
    
    def _create_error_result(self, business_id: str, error_code: int) -> Dict:
        """Create standardized error result"""
        return {
            "business_id": business_id,
            "recommendations": [],
            "total_processed": 0,
            "execution_time": 0.0,
            "confidence_level": "none",
            "success": False,
            "errors": [ERROR_MESSAGES.get(error_code, "Unknown error")]
        }
    
    def get_system_status(self) -> Dict:
        """Get current system status"""
        return {
            "system": CONFIG.SYSTEM_NAME,
            "version": CONFIG.SYSTEM_VERSION,
            "status": "operational",
            "session_id": self.session_id,
            "max_recommendations": CONFIG.MAX_RECOMMENDATIONS,
            "last_updated": datetime.now().isoformat()
        }

def main():
    """Main execution function"""
    # Initialize orchestrator
    orchestrator = CapitalRecommenderOrchestrator()
    
    # Example business profile
    test_business = {
        "company_name": "TechStart Solutions Ltd",
        "sector": "technology",
        "annual_revenue": 450000,
        "employees": 12,
        "location": "london",
        "business_age": 3,
        "funding_amount": 250000,
        "funding_purpose": "expansion",
        "timeline": "3_months",
        "financials": {
            "profit_margin": 0.15,
            "cash_flow_months": 4,
            "debt_to_equity": 0.8
        }
    }
    
    print(f"\n{CONFIG.SYSTEM_NAME} v{CONFIG.SYSTEM_VERSION}")
    print("=" * 50)
    print("Sophisticated Multi-Agent Recommendation Engine")
    print("=" * 50)
    
    # Process recommendation
    result = orchestrator.process_recommendation_request(test_business)
    
    # Display results
    if result["success"]:
        print(f"✅ Success! Generated {len(result['recommendations'])} recommendations")
        print(f"⏱️  Processing time: {result['execution_time']}s")
        print(f"🎯 Confidence level: {result['confidence_level']}")
        print(f"📊 Sources evaluated: {result['total_processed']}")
        
        print("\n🏆 TOP RECOMMENDATIONS:")
        for rec in result["recommendations"]:
            print(f"\n{rec['rank']}. {rec['funding_source']}")
            print(f"   Type: {rec['type'].replace('_', ' ').title()}")
            print(f"   Match Score: {rec['match_score']}")
            print(f"   Success Probability: {rec['success_probability']}")
            print(f"   Broker Commission: {rec['broker_commission']}")
            print(f"   Timeline: {rec['timeline']}")
            print(f"   Reasoning: {rec['reasoning']}")
    else:
        print(f"❌ Error: {result.get('errors', ['Unknown error'])}")
    
    # Display system status
    status = orchestrator.get_system_status()
    print(f"\n📈 SYSTEM STATUS:")
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print(f"\n🚀 Ready for Claude Code handoff!")
    print("   See docs/Claude.md for technical details")

if __name__ == "__main__":
    main()
