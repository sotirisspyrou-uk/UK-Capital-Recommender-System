# config.py
# [Version 06-09-2025 17:50:00]
# Capital Recommender System Configuration
# Authored by: Sotiris Spyrou, CEO, VerityAI

"""
Configuration file for UK Capital Recommender System
Contains all variables, settings, and parameters for the recommendation engine.
"""

import os
from typing import Dict, List, Any

# ==================== SYSTEM CONFIGURATION ====================
SYSTEM_VERSION = "1.0.0"
SYSTEM_NAME = "UK Capital Recommender"
AUTHOR = "Sotiris Spyrou, CEO, VerityAI"
CREATED_DATE = "2025-09-06"

# ==================== CORE SETTINGS ====================
class RecommenderConfig:
    # Target Market
    TARGET_COUNTRY = "UK"
    SUPPORTED_REGIONS = ["England", "Scotland", "Wales", "Northern Ireland"]
    PRIMARY_USERS = "financial_brokers"
    
    # Recommendation Parameters
    MAX_RECOMMENDATIONS = 5
    MIN_MATCH_SCORE = 0.6
    CONFIDENCE_THRESHOLD = 0.7
    DIVERSITY_REQUIREMENT = 2  # Max per funding type
    
    # Performance Settings
    PROCESSING_TIMEOUT = 30  # seconds
    MAX_CONCURRENT_REQUESTS = 10
    CACHE_DURATION = 3600  # 1 hour
    
    # Learning & Analytics
    LEARNING_MODE = True
    SUCCESS_TRACKING = True
    PERFORMANCE_MONITORING = True
    
    # Compliance
    REGULATORY_COMPLIANCE = "FCA"
    DATA_PROTECTION = "GDPR"
    AUDIT_LOGGING = True

# ==================== SCORING WEIGHTS ====================
SCORING_WEIGHTS = {
    "compatibility": 0.40,      # Sector, stage, geography alignment
    "approval_probability": 0.35,  # Historical success rates
    "commercial_value": 0.15,   # Broker commission potential
    "strategic_fit": 0.10       # Long-term relationship value
}

# ==================== BUSINESS CLASSIFICATION ====================
BUSINESS_STAGES = {
    "startup": {"min_age": 0, "max_age": 2, "characteristics": ["innovation", "high_growth_potential"]},
    "growth": {"min_age": 2, "max_age": 7, "characteristics": ["scaling", "market_expansion"]},
    "mature": {"min_age": 7, "max_age": 50, "characteristics": ["established", "stable_revenue"]},
    "recovery": {"min_age": 1, "max_age": 50, "characteristics": ["restructuring", "turnaround"]}
}

COMPANY_SIZES = {
    "micro": {"employees": "1-9", "revenue_max": 632000},
    "small": {"employees": "10-49", "revenue_max": 10200000},
    "medium": {"employees": "50-249", "revenue_max": 50000000},
    "large": {"employees": "250+", "revenue_min": 50000000}
}

UK_SECTORS = {
    "technology": {"sic_codes": ["62", "63"], "risk_level": "medium", "growth_potential": "high"},
    "manufacturing": {"sic_codes": ["10-33"], "risk_level": "medium", "growth_potential": "medium"},
    "retail": {"sic_codes": ["45-47"], "risk_level": "high", "growth_potential": "medium"},
    "professional_services": {"sic_codes": ["69-75"], "risk_level": "low", "growth_potential": "medium"},
    "healthcare": {"sic_codes": ["86-88"], "risk_level": "low", "growth_potential": "high"},
    "construction": {"sic_codes": ["41-43"], "risk_level": "high", "growth_potential": "medium"},
    "finance": {"sic_codes": ["64-66"], "risk_level": "medium", "growth_potential": "medium"},
    "education": {"sic_codes": ["85"], "risk_level": "low", "growth_potential": "low"}
}

# ==================== FUNDING SOURCE TYPES ====================
FUNDING_TYPES = {
    "bank_loan": {
        "typical_range": "£5k-£250k",
        "approval_timeline": "2-6 weeks",
        "interest_rate_range": "5-25%",
        "broker_commission": "1-3%"
    },
    "asset_finance": {
        "typical_range": "£10k-£2m",
        "approval_timeline": "1-3 weeks", 
        "interest_rate_range": "4-15%",
        "broker_commission": "2-5%"
    },
    "angel_investment": {
        "typical_range": "£25k-£500k",
        "approval_timeline": "4-12 weeks",
        "equity_range": "5-25%",
        "broker_commission": "3-7%"
    },
    "venture_capital": {
        "typical_range": "£250k-£10m",
        "approval_timeline": "8-24 weeks",
        "equity_range": "15-40%",
        "broker_commission": "2-5%"
    },
    "crowdfunding": {
        "typical_range": "£10k-£1m",
        "approval_timeline": "2-8 weeks",
        "success_rate": "45%",
        "broker_commission": "3-8%"
    },
    "government_grant": {
        "typical_range": "£5k-£500k",
        "approval_timeline": "6-16 weeks",
        "repayment": "none",
        "broker_commission": "5-15%"
    }
}

# ==================== UK REGIONS ====================
UK_REGIONS = {
    "london": {"population": 9500000, "business_density": "very_high", "funding_availability": "excellent"},
    "south_east": {"population": 9270000, "business_density": "high", "funding_availability": "good"},
    "north_west": {"population": 7420000, "business_density": "medium", "funding_availability": "good"},
    "scotland": {"population": 5480000, "business_density": "medium", "funding_availability": "good"},
    "yorkshire": {"population": 5500000, "business_density": "medium", "funding_availability": "fair"},
    "west_midlands": {"population": 6000000, "business_density": "medium", "funding_availability": "fair"},
    "wales": {"population": 3130000, "business_density": "low", "funding_availability": "fair"},
    "northern_ireland": {"population": 1900000, "business_density": "low", "funding_availability": "limited"}
}

# ==================== ERROR HANDLING ====================
ERROR_CODES = {
    "INVALID_INPUT": 1001,
    "INSUFFICIENT_DATA": 1002,
    "NO_MATCHES_FOUND": 1003,
    "API_TIMEOUT": 1004,
    "SYSTEM_OVERLOAD": 1005,
    "COMPLIANCE_VIOLATION": 1006
}

ERROR_MESSAGES = {
    1001: "Invalid business profile data provided",
    1002: "Insufficient information to generate recommendations", 
    1003: "No suitable funding sources found for this profile",
    1004: "External API request timed out",
    1005: "System temporarily overloaded, please retry",
    1006: "Request violates regulatory compliance rules"
}

# Export main configuration
CONFIG = RecommenderConfig()

print(f"Configuration loaded: {SYSTEM_NAME} v{SYSTEM_VERSION}")
