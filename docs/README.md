# UK Capital Recommender System

**Intelligent funding recommendation engine for UK businesses**

## Overview

The UK Capital Recommender System is a sophisticated multi-agent AI platform that matches UK businesses with optimal funding sources. Built specifically for financial brokers, it provides automated, high-accuracy funding recommendations without manual intervention.

### Key Features

- **Multi-Agent Architecture**: Orchestrated business analysis, funding research, and intelligent matching
- **UK Market Focus**: Comprehensive database of UK funding sources and market intelligence
- **Broker Optimized**: Revenue-focused recommendations with commission tracking
- **4D Scoring Algorithm**: Compatibility + Approval Probability + Commercial Value + Strategic Fit
- **Real-time Intelligence**: Current market conditions and funding source appetite

## Quick Start

1. **Setup the project:**
   ```bash
   ./setup_project.sh
   ```

2. **Run the demonstration:**
   ```bash
   python main.py
   ```

3. **Review the results:**
   The system will display intelligent funding recommendations for a sample UK business.

## Project Structure

```
uk-capital-recommender/
├── main.py                      # Main orchestrator and entry point
├── config.py                    # Complete UK market configuration
├── requirements.txt             # Python dependencies
├── agents/
│   ├── __init__.py             # Agent package initialization
│   ├── business_analyzer.py    # Sophisticated business profiling
│   ├── funding_research.py     # UK funding landscape intelligence
│   └── recommendation_matcher.py # Advanced matching algorithms
├── data/
│   ├── __init__.py             # Data package initialization
│   └── funding_sources.py      # UK funding sources database
├── docs/
│   ├── README.md               # This file
│   └── Claude.md               # Technical handoff documentation
├── tests/
│   ├── __init__.py             # Test package initialization
│   └── test_basic.py           # Basic validation tests
├── examples/
│   └── basic_usage.py          # Usage examples
└── logs/                       # System logs (auto-generated)
```

## System Architecture

```
Business Profile Input
        ↓
Business Analyzer Agent → Business Intelligence
        ↓
Funding Research Agent → Available Sources + Market Intelligence
        ↓
Recommendation Matcher → 4D Scored Matches
        ↓
Main Orchestrator → Final Ranked Recommendations
```

## Usage Example

```python
from main import CapitalRecommenderOrchestrator

# Initialize the system
orchestrator = CapitalRecommenderOrchestrator()

# Define business profile
business_data = {
    "company_name": "TechStart Solutions Ltd",
    "sector": "technology",
    "annual_revenue": 450000,
    "employees": 12,
    "location": "london",
    "business_age": 3,
    "funding_amount": 250000,
    "funding_purpose": "expansion",
    "timeline": "3_months"
}

# Get recommendations
result = orchestrator.process_recommendation_request(business_data)

# Display results
if result["success"]:
    for rec in result["recommendations"]:
        print(f"{rec['rank']}. {rec['funding_source']} - Score: {rec['match_score']}")
```

## Configuration

The system includes comprehensive UK market data in `config.py`:

- **8 Business Sectors**: Technology, Manufacturing, Retail, etc.
- **8 UK Regions**: London, Scotland, Wales, etc.
- **7 Funding Types**: Bank loans, VC, Angel, Crowdfunding, etc.
- **4D Scoring Weights**: Configurable algorithm parameters

## Next Steps

- Deploy to web interface using Next.js + Supabase
- Integrate real-time APIs (Companies House, Credit agencies)
- Add machine learning models for enhanced scoring
- Scale to production with enterprise features

## Author

Sotiris Spyrou, CEO, VerityAI  
Date: September 6, 2025

**Ready for Claude Code handoff and production development!**
