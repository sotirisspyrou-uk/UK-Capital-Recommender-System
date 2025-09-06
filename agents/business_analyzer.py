# agents/business_analyzer.py
# [Version 06-09-2025 17:50:00]
# Business Analyzer Agent - Comprehensive UK business profiling
# Authored by: Sotiris Spyrou, CEO, VerityAI

"""
Business Analyzer Agent for the Capital Recommender System.
Analyzes business profiles to extract funding-relevant characteristics.
"""

import logging
from typing import Dict, List, Any
from config import UK_SECTORS, COMPANY_SIZES, UK_REGIONS

logger = logging.getLogger(__name__)

class BusinessAnalyzer:
    """
    Comprehensive business analysis agent for funding optimization.
    """
    
    def __init__(self):
        self.sector_data = UK_SECTORS
        self.regional_data = UK_REGIONS
        logger.info("Business Analyzer initialized")
    
    def analyze_business(self, business_profile) -> Dict[str, Any]:
        """
        Main analysis function that processes business profile.
        """
        try:
            logger.info(f"Analyzing business: {business_profile.company_name}")
            
            # Core analysis components
            demographic_analysis = self._analyze_demographics(business_profile)
            financial_analysis = self._analyze_financials(business_profile)
            risk_analysis = self._analyze_risk_profile(business_profile)
            
            # Calculate funding readiness
            funding_readiness = self._calculate_funding_readiness(
                demographic_analysis, financial_analysis, risk_analysis
            )
            
            # Generate matching tags
            matching_tags = self._generate_matching_tags(business_profile, demographic_analysis)
            
            # Compile business intelligence
            intelligence = {
                "business_profile": {
                    "risk_level": risk_analysis["overall_risk"],
                    "stage": self._determine_business_stage(business_profile),
                    "creditworthiness": financial_analysis["creditworthiness"],
                    "growth_trajectory": "accelerating" if business_profile.business_age <= 3 else "stable",
                    "funding_readiness": funding_readiness,
                    "sector_attractiveness": demographic_analysis["sector_attractiveness"]
                },
                "funding_indicators": {
                    "amount_justification": self._assess_amount_justification(business_profile),
                    "repayment_capacity": financial_analysis["repayment_capacity"],
                    "asset_backing": financial_analysis["asset_backing"],
                    "management_strength": 0.75  # Simplified
                },
                "matching_tags": matching_tags,
                "red_flags": self._identify_red_flags(business_profile),
                "recommended_funding_types": self._recommend_funding_types(business_profile, funding_readiness)
            }
            
            logger.info(f"Business analysis completed - Readiness: {funding_readiness:.2f}")
            return intelligence
            
        except Exception as e:
            logger.error(f"Error in business analysis: {str(e)}")
            return self._create_fallback_analysis(business_profile)
    
    def _analyze_demographics(self, profile) -> Dict[str, Any]:
        """Analyze business demographic characteristics"""
        sector_info = self.sector_data.get(profile.sector, {})
        region_info = self.regional_data.get(profile.location.lower(), {})
        
        return {
            "sector": profile.sector,
            "sector_risk": sector_info.get("risk_level", "medium"),
            "sector_attractiveness": self._calculate_sector_attractiveness(sector_info),
            "location": profile.location,
            "regional_advantage": region_info.get("funding_availability", "fair"),
            "business_age": profile.business_age,
            "company_size": self._determine_company_size(profile.employees, profile.annual_revenue)
        }
    
    def _analyze_financials(self, profile) -> Dict[str, Any]:
        """Analyze financial health"""
        financials = profile.financials or {}
        
        profit_margin = financials.get("profit_margin", 0.1)
        cash_flow_months = financials.get("cash_flow_months", 2)
        
        creditworthiness = self._calculate_creditworthiness(
            profit_margin, cash_flow_months, profile.annual_revenue
        )
        
        repayment_capacity = self._calculate_repayment_capacity(
            profile.annual_revenue, profit_margin
        )
        
        asset_backing = self._estimate_asset_backing(
            profile.annual_revenue, profile.sector
        )
        
        return {
            "creditworthiness": creditworthiness,
            "repayment_capacity": repayment_capacity,
            "asset_backing": asset_backing,
            "profit_margin": profit_margin,
            "cash_flow_months": cash_flow_months
        }
    
    def _analyze_risk_profile(self, profile) -> Dict[str, Any]:
        """Comprehensive risk assessment"""
        sector_risk = self._assess_sector_risk(profile.sector)
        geographic_risk = self._assess_geographic_risk(profile.location)
        financial_risk = self._assess_financial_risk(profile)
        
        overall_risk = self._calculate_overall_risk(sector_risk, geographic_risk, financial_risk)
        
        return {
            "sector_risk": sector_risk,
            "geographic_risk": geographic_risk,
            "financial_risk": financial_risk,
            "overall_risk": overall_risk
        }
    
    def _calculate_funding_readiness(self, demographic, financial, risk) -> float:
        """Calculate overall funding readiness score (0-1)"""
        weights = {
            "financial_health": 0.4,
            "business_maturity": 0.25,
            "sector_attractiveness": 0.2,
            "risk_level": 0.15
        }
        
        financial_score = financial["creditworthiness"]
        maturity_score = min(demographic["business_age"] / 10, 1.0)
        sector_score = demographic["sector_attractiveness"]
        risk_score = 1.0 if risk["overall_risk"] == "low" else 0.7 if risk["overall_risk"] == "medium" else 0.4
        
        readiness = (
            financial_score * weights["financial_health"] +
            maturity_score * weights["business_maturity"] +
            sector_score * weights["sector_attractiveness"] +
            risk_score * weights["risk_level"]
        )
        
        return min(max(readiness, 0.0), 1.0)
    
    def _generate_matching_tags(self, profile, demographic) -> List[str]:
        """Generate tags for funding source matching"""
        tags = [
            f"{profile.sector}_business",
            f"{demographic['company_size']}_enterprise",
            f"{profile.location.lower()}_location"
        ]
        
        if profile.business_age <= 2:
            tags.append("startup")
        elif profile.business_age <= 7:
            tags.append("growth_stage")
        else:
            tags.append("established")
        
        if profile.annual_revenue > 1000000:
            tags.append("high_revenue")
        
        return tags
    
    def _identify_red_flags(self, profile) -> List[str]:
        """Identify potential deal-breaker issues"""
        red_flags = []
        
        funding_ratio = profile.funding_amount / max(profile.annual_revenue, 1)
        if funding_ratio > 2.0:
            red_flags.append("excessive_funding_request")
        
        if profile.business_age < 1:
            red_flags.append("very_new_business")
        
        return red_flags
    
    def _recommend_funding_types(self, profile, readiness) -> List[str]:
        """Recommend optimal funding types"""
        recommendations = []
        
        if readiness >= 0.8:
            if profile.funding_amount >= 250000:
                recommendations.extend(["venture_capital", "angel_investment"])
            recommendations.extend(["bank_loan", "asset_finance"])
        elif readiness >= 0.6:
            recommendations.extend(["bank_loan", "asset_finance", "crowdfunding"])
            if profile.sector == "technology":
                recommendations.append("angel_investment")
        else:
            recommendations.extend(["asset_finance", "crowdfunding", "government_grant"])
        
        return list(set(recommendations))
    
    # Helper methods
    def _determine_company_size(self, employees: int, revenue: float) -> str:
        """Determine company size category"""
        if employees <= 9 and revenue <= 632000:
            return "micro"
        elif employees <= 49 and revenue <= 10200000:
            return "small"
        elif employees <= 249 and revenue <= 50000000:
            return "medium"
        else:
            return "large"
    
    def _calculate_creditworthiness(self, profit_margin: float, cash_flow: int, revenue: float) -> float:
        """Calculate creditworthiness score"""
        profit_score = min(profit_margin * 10, 1.0)
        cash_score = min(cash_flow / 6, 1.0)
        revenue_score = min(revenue / 1000000, 1.0)
        
        return (profit_score * 0.4 + cash_score * 0.3 + revenue_score * 0.3)
    
    def _calculate_repayment_capacity(self, revenue: float, margin: float) -> float:
        """Calculate loan repayment capacity"""
        annual_profit = revenue * margin
        monthly_capacity = annual_profit / 12
        return min(monthly_capacity / 10000, 1.0)
    
    def _estimate_asset_backing(self, revenue: float, sector: str) -> float:
        """Estimate asset backing strength"""
        base_ratio = 0.3
        
        if sector in ["manufacturing", "construction"]:
            base_ratio += 0.2
        elif sector in ["technology", "professional_services"]:
            base_ratio -= 0.1
        
        return min(base_ratio, 1.0)
    
    def _calculate_sector_attractiveness(self, sector_info: Dict) -> float:
        """Calculate sector attractiveness for funding"""
        growth_potential = sector_info.get("growth_potential", "medium")
        risk_level = sector_info.get("risk_level", "medium")
        
        growth_score = {"high": 0.8, "medium": 0.6, "low": 0.4}.get(growth_potential, 0.5)
        risk_score = {"low": 0.8, "medium": 0.6, "high": 0.3}.get(risk_level, 0.5)
        
        return (growth_score + risk_score) / 2
    
    def _determine_business_stage(self, profile) -> str:
        """Determine business development stage"""
        age = profile.business_age
        revenue = profile.annual_revenue
        
        if age <= 2 and revenue < 500000:
            return "startup"
        elif age <= 7 or revenue < 2000000:
            return "growth"
        else:
            return "mature"
    
    def _assess_amount_justification(self, profile) -> str:
        """Assess if funding amount is reasonable"""
        funding_ratio = profile.funding_amount / max(profile.annual_revenue, 1)
        
        if funding_ratio <= 0.5:
            return "conservative"
        elif funding_ratio <= 1.0:
            return "reasonable"
        elif funding_ratio <= 2.0:
            return "optimistic"
        else:
            return "excessive"
    
    def _assess_sector_risk(self, sector: str) -> str:
        """Assess sector-specific risk"""
        return self.sector_data.get(sector, {}).get("risk_level", "medium")
    
    def _assess_geographic_risk(self, location: str) -> str:
        """Assess geographic risk"""
        region_data = self.regional_data.get(location.lower(), {})
        business_density = region_data.get("business_density", "medium")
        
        risk_mapping = {
            "very_high": "low",
            "high": "low",
            "medium": "medium", 
            "low": "high"
        }
        
        return risk_mapping.get(business_density, "medium")
    
    def _assess_financial_risk(self, profile) -> str:
        """Assess financial risk"""
        financials = profile.financials or {}
        
        cash_flow = financials.get("cash_flow_months", 2)
        profit_margin = financials.get("profit_margin", 0.05)
        
        risk_factors = 0
        if cash_flow < 2:
            risk_factors += 1
        if profit_margin < 0.05:
            risk_factors += 1
        
        if risk_factors >= 2:
            return "high"
        elif risk_factors == 1:
            return "medium"
        else:
            return "low"
    
    def _calculate_overall_risk(self, sector: str, geographic: str, financial: str) -> str:
        """Calculate overall risk profile"""
        risk_scores = {"low": 1, "medium": 2, "high": 3}
        
        total_score = (
            risk_scores[sector] +
            risk_scores[geographic] +
            risk_scores[financial]
        )
        
        avg_score = total_score / 3
        
        if avg_score <= 1.5:
            return "low"
        elif avg_score <= 2.5:
            return "medium"
        else:
            return "high"
    
    def _create_fallback_analysis(self, profile) -> Dict[str, Any]:
        """Create minimal analysis if main analysis fails"""
        return {
            "business_profile": {
                "risk_level": "medium",
                "stage": "unknown",
                "creditworthiness": 0.5,
                "growth_trajectory": "stable",
                "funding_readiness": 0.4,
                "sector_attractiveness": 0.5
            },
            "funding_indicators": {
                "amount_justification": "unknown",
                "repayment_capacity": 0.5,
                "asset_backing": 0.3,
                "management_strength": 0.5
            },
            "matching_tags": [profile.sector, "fallback_analysis"],
            "red_flags": ["incomplete_data"],
            "recommended_funding_types": ["asset_finance", "crowdfunding"]
        }

# Example usage
if __name__ == "__main__":
    analyzer = BusinessAnalyzer()
    print(f"Initialized: {analyzer.__class__.__name__}")
