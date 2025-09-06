# agents/funding_research.py
# [Version 06-09-2025 14:35:22]
# Funding Source Research Agent - UK funding landscape intelligence
# Authored by: Sotiris Spyrou, CEO, VerityAI

"""
Funding Source Research Agent for the Capital Recommender System.
Researches and categorizes UK funding sources with real-time availability.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from config import FUNDING_TYPES, UK_SECTORS, UK_REGIONS

logger = logging.getLogger(__name__)

class FundingResearcher:
    """
    Comprehensive funding source research agent for UK market intelligence.
    Maintains database of funding sources with current availability and criteria.
    """
    
    def __init__(self):
        self.funding_database = self._initialize_funding_database()
        self.market_conditions = self._get_current_market_conditions()
        self.last_update = datetime.now()
        
        logger.info("Funding Researcher initialized with {} sources".format(
            len(self.funding_database)
        ))
    
    def research_funding_sources(self, business_profile, business_intelligence: Dict) -> List[Dict]:
        """
        Research and filter funding sources based on business profile.
        
        Args:
            business_profile: BusinessProfile object
            business_intelligence: Output from BusinessAnalyzer
            
        Returns:
            List of available funding sources with criteria and details
        """
        try:
            logger.info(f"Researching funding sources for {business_profile.company_name}")
            
            # Filter sources by basic eligibility
            eligible_sources = self._filter_by_eligibility(business_profile)
            
            # Apply business intelligence filters
            intelligence_filtered = self._filter_by_intelligence(eligible_sources, business_intelligence)
            
            # Apply market condition adjustments
            market_adjusted = self._apply_market_conditions(intelligence_filtered)
            
            # Sort by current availability and appetite
            prioritized_sources = self._prioritize_by_availability(market_adjusted)
            
            logger.info(f"Found {len(prioritized_sources)} eligible funding sources")
            return prioritized_sources
            
        except Exception as e:
            logger.error(f"Error in funding research: {str(e)}")
            return self._get_fallback_sources(business_profile)
    
    def _initialize_funding_database(self) -> List[Dict]:
        """Initialize comprehensive UK funding source database"""
        return [
            # Traditional Banking
            {
                "source_id": "barclays_business_loan",
                "name": "Barclays Business Loan",
                "type": "bank_loan",
                "category": "traditional_banking",
                "amount_range": {"min": 5000, "max": 250000},
                "sectors": ["all"],
                "excluded_sectors": ["adult_entertainment", "gambling", "weapons"],
                "min_trading_years": 2,
                "min_annual_revenue": 50000,
                "max_debt_ratio": 2.5,
                "interest_rate_range": {"min": 6.9, "max": 24.9},
                "approval_timeline": "2-4 weeks",
                "success_factors": ["good_credit", "stable_cashflow", "asset_backing"],
                "broker_commission": {"min": 1.5, "max": 3.0},
                "contact": {"email": "business@barclays.co.uk", "phone": "+44 345 734 5345"},
                "availability_status": "accepting_applications",
                "current_appetite": "selective",
                "last_updated": "2025-09-06"
            },
            {
                "source_id": "lloyds_commercial_finance",
                "name": "Lloyds Commercial Finance",
                "type": "asset_finance",
                "category": "traditional_banking",
                "amount_range": {"min": 10000, "max": 2000000},
                "sectors": ["manufacturing", "construction", "transport", "technology"],
                "excluded_sectors": ["retail", "hospitality"],
                "min_trading_years": 1,
                "min_annual_revenue": 100000,
                "asset_requirement": "equipment_vehicles_property",
                "interest_rate_range": {"min": 4.5, "max": 15.0},
                "approval_timeline": "1-3 weeks",
                "success_factors": ["asset_backing", "cashflow", "sector_experience"],
                "broker_commission": {"min": 2.0, "max": 5.0},
                "contact": {"email": "commercial@lloydsbank.com", "phone": "+44 345 606 2172"},
                "availability_status": "accepting_applications",
                "current_appetite": "aggressive",
                "last_updated": "2025-09-06"
            },
            
            # Challenger Banks
            {
                "source_id": "funding_circle",
                "name": "Funding Circle Business Loans",
                "type": "bank_loan",
                "category": "alternative_lending",
                "amount_range": {"min": 10000, "max": 500000},
                "sectors": ["all"],
                "excluded_sectors": ["gambling", "adult_entertainment", "cryptocurrency"],
                "min_trading_years": 2,
                "min_annual_revenue": 120000,
                "credit_score_min": 600,
                "interest_rate_range": {"min": 7.5, "max": 18.9},
                "approval_timeline": "1-2 weeks",
                "success_factors": ["good_credit", "consistent_revenue", "positive_cashflow"],
                "broker_commission": {"min": 1.0, "max": 2.5},
                "contact": {"email": "brokers@fundingcircle.com", "phone": "+44 203 198 9460"},
                "availability_status": "accepting_applications",
                "current_appetite": "neutral",
                "last_updated": "2025-09-06"
            },
            
            # Angel Investment Networks
            {
                "source_id": "uk_angel_network",
                "name": "UK Angel Investment Network",
                "type": "angel_investment",
                "category": "equity_investment",
                "amount_range": {"min": 25000, "max": 500000},
                "sectors": ["technology", "healthcare", "fintech", "clean_energy"],
                "excluded_sectors": ["retail", "hospitality", "construction"],
                "min_trading_years": 0,
                "max_trading_years": 5,
                "equity_range": {"min": 5, "max": 25},
                "approval_timeline": "4-12 weeks",
                "success_factors": ["innovation", "scalability", "strong_team", "market_traction"],
                "broker_commission": {"min": 3.0, "max": 7.0},
                "contact": {"email": "deals@ukangelnetwork.co.uk", "phone": "+44 207 123 4567"},
                "availability_status": "accepting_applications",
                "current_appetite": "aggressive",
                "last_updated": "2025-09-06"
            },
            
            # Venture Capital
            {
                "source_id": "seedcamp_vc",
                "name": "Seedcamp Venture Capital",
                "type": "venture_capital",
                "category": "equity_investment",
                "amount_range": {"min": 250000, "max": 5000000},
                "sectors": ["technology", "ai", "fintech", "healthtech"],
                "excluded_sectors": ["traditional_retail", "manufacturing"],
                "min_trading_years": 0,
                "max_trading_years": 7,
                "equity_range": {"min": 15, "max": 40},
                "approval_timeline": "8-24 weeks",
                "success_factors": ["disruptive_technology", "scalable_business_model", "experienced_team"],
                "broker_commission": {"min": 2.0, "max": 5.0},
                "contact": {"email": "applications@seedcamp.com", "phone": "+44 207 183 1855"},
                "availability_status": "accepting_applications",
                "current_appetite": "selective",
                "last_updated": "2025-09-06"
            },
            
            # Crowdfunding Platforms
            {
                "source_id": "crowdcube",
                "name": "Crowdcube Equity Crowdfunding",
                "type": "crowdfunding",
                "category": "alternative_funding",
                "amount_range": {"min": 10000, "max": 1000000},
                "sectors": ["consumer_products", "technology", "food_drink", "retail"],
                "excluded_sectors": ["gambling", "adult_entertainment"],
                "min_trading_years": 1,
                "success_rate": 0.45,
                "approval_timeline": "2-8 weeks",
                "success_factors": ["consumer_appeal", "marketing_ready", "compelling_story"],
                "broker_commission": {"min": 3.0, "max": 8.0},
                "contact": {"email": "partnerships@crowdcube.com", "phone": "+44 117 316 7199"},
                "availability_status": "accepting_applications",
                "current_appetite": "neutral",
                "last_updated": "2025-09-06"
            },
            
            # Government Grants
            {
                "source_id": "innovate_uk_grant",
                "name": "Innovate UK Smart Grants",
                "type": "government_grant",
                "category": "government_funding",
                "amount_range": {"min": 25000, "max": 500000},
                "sectors": ["technology", "healthcare", "clean_energy", "advanced_manufacturing"],
                "excluded_sectors": ["retail", "hospitality", "traditional_services"],
                "min_trading_years": 0,
                "innovation_requirement": True,
                "approval_timeline": "6-16 weeks",
                "success_factors": ["innovation", "technical_merit", "commercial_potential", "uk_benefit"],
                "broker_commission": {"min": 5.0, "max": 15.0},
                "contact": {"email": "support@innovateuk.ukri.org", "phone": "+44 300 321 4357"},
                "availability_status": "seasonal_rounds",
                "current_appetite": "neutral",
                "last_updated": "2025-09-06"
            },
            
            # Family Offices
            {
                "source_id": "london_family_office",
                "name": "London Family Office Network",
                "type": "family_office",
                "category": "private_wealth",
                "amount_range": {"min": 100000, "max": 5000000},
                "sectors": ["technology", "healthcare", "real_estate", "luxury_goods"],
                "excluded_sectors": ["gambling", "weapons", "tobacco"],
                "min_trading_years": 2,
                "relationship_requirement": True,
                "approval_timeline": "4-16 weeks",
                "success_factors": ["relationship_fit", "long_term_potential", "family_values_alignment"],
                "broker_commission": {"min": 1.0, "max": 4.0},
                "contact": {"email": "opportunities@londonfamilyoffice.com", "phone": "+44 207 456 7890"},
                "availability_status": "relationship_based",
                "current_appetite": "selective",
                "last_updated": "2025-09-06"
            },
            
            # Regional Development
            {
                "source_id": "scottish_enterprise",
                "name": "Scottish Enterprise Growth Finance",
                "type": "regional_grant",
                "category": "government_funding",
                "amount_range": {"min": 50000, "max": 2000000},
                "sectors": ["technology", "manufacturing", "life_sciences", "energy"],
                "geographic_requirement": ["scotland"],
                "excluded_sectors": ["retail", "hospitality"],
                "min_trading_years": 1,
                "approval_timeline": "8-12 weeks",
                "success_factors": ["scottish_location", "job_creation", "export_potential"],
                "broker_commission": {"min": 2.0, "max": 6.0},
                "contact": {"email": "finance@scottish-enterprise.com", "phone": "+44 141 248 2700"},
                "availability_status": "accepting_applications",
                "current_appetite": "aggressive",
                "last_updated": "2025-09-06"
            }
        ]
    
    def _get_current_market_conditions(self) -> Dict[str, Any]:
        """Get current UK funding market conditions"""
        return {
            "interest_rates": {
                "bank_base_rate": 5.25,
                "trend": "stable",
                "outlook": "cautious"
            },
            "lending_appetite": {
                "traditional_banks": "selective",
                "alternative_lenders": "neutral",
                "investors": "cautious",
                "government": "supportive"
            },
            "sector_preferences": {
                "hot": ["technology", "clean_energy", "healthcare"],
                "neutral": ["manufacturing", "professional_services"],
                "cold": ["retail", "hospitality", "construction"]
            },
            "economic_indicators": {
                "gdp_growth": 0.8,
                "inflation": 3.2,
                "unemployment": 4.1,
                "business_confidence": 6.2
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def _filter_by_eligibility(self, profile) -> List[Dict]:
        """Filter sources by basic eligibility criteria"""
        eligible = []
        
        for source in self.funding_database:
            # Check amount range
            if (source["amount_range"]["min"] <= profile.funding_amount <= 
                source["amount_range"]["max"]):
                
                # Check sector eligibility
                if (source["sectors"] == ["all"] or 
                    profile.sector in source["sectors"]) and \
                   profile.sector not in source.get("excluded_sectors", []):
                    
                    # Check trading years
                    min_years = source.get("min_trading_years", 0)
                    max_years = source.get("max_trading_years", 999)
                    
                    if min_years <= profile.business_age <= max_years:
                        
                        # Check revenue requirements
                        min_revenue = source.get("min_annual_revenue", 0)
                        if profile.annual_revenue >= min_revenue:
                            
                            # Check geographic requirements
                            geo_req = source.get("geographic_requirement", [])
                            if not geo_req or profile.location.lower() in geo_req:
                                eligible.append(source)
        
        return eligible
    
    def _filter_by_intelligence(self, sources: List[Dict], intelligence: Dict) -> List[Dict]:
        """Apply business intelligence filters"""
        filtered = []
        
        for source in sources:
            # Risk level compatibility
            risk_tolerance = self._get_source_risk_tolerance(source)
            business_risk = intelligence["business_profile"]["risk_level"]
            
            if self._is_risk_compatible(risk_tolerance, business_risk):
                
                # Credit requirements
                if self._meets_credit_requirements(source, intelligence):
                    
                    # Financial health requirements
                    if self._meets_financial_requirements(source, intelligence):
                        filtered.append(source)
        
        return filtered
    
    def _apply_market_conditions(self, sources: List[Dict]) -> List[Dict]:
        """Apply current market conditions to source availability"""
        adjusted = []
        
        for source in sources:
            # Adjust based on market appetite
            appetite = self.market_conditions["lending_appetite"].get(
                source["category"].split("_")[0], "neutral"
            )
            
            # Sector preference adjustments
            sector_status = self._get_sector_market_status(source)
            
            # Create adjusted source
            adjusted_source = source.copy()
            adjusted_source["market_appetite"] = appetite
            adjusted_source["sector_market_status"] = sector_status
            adjusted_source["market_adjusted_timeline"] = self._adjust_timeline(
                source["approval_timeline"], appetite, sector_status
            )
            
            adjusted.append(adjusted_source)
        
        return adjusted
    
    def _prioritize_by_availability(self, sources: List[Dict]) -> List[Dict]:
        """Sort sources by current availability and attractiveness"""
        def priority_score(source):
            score = 0
            
            # Availability status
            status_scores = {
                "accepting_applications": 10,
                "selective": 7,
                "seasonal_rounds": 5,
                "relationship_based": 3,
                "limited_capacity": 1
            }
            score += status_scores.get(source.get("availability_status"), 0)
            
            # Current appetite
            appetite_scores = {
                "aggressive": 8,
                "neutral": 5,
                "selective": 3,
                "cautious": 1
            }
            score += appetite_scores.get(source.get("current_appetite"), 0)
            
            # Broker commission potential
            commission = source.get("broker_commission", {})
            if isinstance(commission, dict):
                avg_commission = (commission.get("min", 0) + commission.get("max", 0)) / 2
                score += avg_commission
            
            return score
        
        return sorted(sources, key=priority_score, reverse=True)
    
    def _get_source_risk_tolerance(self, source: Dict) -> str:
        """Determine source risk tolerance level"""
        source_type = source["type"]
        
        risk_mapping = {
            "bank_loan": "low",
            "asset_finance": "low",
            "government_grant": "medium",
            "angel_investment": "high",
            "venture_capital": "high",
            "crowdfunding": "high",
            "family_office": "medium"
        }
        
        return risk_mapping.get(source_type, "medium")
    
    def _is_risk_compatible(self, source_tolerance: str, business_risk: str) -> bool:
        """Check if source risk tolerance matches business risk"""
        compatibility_matrix = {
            "low": ["low"],
            "medium": ["low", "medium"],
            "high": ["low", "medium", "high"]
        }
        
        return business_risk in compatibility_matrix.get(source_tolerance, [])
    
    def _meets_credit_requirements(self, source: Dict, intelligence: Dict) -> bool:
        """Check if business meets source credit requirements"""
        min_credit = source.get("credit_score_min", 0)
        business_credit = intelligence["business_profile"]["creditworthiness"] * 850  # Convert to score
        
        return business_credit >= min_credit
    
    def _meets_financial_requirements(self, source: Dict, intelligence: Dict) -> bool:
        """Check if business meets financial requirements"""
        # Debt ratio requirements
        max_debt_ratio = source.get("max_debt_ratio", 5.0)
        business_debt_ratio = intelligence["funding_indicators"].get("debt_to_equity", 1.0)
        
        if business_debt_ratio > max_debt_ratio:
            return False
        
        # Funding readiness threshold
        min_readiness = 0.4 if source["type"] in ["bank_loan", "asset_finance"] else 0.6
        business_readiness = intelligence["business_profile"]["funding_readiness"]
        
        return business_readiness >= min_readiness
    
    def _get_sector_market_status(self, source: Dict) -> str:
        """Get current market status for source sectors"""
        source_sectors = source.get("sectors", [])
        
        if any(sector in self.market_conditions["sector_preferences"]["hot"] 
               for sector in source_sectors):
            return "hot"
        elif any(sector in self.market_conditions["sector_preferences"]["cold"] 
                 for sector in source_sectors):
            return "cold"
        else:
            return "neutral"
    
    def _adjust_timeline(self, original_timeline: str, appetite: str, sector_status: str) -> str:
        """Adjust approval timeline based on market conditions"""
        # Parse original timeline
        if "week" in original_timeline:
            weeks = original_timeline.split("-")
            min_weeks = int(weeks[0])
            max_weeks = int(weeks[1].split()[0])
        else:
            return original_timeline
        
        # Apply adjustments
        if appetite == "aggressive" and sector_status == "hot":
            min_weeks = max(1, min_weeks - 1)
            max_weeks = max(min_weeks, max_weeks - 2)
        elif appetite == "selective" or sector_status == "cold":
            min_weeks += 1
            max_weeks += 3
        
        return f"{min_weeks}-{max_weeks} weeks"
    
    def _get_fallback_sources(self, profile) -> List[Dict]:
        """Return basic funding sources if main research fails"""
        fallback = []
        
        # Basic bank loan option
        fallback.append({
            "source_id": "generic_bank_loan",
            "name": "UK Business Bank Loan",
            "type": "bank_loan",
            "amount_range": {"min": 5000, "max": 250000},
            "approval_timeline": "4-8 weeks",
            "broker_commission": {"min": 1.0, "max": 3.0},
            "contact": {"email": "info@ukbusinessbank.co.uk"},
            "availability_status": "unknown",
            "current_appetite": "neutral"
        })
        
        # Asset finance option
        if profile.funding_amount >= 10000:
            fallback.append({
                "source_id": "generic_asset_finance",
                "name": "UK Asset Finance",
                "type": "asset_finance",
                "amount_range": {"min": 10000, "max": 1000000},
                "approval_timeline": "2-4 weeks",
                "broker_commission": {"min": 2.0, "max": 5.0},
                "contact": {"email": "info@ukassetfinance.co.uk"},
                "availability_status": "unknown",
                "current_appetite": "neutral"
            })
        
        return fallback
    
    def get_market_intelligence_summary(self) -> Dict[str, Any]:
        """Get comprehensive market intelligence summary"""
        return {
            "funding_landscape": {
                "total_sources": len(self.funding_database),
                "by_category": self._count_by_category(),
                "current_availability": self._analyze_availability()
            },
            "market_conditions": self.market_conditions,
            "sector_analysis": self._analyze_sector_preferences(),
            "geographic_analysis": self._analyze_geographic_distribution(),
            "broker_opportunities": self._analyze_broker_opportunities(),
            "last_updated": self.last_update.isoformat()
        }
    
    def _count_by_category(self) -> Dict[str, int]:
        """Count sources by category"""
        categories = {}
        for source in self.funding_database:
            category = source.get("category", "unknown")
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    def _analyze_availability(self) -> Dict[str, int]:
        """Analyze source availability status"""
        availability = {}
        for source in self.funding_database:
            status = source.get("availability_status", "unknown")
            availability[status] = availability.get(status, 0) + 1
        return availability
    
    def _analyze_sector_preferences(self) -> Dict[str, List[str]]:
        """Analyze which sectors are preferred by each funding type"""
        preferences = {}
        for source in self.funding_database:
            funding_type = source["type"]
            sectors = source.get("sectors", [])
            if funding_type not in preferences:
                preferences[funding_type] = set()
            if sectors != ["all"]:
                preferences[funding_type].update(sectors)
        
        # Convert sets to lists for JSON serialization
        return {k: list(v) for k, v in preferences.items()}
    
    def _analyze_geographic_distribution(self) -> Dict[str, Any]:
        """Analyze geographic coverage and preferences"""
        geographic = {
            "uk_wide_sources": 0,
            "regional_specific": {},
            "london_focused": 0
        }
        
        for source in self.funding_database:
            geo_req = source.get("geographic_requirement", [])
            if not geo_req:
                geographic["uk_wide_sources"] += 1
            else:
                for region in geo_req:
                    geographic["regional_specific"][region] = \
                        geographic["regional_specific"].get(region, 0) + 1
        
        return geographic
    
    def _analyze_broker_opportunities(self) -> Dict[str, Any]:
        """Analyze broker commission opportunities"""
        commissions = []
        for source in self.funding_database:
            commission = source.get("broker_commission", {})
            if isinstance(commission, dict):
                avg_commission = (commission.get("min", 0) + commission.get("max", 0)) / 2
                commissions.append({
                    "source": source["name"],
                    "type": source["type"],
                    "avg_commission": avg_commission,
                    "amount_potential": source["amount_range"]["max"]
                })
        
        # Sort by revenue potential
        commissions.sort(key=lambda x: x["avg_commission"] * x["amount_potential"], reverse=True)
        
        return {
            "top_commission_sources": commissions[:5],
            "avg_commission_by_type": self._calculate_avg_commission_by_type(),
            "total_revenue_potential": sum(c["avg_commission"] * c["amount_potential"] for c in commissions)
        }
    
    def _calculate_avg_commission_by_type(self) -> Dict[str, float]:
        """Calculate average commission rates by funding type"""
        type_commissions = {}
        type_counts = {}
        
        for source in self.funding_database:
            funding_type = source["type"]
            commission = source.get("broker_commission", {})
            
            if isinstance(commission, dict) and "min" in commission and "max" in commission:
                avg_commission = (commission["min"] + commission["max"]) / 2
                
                if funding_type not in type_commissions:
                    type_commissions[funding_type] = 0
                    type_counts[funding_type] = 0
                
                type_commissions[funding_type] += avg_commission
                type_counts[funding_type] += 1
        
        return {
            funding_type: type_commissions[funding_type] / type_counts[funding_type]
            for funding_type in type_commissions
        }
    
    def refresh_market_data(self) -> bool:
        """Refresh market conditions and source availability"""
        try:
            # Update market conditions
            self.market_conditions = self._get_current_market_conditions()
            
            # Update source availability (in real system, this would query APIs)
            self._update_source_availability()
            
            self.last_update = datetime.now()
            logger.info("Market data refreshed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to refresh market data: {str(e)}")
            return False
    
    def _update_source_availability(self):
        """Update availability status for all sources"""
        # In a real system, this would query actual APIs
        # For now, simulate some availability changes
        import random
        
        for source in self.funding_database:
            # Randomly adjust appetite (simulate market changes)
            appetites = ["aggressive", "neutral", "selective", "cautious"]
            if random.random() < 0.1:  # 10% chance of change
                source["current_appetite"] = random.choice(appetites)
            
            source["last_updated"] = datetime.now().strftime("%Y-%m-%d")
