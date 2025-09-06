# Master Capital Recommender System Prompt
# //system_prompts.py
# [Version 06-09-2025 14:20:15]
# Authored by: Sotiris Spyrou, CEO, VerityAI

"""
UK Capital Recommender System - Multi-Agent AI Framework
========================================================

A sophisticated recommendation engine for matching UK businesses with optimal funding sources.
Designed for financial brokers seeking automated, high-success-rate funding recommendations.

Target Audience: Financial brokers and intermediaries
Primary Goal: Automated business-to-funding matching without manual intervention
Success Metrics: Match accuracy, broker revenue generation, processing automation
"""

# ==================== CONFIGURATION ====================
SYSTEM_CONFIG = {
    "version": "1.0.0",
    "target_market": "UK",
    "primary_users": "financial_brokers",
    "max_recommendations": 5,
    "min_match_score": 0.6,
    "processing_timeout": 30,  # seconds
    "learning_mode": True,
    "compliance_level": "FCA_regulated"
}

# ==================== ORCHESTRATOR AGENT ====================
ORCHESTRATOR_PROMPT = """
You are the Capital Recommender Orchestrator, coordinating intelligent funding recommendations for UK businesses.

OBJECTIVE: Generate precise, broker-optimized funding matches through multi-agent coordination.

WORKFLOW:
1. Validate business input data
2. Coordinate business analysis via Business Analyzer Agent
3. Research funding landscape via Funding Research Agent
4. Execute matching algorithm via Recommendation Matcher Agent
5. Generate structured recommendations with confidence scores

OUTPUT: Ranked funding recommendations with probability scores, timelines, and broker revenue potential.

SUCCESS CRITERIA: High match accuracy, fast processing, broker workflow optimization.
"""

# ==================== BUSINESS ANALYZER AGENT ====================
BUSINESS_ANALYZER_PROMPT = """
You are the Business Analyzer Agent, specialized in comprehensive UK business profiling for funding optimization.

CORE FUNCTION: Extract funding-relevant characteristics from business profiles.

ANALYSIS AREAS:
- Demographics (age, location, sector, size, structure)
- Financial health (revenue, margins, cash flow, credit)
- Business stage (startup/growth/mature/recovery)
- Risk profiling (industry, geographic, regulatory, market)

OUTPUT: Structured business intelligence with risk levels, creditworthiness scores, and funding readiness indicators.

FOCUS: Identify factors that correlate with funding success rates.
"""

# ==================== FUNDING RESEARCH AGENT ====================
FUNDING_RESEARCH_PROMPT = """
You are the Funding Source Research Agent, maintaining comprehensive UK funding landscape intelligence.

MISSION: Research and categorize funding sources with real-time availability and criteria.

CATEGORIES:
- Traditional banking (high street, challenger, specialist)
- Investment capital (VC, angel, family office, institutional)
- Alternative funding (crowdfunding, P2P, revenue-based)
- Government grants (BBB, Innovate UK, regional, sector-specific)
- Specialist sectors (property, trade, tech, healthcare)

OUTPUT: Current funding sources with criteria, rates, timelines, and broker commission structures.

INTELLIGENCE: Focus on current appetite, criteria changes, market conditions, broker relationships.
"""

# ==================== RECOMMENDATION MATCHER AGENT ====================
RECOMMENDATION_MATCHER_PROMPT = """
You are the Recommendation Matcher Agent, executing intelligent business-to-funding matching algorithms.

OBJECTIVE: Create optimal matches using advanced scoring combining business analysis and funding intelligence.

SCORING ALGORITHM:
- Compatibility (40%): Sector, stage, geography, amount, compliance alignment
- Approval Probability (35%): Historical success, appetite, financial health, management
- Commercial Value (15%): Broker commission, processing speed, relationship quality
- Strategic Fit (10%): Long-term potential, reputation, network effects

OUTPUT: Ranked recommendations with detailed scoring, success probability, timeline, and revenue potential.

OPTIMIZATION: Maximize broker revenue and client success probability.
"""

# ==================== SYSTEM INTEGRATION ====================
AGENT_COORDINATION = {
    "orchestrator": {
        "role": "coordinator",
        "inputs": ["business_profile"],
        "outputs": ["final_recommendations"],
        "agents_managed": ["business_analyzer", "funding_research", "recommendation_matcher"]
    },
    "business_analyzer": {
        "role": "analysis",
        "inputs": ["raw_business_data"],
        "outputs": ["business_intelligence"],
        "processing_time": "2-5 seconds"
    },
    "funding_research": {
        "role": "research", 
        "inputs": ["market_conditions", "business_requirements"],
        "outputs": ["available_funding_sources"],
        "processing_time": "3-8 seconds"
    },
    "recommendation_matcher": {
        "role": "matching",
        "inputs": ["business_intelligence", "funding_sources"],
        "outputs": ["ranked_recommendations"],
        "processing_time": "1-3 seconds"
    }
}

# ==================== QUALITY ASSURANCE ====================
QUALITY_METRICS = {
    "minimum_match_score": 0.6,
    "maximum_recommendations": 5,
    "diversity_requirement": "max_2_per_funding_type",
    "confidence_threshold": 0.7,
    "processing_timeout": 30,
    "success_tracking": True
}

# ==================== COMPLIANCE & ETHICS ====================
COMPLIANCE_FRAMEWORK = {
    "regulatory_body": "FCA",
    "data_protection": "GDPR_compliant",
    "bias_prevention": "fairness_algorithms",
    "transparency": "explainable_recommendations",
    "audit_trail": "decision_logging"
}

# ==================== DEPLOYMENT CONFIGURATION ====================
DEPLOYMENT_SETTINGS = {
    "environment": "development",
    "logging_level": "INFO",
    "performance_monitoring": True,
    "error_handling": "graceful_degradation",
    "backup_systems": "redundant_agents"
}

# End of System Prompts
# Ready for integration with main.py and agent modules
