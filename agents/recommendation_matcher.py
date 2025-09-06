# agents/recommendation_matcher.py
# [Version 06-09-2025 14:35:22]
# Recommendation Matcher Agent - Advanced scoring and matching algorithms
# Authored by: Sotiris Spyrou, CEO, VerityAI

"""
Recommendation Matcher Agent for the Capital Recommender System.
Executes sophisticated matching logic using multi-dimensional scoring algorithms.
"""

import math
import logging
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

from config import SCORING_WEIGHTS, FUNDING_TYPES, CONFIG

logger = logging.getLogger(__name__)

@dataclass
class MatchResult:
    """Individual funding source match result"""
    source_id: str
    source_name: str
    funding_type: str
    overall_score: float
    score_breakdown: Dict[str, float]
    success_probability: float
    amount_range: str
    timeline: str
    broker_commission: str
    requirements: List[str]
    contact: Dict[str, str]
    next_steps: List[str]
    reasoning: str

class RecommendationMatcher:
    """
    Advanced recommendation matching engine using multi-dimensional scoring.
    Combines business intelligence with funding source data for optimal matches.
    """
    
    def __init__(self):
        self.scoring_weights = SCORING_WEIGHTS
        self.funding_type_data = FUNDING_TYPES
        self.min_score_threshold = CONFIG.MIN_MATCH_SCORE
        self.max_recommendations = CONFIG.MAX_RECOMMENDATIONS
        
        logger.info("Recommendation Matcher initialized")
    
    def generate_matches(self, business_intelligence: Dict, funding_sources: List[Dict], 
                        business_profile) -> List[Dict]:
        """
        Generate ranked funding recommendations using advanced matching algorithms.
        
        Args:
            business_intelligence: Output from BusinessAnalyzer
            funding_sources: Available sources from FundingResearcher
            business_profile: Original business profile data
            
        Returns:
            List of ranked match results with detailed scoring
        """
        try:
            logger.info(f"Generating matches for {len(funding_sources)} funding sources")
            
            matches = []
            
            for source in funding_sources:
                # Calculate multi-dimensional match score
                match_score = self._calculate_match_score(
                    business_intelligence, source, business_profile
                )
                
                # Only include matches above threshold
                if match_score["overall_score"] >= self.min_score_threshold:
                    # Create detailed match result
                    match_result = self._create_match_result(
                        source, match_score, business_intelligence, business_profile
                    )
                    matches.append(match_result)
            
            # Sort by overall score and apply diversity rules
            ranked_matches = self._rank_and_diversify_matches(matches)
            
            # Limit to maximum recommendations
            final_matches = ranked_matches[:self.max_recommendations]
            
            logger.info(f"Generated {len(final_matches)} qualified recommendations")
            return [self._match_result_to_dict(match) for match in final_matches]
            
        except Exception as e:
            logger.error(f"Error generating matches: {str(e)}")
            return self._create_fallback_matches(business_profile)
    
    def _calculate_match_score(self, intelligence: Dict, source: Dict, profile) -> Dict[str, float]:
        """
        Calculate comprehensive match score using 4-dimensional framework:
        1. Compatibility (40%) - Sector, stage, geography, amount alignment
        2. Approval Probability (35%) - Historical success, appetite, financial health
        3. Commercial Value (15%) - Broker commission, processing efficiency
        4. Strategic Fit (10%) - Long-term potential, reputation, network effects
        """
        
        # Calculate individual dimension scores
        compatibility = self._calculate_compatibility_score(intelligence, source, profile)
        probability = self._calculate_approval_probability(intelligence, source, profile)
        commercial = self._calculate_commercial_value(source, profile)
        strategic = self._calculate_strategic_fit(intelligence, source, profile)
        
        # Apply weights and calculate overall score
        overall_score = (
            compatibility * self.scoring_weights["compatibility"] +
            probability * self.scoring_weights["approval_probability"] +
            commercial * self.scoring_weights["commercial_value"] +
            strategic * self.scoring_weights["strategic_fit"]
        )
        
        return {
            "overall_score": min(overall_score, 1.0),
            "compatibility": compatibility,
            "approval_probability": probability,
            "commercial_value": commercial,
            "strategic_fit": strategic
        }
    
    def _calculate_compatibility_score(self, intelligence: Dict, source: Dict, profile) -> float:
        """Calculate compatibility between business and funding source"""
        score = 0.0
        
        # Sector alignment (25% of compatibility)
        sector_score = self._assess_sector_compatibility(source, profile.sector)
        score += sector_score * 0.25
        
        # Business stage vs funding stage preference (25%)
        stage_score = self._assess_stage_compatibility(intelligence, source, profile)
        score += stage_score * 0.25
        
        # Geographic coverage and focus (20%)
        geo_score = self._assess_geographic_compatibility(source, profile.location)
        score += geo_score * 0.20
        
        # Amount range compatibility (20%)
        amount_score = self._assess_amount_compatibility(source, profile.funding_amount)
        score += amount_score * 0.20
        
        # Regulatory compliance matching (10%)
        compliance_score = self._assess_compliance_compatibility(source, profile)
        score += compliance_score * 0.10
        
        return min(score, 1.0)
    
    def _calculate_approval_probability(self, intelligence: Dict, source: Dict, profile) -> float:
        """Calculate likelihood of approval based on historical and current factors"""
        score = 0.0
        
        # Historical success rates for similar profiles (30%)
        historical_score = self._assess_historical_success_rate(intelligence, source)
        score += historical_score * 0.30
        
        # Current lending/investment appetite (25%)
        appetite_score = self._assess_current_appetite(source)
        score += appetite_score * 0.25
        
        # Credit and financial health alignment (25%)
        financial_score = self._assess_financial_alignment(intelligence, source)
        score += financial_score * 0.25
        
        # Management team strength match (10%)
        management_score = self._assess_management_fit(intelligence, source)
        score += management_score * 0.10
        
        # Market condition favorability (10%)
        market_score = self._assess_market_conditions(source)
        score += market_score * 0.10
        
        return min(score, 1.0)
    
    def _calculate_commercial_value(self, source: Dict, profile) -> float:
        """Calculate commercial value for broker"""
        score = 0.0
        
        # Broker commission potential (40%)
        commission_score = self._assess_commission_potential(source, profile)
        score += commission_score * 0.40
        
        # Processing speed and efficiency (30%)
        efficiency_score = self._assess_processing_efficiency(source)
        score += efficiency_score * 0.30
        
        # Relationship manager quality (20%)
        relationship_score = self._assess_relationship_quality(source)
        score += relationship_score * 0.20
        
        # Application complexity level (10%)
        complexity_score = self._assess_application_complexity(source)
        score += complexity_score * 0.10
        
        return min(score, 1.0)
    
    def _calculate_strategic_fit(self, intelligence: Dict, source: Dict, profile) -> float:
        """Calculate strategic fit and long-term value"""
        score = 0.0
        
        # Long-term relationship potential (40%)
        relationship_score = self._assess_longterm_potential(intelligence, source)
        score += relationship_score * 0.40
        
        # Portfolio diversification value (20%)
        diversification_score = self._assess_portfolio_fit(source, profile)
        score += diversification_score * 0.20
        
        # Market reputation and credibility (20%)
        reputation_score = self._assess_reputation_value(source)
        score += reputation_score * 0.20
        
        # Follow-on funding opportunities (10%)
        followon_score = self._assess_followon_potential(source, profile)
        score += followon_score * 0.10
        
        # Network effect benefits (10%)
        network_score = self._assess_network_benefits(source, profile)
        score += network_score * 0.10
        
        return min(score, 1.0)
    
    # Individual assessment methods
    def _assess_sector_compatibility(self, source: Dict, sector: str) -> float:
        """Assess sector compatibility"""
        source_sectors = source.get("sectors", [])
        excluded_sectors = source.get("excluded_sectors", [])
        
        if sector in excluded_sectors:
            return 0.0
        elif source_sectors == ["all"] or sector in source_sectors:
            return 1.0
        else:
            return 0.3  # Some flexibility for related sectors
    
    def _assess_stage_compatibility(self, intelligence: Dict, source: Dict, profile) -> float:
        """Assess business stage compatibility"""
        business_stage = intelligence["business_profile"]["stage"]
        source_type = source["type"]
        
        # Stage preference mapping
        stage_preferences = {
            "bank_loan": {"mature": 1.0, "growth": 0.8, "startup": 0.4},
            "asset_finance": {"mature": 1.0, "growth": 0.9, "startup": 0.6},
            "angel_investment": {"startup": 1.0, "growth": 0.7, "mature": 0.3},
            "venture_capital": {"startup": 0.9, "growth": 1.0, "mature": 0.2},
            "crowdfunding": {"startup": 0.8, "growth": 0.9, "mature": 0.5},
            "government_grant": {"startup": 0.9, "growth": 0.8, "mature": 0.6},
            "family_office": {"growth": 1.0, "mature": 0.8, "startup": 0.6}
        }
        
        preferences = stage_preferences.get(source_type, {})
        return preferences.get(business_stage, 0.5)
    
    def _assess_geographic_compatibility(self, source: Dict, location: str) -> float:
        """Assess geographic compatibility"""
        geo_requirements = source.get("geographic_requirement", [])
        
        if not geo_requirements:  # UK-wide
            return 1.0
        elif location.lower() in geo_requirements:
            return 1.0
        else:
            return 0.0
    
    def _assess_amount_compatibility(self, source: Dict, amount: float) -> float:
        """Assess funding amount compatibility"""
        min_amount = source["amount_range"]["min"]
        max_amount = source["amount_range"]["max"]
        
        if min_amount <= amount <= max_amount:
            # Perfect fit in middle 50% of range
            mid_point = (min_amount + max_amount) / 2
            range_size = max_amount - min_amount
            
            if abs(amount - mid_point) <= (range_size * 0.25):
                return 1.0
            else:
                return 0.8
        else:
            return 0.0
    
    def _assess_compliance_compatibility(self, source: Dict, profile) -> float:
        """Assess regulatory compliance alignment"""
        # Simple assessment - in real system would check detailed compliance
        return 0.9  # Assume generally compliant
    
    def _assess_historical_success_rate(self, intelligence: Dict, source: Dict) -> float:
        """Assess historical success rate for similar profiles"""
        # Simulate historical success based on source type and business profile
        base_rates = {
            "bank_loan": 0.65,
            "asset_finance": 0.75,
            "angel_investment": 0.25,
            "venture_capital": 0.15,
            "crowdfunding": 0.45,
            "government_grant": 0.35,
            "family_office": 0.40
        }
        
        base_rate = base_rates.get(source["type"], 0.5)
        
        # Adjust based on business intelligence
        readiness = intelligence["business_profile"]["funding_readiness"]
        creditworthiness = intelligence["business_profile"]["creditworthiness"]
        
        adjusted_rate = base_rate * (0.5 + 0.5 * readiness) * (0.5 + 0.5 * creditworthiness)
        
        return min(adjusted_rate, 1.0)
    
    def _assess_current_appetite(self, source: Dict) -> float:
        """Assess current lending/investment appetite"""
        appetite_scores = {
            "aggressive": 1.0,
            "neutral": 0.7,
            "selective": 0.5,
            "cautious": 0.3,
            "limited": 0.1
        }
        
        appetite = source.get("current_appetite", "neutral")
        return appetite_scores.get(appetite, 0.5)
    
    def _assess_financial_alignment(self, intelligence: Dict, source: Dict) -> float:
        """Assess financial health alignment"""
        creditworthiness = intelligence["business_profile"]["creditworthiness"]
        repayment_capacity = intelligence["funding_indicators"]["repayment_capacity"]
        
        # Weight creditworthiness and repayment capacity
        return (creditworthiness * 0.6 + repayment_capacity * 0.4)
    
    def _assess_management_fit(self, intelligence: Dict, source: Dict) -> float:
        """Assess management team alignment"""
        management_strength = intelligence["funding_indicators"]["management_strength"]
        
        # Different funding types have different management requirements
        if source["type"] in ["venture_capital", "angel_investment"]:
            return management_strength
        else:
            return 0.7 + (management_strength * 0.3)  # Less critical for traditional funding
    
    def _assess_market_conditions(self, source: Dict) -> float:
        """Assess market condition favorability"""
        sector_status = source.get("sector_market_status", "neutral")
        
        status_scores = {
            "hot": 1.0,
            "neutral": 0.7,
            "cold": 0.4
        }
        
        return status_scores.get(sector_status, 0.7)
    
    def _assess_commission_potential(self, source: Dict, profile) -> float:
        """Assess broker commission potential"""
        commission = source.get("broker_commission", {})
        
        if isinstance(commission, dict):
            avg_commission = (commission.get("min", 0) + commission.get("max", 0)) / 2
            potential_revenue = (avg_commission / 100) * profile.funding_amount
            
            # Normalize to 0-1 scale (£10k commission = 1.0)
            return min(potential_revenue / 10000, 1.0)
        
        return 0.5
    
    def _assess_processing_efficiency(self, source: Dict) -> float:
        """Assess processing speed and efficiency"""
        timeline = source.get("approval_timeline", "4-8 weeks")
        
        # Extract weeks from timeline string
        if "week" in timeline:
            weeks_parts = timeline.split("-")
            try:
                max_weeks = int(weeks_parts[1].split()[0])
                # Faster = better (inverse relationship)
                return max(0.1, 1.0 - (max_weeks - 1) / 20)
            except (ValueError, IndexError):
                return 0.5
        
        return 0.5
    
    def _assess_relationship_quality(self, source: Dict) -> float:
        """Assess relationship manager quality"""
        # Simulate based on source type and status
        if source.get("availability_status") == "relationship_based":
            return 0.9  # High touch relationship
        elif source["type"] in ["family_office", "venture_capital"]:
            return 0.8  # Generally good relationships
        else:
            return 0.6  # Standard relationship quality
    
    def _assess_application_complexity(self, source: Dict) -> float:
        """Assess application complexity (lower complexity = higher score)"""
        complexity_by_type = {
            "asset_finance": 0.9,  # Simple, asset-backed
            "bank_loan": 0.7,     # Standard process
            "crowdfunding": 0.6,   # Marketing intensive
            "government_grant": 0.4,  # Complex application
            "venture_capital": 0.3,   # Very complex
            "angel_investment": 0.5,  # Moderate complexity
            "family_office": 0.4     # Relationship dependent
        }
        
        return complexity_by_type.get(source["type"], 0.5)
    
    def _assess_longterm_potential(self, intelligence: Dict, source: Dict) -> float:
        """Assess long-term relationship potential"""
        if source["type"] in ["venture_capital", "family_office", "angel_investment"]:
            # Equity partners - high long-term potential
            return 0.9
        elif source["type"] in ["bank_loan", "asset_finance"]:
            # Lending relationships can develop over time
            return 0.6
        else:
            return 0.4
    
    def _assess_portfolio_fit(self, source: Dict, profile) -> float:
        """Assess portfolio diversification value"""
        # Simulate based on broker's portfolio needs
        return 0.7  # Assume most deals add portfolio value
    
    def _assess_reputation_value(self, source: Dict) -> float:
        """Assess market reputation and credibility"""
        reputation_by_name = {
            "Barclays": 0.9,
            "Lloyds": 0.9,
            "Seedcamp": 0.8,
            "Crowdcube": 0.7
        }
        
        source_name = source.get("name", "")
        for name, score in reputation_by_name.items():
            if name in source_name:
                return score
        
        return 0.6  # Default reputation score
    
    def _assess_followon_potential(self, source: Dict, profile) -> float:
        """Assess follow-on funding opportunities"""
        if source["type"] in ["venture_capital", "angel_investment"]:
            return 0.8  # High follow-on potential
        elif source["type"] == "family_office":
            return 0.7
        else:
            return 0.3  # Limited follow-on for debt
    
    def _assess_network_benefits(self, source: Dict, profile) -> float:
        """Assess network effect benefits"""
        if source["type"] in ["venture_capital", "angel_investment", "family_office"]:
            return 0.8  # Strong networks
        elif profile.sector == "technology":
            return 0.6  # Tech sector has good networks
        else:
            return 0.4
    
    def _create_match_result(self, source: Dict, match_score: Dict, 
                           intelligence: Dict, profile) -> MatchResult:
        """Create detailed match result object"""
        
        # Calculate success probability (combination of approval probability and compatibility)
        success_probability = (
            match_score["approval_probability"] * 0.7 +
            match_score["compatibility"] * 0.3
        )
        
        # Format amount range
        amount_range = f"£{source['amount_range']['min']:,} - £{source['amount_range']['max']:,}"
        
        # Format broker commission
        commission = source.get("broker_commission", {})
        if isinstance(commission, dict):
            broker_commission = f"{commission.get('min', 0):.1f}%-{commission.get('max', 0):.1f}%"
        else:
            broker_commission = "Contact for details"
        
        # Generate requirements and next steps
        requirements = self._generate_requirements(source, intelligence)
        next_steps = self._generate_next_steps(source, profile)
        reasoning = self._generate_reasoning(match_score, source, intelligence)
        
        return MatchResult(
            source_id=source["source_id"],
            source_name=source["name"],
            funding_type=source["type"],
            overall_score=match_score["overall_score"],
            score_breakdown=match_score,
            success_probability=success_probability,
            amount_range=amount_range,
            timeline=source.get("market_adjusted_timeline", source["approval_timeline"]),
            broker_commission=broker_commission,
            requirements=requirements,
            contact=source.get("contact", {}),
            next_steps=next_steps,
            reasoning=reasoning
        )
    
    def _generate_requirements(self, source: Dict, intelligence: Dict) -> List[str]:
        """Generate key requirements for funding application"""
        requirements = []
        
        # Trading years requirement
        min_years = source.get("min_trading_years", 0)
        if min_years > 0:
            requirements.append(f"Minimum {min_years} years trading history")
        
        # Revenue requirement
        min_revenue = source.get("min_annual_revenue", 0)
        if min_revenue > 0:
            requirements.append(f"Minimum £{min_revenue:,} annual revenue")
        
        # Sector-specific requirements
        if source.get("innovation_requirement"):
            requirements.append("Innovation/R&D focus required")
        
        if source.get("asset_requirement"):
            requirements.append("Asset backing required")
        
        # Financial health requirements
        if intelligence["business_profile"]["creditworthiness"] < 0.7:
            requirements.append("Strong credit history essential")
        
        return requirements[:5]  # Limit to top 5
    
    def _generate_next_steps(self, source: Dict, profile) -> List[str]:
        """Generate actionable next steps"""
        steps = []
        
        # Document preparation
        if source["type"] in ["bank_loan", "asset_finance"]:
            steps.extend([
                "Prepare 3 years of audited accounts",
                "Gather recent bank statements",
                "Complete business plan summary"
            ])
        elif source["type"] in ["venture_capital", "angel_investment"]:
            steps.extend([
                "Prepare investor pitch deck",
                "Document growth strategy",
                "Prepare financial projections"
            ])
        elif source["type"] == "government_grant":
            steps.extend([
                "Review eligibility criteria in detail",
                "Prepare innovation/project plan",
                "Complete online application"
            ])
        
        # Contact step
        contact_info = source.get("contact", {})
        if contact_info.get("email"):
            steps.append(f"Contact via {contact_info['email']}")
        
        return steps[:4]  # Limit to top 4
    
    def _generate_reasoning(self, match_score: Dict, source: Dict, intelligence: Dict) -> str:
        """Generate human-readable reasoning for the recommendation"""
        reasons = []
        
        # Highlight strongest aspects
        if match_score["compatibility"] >= 0.8:
            reasons.append("excellent sector and stage alignment")
        
        if match_score["approval_probability"] >= 0.7:
            reasons.append("high approval probability based on financial profile")
        
        if match_score["commercial_value"] >= 0.7:
            reasons.append("attractive commission structure")
        
        # Source-specific strengths
        if source.get("current_appetite") == "aggressive":
            reasons.append("actively seeking new deals")
        
        if source.get("availability_status") == "accepting_applications":
            reasons.append("currently accepting applications")
        
        # Combine reasons
        if reasons:
            return f"Recommended due to {', '.join(reasons)}."
        else:
            return "Solid match across multiple criteria."
    
    def _rank_and_diversify_matches(self, matches: List[MatchResult]) -> List[MatchResult]:
        """Sort matches by score and apply diversity rules"""
        # Sort by overall score
        sorted_matches = sorted(matches, key=lambda x: x.overall_score, reverse=True)
        
        # Apply diversity rules (max 2 per funding type)
        diversified_matches = []
        type_counts = {}
        
        for match in sorted_matches:
            funding_type = match.funding_type
            current_count = type_counts.get(funding_type, 0)
            
            if current_count < CONFIG.DIVERSITY_REQUIREMENT:
                diversified_matches.append(match)
                type_counts[funding_type] = current_count + 1
        
        return diversified_matches
    
    def _match_result_to_dict(self, match: MatchResult) -> Dict[str, Any]:
        """Convert MatchResult to dictionary"""
        return {
            "source_id": match.source_id,
            "source_name": match.source_name,
            "funding_type": match.funding_type,
            "overall_score": round(match.overall_score, 3),
            "score_breakdown": {
                k: round(v, 3) for k, v in match.score_breakdown.items()
            },
            "success_probability": round(match.success_probability, 3),
            "amount_range": match.amount_range,
            "timeline": match.timeline,
            "broker_commission": match.broker_commission,
            "requirements": match.requirements,
            "contact": match.contact,
            "next_steps": match.next_steps,
            "reasoning": match.reasoning
        }
    
    def _create_fallback_matches(self, profile) -> List[Dict]:
        """Create basic fallback matches if main matching fails"""
        fallback = [{
            "source_id": "fallback_generic",
            "source_name": "UK Business Finance",
            "funding_type": "bank_loan",
            "overall_score": 0.6,
            "score_breakdown": {
                "compatibility": 0.6,
                "approval_probability": 0.6,
                "commercial_value": 0.6,
                "strategic_fit": 0.6
            },
            "success_probability": 0.6,
            "amount_range": "Contact for details",
            "timeline": "4-8 weeks",
            "broker_commission": "2-4%",
            "requirements": ["Business plan", "Financial statements"],
            "contact": {"email": "info@ukbusinessfinance.co.uk"},
            "next_steps": ["Contact for initial assessment"],
            "reasoning": "Generic business lending option."
        }]
        
        return fallback
    
    def get_matching_statistics(self) -> Dict[str, Any]:
        """Get statistics about matching performance"""
        return {
            "scoring_framework": {
                "dimensions": 4,
                "weights": self.scoring_weights,
                "min_threshold": self.min_score_threshold
            },
            "quality_controls": {
                "max_recommendations": self.max_recommendations,
                "diversity_requirement": CONFIG.DIVERSITY_REQUIREMENT,
                "confidence_threshold": CONFIG.CONFIDENCE_THRESHOLD
            },
            "algorithm_version": "1.0.0",
            "last_updated": "2025-09-06"
        }
