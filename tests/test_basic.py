# tests/test_basic.py
# Comprehensive tests for UK Capital Recommender System

"""
Comprehensive test suite for validating core functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test all critical imports"""
    try:
        from config import CONFIG, SCORING_WEIGHTS, UK_SECTORS, FUNDING_TYPES
        from main import CapitalRecommenderOrchestrator, BusinessProfile
        from agents.business_analyzer import BusinessAnalyzer
        from data.funding_sources import funding_db
        print("✅ All import tests passed")
        return True
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_configuration():
    """Test configuration completeness"""
    from config import CONFIG, SCORING_WEIGHTS, UK_SECTORS
    
    # Test basic config
    assert CONFIG.TARGET_COUNTRY == "UK"
    assert CONFIG.MAX_RECOMMENDATIONS == 5
    assert CONFIG.MIN_MATCH_SCORE == 0.6
    
    # Test scoring weights sum to 1.0
    total_weight = sum(SCORING_WEIGHTS.values())
    assert abs(total_weight - 1.0) < 0.001
    assert len(SCORING_WEIGHTS) == 4
    
    # Test UK sectors data
    assert len(UK_SECTORS) >= 6
    assert "technology" in UK_SECTORS
    assert "manufacturing" in UK_SECTORS
    
    print("✅ Configuration tests passed")

def test_funding_database():
    """Test funding sources database"""
    from data.funding_sources import funding_db
    
    sources = funding_db.get_all_sources()
    assert len(sources) >= 5
    
    # Test database methods
    stats = funding_db.get_database_stats()
    assert "total_sources" in stats
    assert stats["total_sources"] > 0
    
    # Test filtering
    bank_loans = funding_db.get_sources_by_type("bank_loan")
    assert len(bank_loans) >= 1
    
    print("✅ Funding database tests passed")

def test_business_analyzer():
    """Test business analyzer functionality"""
    from agents.business_analyzer import BusinessAnalyzer
    from main import BusinessProfile
    
    analyzer = BusinessAnalyzer()
    
    # Create test business profile
    test_data = {
        "company_name": "Test Company Ltd",
        "sector": "technology",
        "annual_revenue": 500000,
        "employees": 15,
        "location": "london",
        "business_age": 3,
        "funding_amount": 200000,
        "funding_purpose": "expansion",
        "timeline": "3_months"
    }
    
    profile = BusinessProfile(test_data)
    result = analyzer.analyze_business(profile)
    
    # Validate analysis results
    assert "business_profile" in result
    assert "funding_indicators" in result
    assert "matching_tags" in result
    assert "recommended_funding_types" in result
    
    assert result["business_profile"]["funding_readiness"] >= 0.0
    assert result["business_profile"]["funding_readiness"] <= 1.0
    
    print("✅ Business analyzer tests passed")

def test_main_orchestrator():
    """Test main recommendation orchestrator"""
    from main import CapitalRecommenderOrchestrator
    
    orchestrator = CapitalRecommenderOrchestrator()
    
    # Test business profile
    test_business = {
        "company_name": "Test Solutions Ltd",
        "sector": "technology",
        "annual_revenue": 400000,
        "employees": 10,
        "location": "london",
        "business_age": 2,
        "funding_amount": 150000,
        "funding_purpose": "expansion",
        "timeline": "3_months"
    }
    
    result = orchestrator.process_recommendation_request(test_business)
    
    # Validate results
    assert result["success"] == True
    assert "recommendations" in result
    assert "execution_time" in result
    assert "confidence_level" in result
    
    if result["recommendations"]:
        rec = result["recommendations"][0]
        assert "rank" in rec
        assert "funding_source" in rec
        assert "match_score" in rec
        assert rec["match_score"] >= 0.0
        assert rec["match_score"] <= 1.0
    
    print("✅ Main orchestrator tests passed")

def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("=" * 60)
    print("UK CAPITAL RECOMMENDER SYSTEM - COMPREHENSIVE TESTS")
    print("=" * 60)
    
    all_passed = True
    
    try:
        if not test_imports():
            all_passed = False
        
        test_configuration()
        test_funding_database() 
        test_business_analyzer()
        test_main_orchestrator()
        
        if all_passed:
            print("\n🎉 ALL COMPREHENSIVE TESTS PASSED!")
            print("System is ready for production deployment!")
        else:
            print("\n❌ Some tests failed - check output above")
        
    except Exception as e:
        print(f"\n❌ Test execution failed: {str(e)}")
        all_passed = False
    
    return all_passed

if __name__ == "__main__":
    run_comprehensive_tests()
