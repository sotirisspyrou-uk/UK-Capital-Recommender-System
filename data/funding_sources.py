# data/funding_sources.py
# [Version 06-09-2025 17:50:00]
# Funding Sources Database - Complete Structure
# Authored by: Sotiris Spyrou, CEO, VerityAI

"""
Funding Sources Database for the Capital Recommender System.
Manages funding source data with comprehensive UK market coverage.
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class FundingSourcesDB:
    """
    Comprehensive funding sources database for UK market.
    """
    
    def __init__(self):
        self.sources = self._create_comprehensive_sources()
        self.last_updated = datetime.now()
    
    def _create_comprehensive_sources(self) -> List[Dict]:
        """Create comprehensive UK funding sources database"""
        return [
            # Traditional Banking
            {
                "source_id": "barclays_business_loan",
                "name": "Barclays Business Loan",
                "type": "bank_loan",
                "category": "traditional_banking",
                "amount_range": {"min": 5000, "max": 250000},
                "interest_rate_range": {"min": 6.9, "max": 24.9},
                "sectors": ["all"],
                "excluded_sectors": ["gambling", "adult_entertainment"],
                "min_trading_years": 2,
                "min_annual_revenue": 50000,
                "approval_timeline": "2-4 weeks",
                "broker_commission": {"min": 1.5, "max": 3.0},
                "contact": {"email": "business@barclays.co.uk", "phone": "+44 345 734 5345"},
                "availability_status": "accepting_applications",
                "current_appetite": "selective"
            },
            {
                "source_id": "lloyds_asset_finance",
                "name": "Lloyds Asset Finance",
                "type": "asset_finance",
                "category": "traditional_banking",
                "amount_range": {"min": 10000, "max": 2000000},
                "interest_rate_range": {"min": 4.5, "max": 15.0},
                "sectors": ["manufacturing", "construction", "transport", "technology"],
                "excluded_sectors": ["retail", "hospitality"],
                "min_trading_years": 1,
                "min_annual_revenue": 100000,
                "approval_timeline": "1-3 weeks",
                "broker_commission": {"min": 2.0, "max": 5.0},
                "contact": {"email": "commercial@lloydsbank.com", "phone": "+44 345 606 2172"},
                "availability_status": "accepting_applications",
                "current_appetite": "aggressive"
            },
            
            # Investment Capital
            {
                "source_id": "uk_angel_network",
                "name": "UK Angel Investment Network",
                "type": "angel_investment",
                "category": "equity_investment",
                "amount_range": {"min": 25000, "max": 500000},
                "equity_range": {"min": 5, "max": 25},
                "sectors": ["technology", "healthcare", "fintech", "clean_energy"],
                "excluded_sectors": ["retail", "hospitality"],
                "min_trading_years": 0,
                "max_trading_years": 5,
                "approval_timeline": "4-12 weeks",
                "broker_commission": {"min": 3.0, "max": 7.0},
                "contact": {"email": "deals@ukangelnetwork.co.uk", "phone": "+44 207 123 4567"},
                "availability_status": "accepting_applications",
                "current_appetite": "aggressive"
            },
            {
                "source_id": "seedcamp_vc",
                "name": "Seedcamp Venture Capital",
                "type": "venture_capital",
                "category": "equity_investment",
                "amount_range": {"min": 250000, "max": 5000000},
                "equity_range": {"min": 15, "max": 40},
                "sectors": ["technology", "ai", "fintech", "healthtech"],
                "excluded_sectors": ["traditional_retail", "manufacturing"],
                "min_trading_years": 0,
                "max_trading_years": 7,
                "approval_timeline": "8-24 weeks",
                "broker_commission": {"min": 2.0, "max": 5.0},
                "contact": {"email": "applications@seedcamp.com", "phone": "+44 207 183 1855"},
                "availability_status": "accepting_applications",
                "current_appetite": "selective"
            },
            
            # Alternative Funding
            {
                "source_id": "crowdcube",
                "name": "Crowdcube Equity Crowdfunding",
                "type": "crowdfunding",
                "category": "alternative_funding",
                "amount_range": {"min": 10000, "max": 1000000},
                "equity_range": {"min": 5, "max": 30},
                "sectors": ["consumer_products", "technology", "food_drink", "retail"],
                "excluded_sectors": ["gambling", "adult_entertainment"],
                "min_trading_years": 1,
                "approval_timeline": "2-8 weeks",
                "success_rate": 0.45,
                "broker_commission": {"min": 3.0, "max": 8.0},
                "contact": {"email": "partnerships@crowdcube.com", "phone": "+44 117 316 7199"},
                "availability_status": "accepting_applications",
                "current_appetite": "neutral"
            },
            
            # Government Support
            {
                "source_id": "innovate_uk_grant",
                "name": "Innovate UK Smart Grants",
                "type": "government_grant",
                "category": "government_funding",
                "amount_range": {"min": 25000, "max": 500000},
                "grant_percentage": {"min": 70, "max": 100},
                "sectors": ["technology", "healthcare", "clean_energy", "advanced_manufacturing"],
                "excluded_sectors": ["retail", "hospitality", "traditional_services"],
                "min_trading_years": 0,
                "innovation_requirement": True,
                "approval_timeline": "6-16 weeks",
                "broker_commission": {"min": 5.0, "max": 15.0},
                "contact": {"email": "support@innovateuk.ukri.org", "phone": "+44 300 321 4357"},
                "availability_status": "seasonal_rounds",
                "current_appetite": "neutral"
            }
        ]
    
    def get_all_sources(self) -> List[Dict]:
        """Get all funding sources"""
        return self.sources.copy()
    
    def get_source_by_id(self, source_id: str) -> Optional[Dict]:
        """Get funding source by ID"""
        for source in self.sources:
            if source["source_id"] == source_id:
                return source.copy()
        return None
    
    def get_sources_by_type(self, funding_type: str) -> List[Dict]:
        """Get sources by funding type"""
        return [s for s in self.sources if s["type"] == funding_type]
    
    def get_sources_by_amount(self, amount: float) -> List[Dict]:
        """Get sources that accept funding amount"""
        matches = []
        for source in self.sources:
            if (source["amount_range"]["min"] <= amount <= source["amount_range"]["max"]):
                matches.append(source)
        return matches
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            "total_sources": len(self.sources),
            "by_type": self._count_by_type(),
            "by_category": self._count_by_category(),
            "amount_ranges": {
                "min_amount": min(s["amount_range"]["min"] for s in self.sources),
                "max_amount": max(s["amount_range"]["max"] for s in self.sources)
            },
            "last_updated": self.last_updated.isoformat()
        }
    
    def _count_by_type(self) -> Dict[str, int]:
        """Count sources by type"""
        types = {}
        for source in self.sources:
            source_type = source["type"]
            types[source_type] = types.get(source_type, 0) + 1
        return types
    
    def _count_by_category(self) -> Dict[str, int]:
        """Count sources by category"""
        categories = {}
        for source in self.sources:
            category = source["category"]
            categories[category] = categories.get(category, 0) + 1
        return categories

# Create singleton instance
funding_db = FundingSourcesDB()

if __name__ == "__main__":
    print(f"Funding Sources DB initialized with {len(funding_db.sources)} comprehensive sources")
    stats = funding_db.get_database_stats()
    print(f"Types: {list(stats['by_type'].keys())}")
    print(f"Categories: {list(stats['by_category'].keys())}")
    print(f"Amount range: £{stats['amount_ranges']['min_amount']:,} - £{stats['amount_ranges']['max_amount']:,}")
