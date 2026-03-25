import pytest # type: ignore
from app.recommender import RecommenderEngine # type: ignore
from app.schemas import CarbonDataInput # type: ignore

def test_recommendation_logic():
    engine = RecommenderEngine()
    
    # Mock some historical data
    mock_data = [
        {
            "carbon_footprint": 100.0,
            "raw_material_energy": 50.0,
            "manufacturing_energy": 30.0,
            "transport_distance_km": 1000.0
        },
        {
            "carbon_footprint": 20.0,
            "raw_material_energy": 10.0,
            "manufacturing_energy": 5.0,
            "transport_distance_km": 100.0
        }
    ]
    
    recommendations = engine.optimize_sustainability(mock_data)
    
    assert len(recommendations.actions) > 0
    assert recommendations.total_optimization_potential > 0
    assert "Supply Chain" in [a.category for a in recommendations.actions]

def test_action_scoring():
    engine = RecommenderEngine()
    action = engine._generate_supply_chain_action(90.0, 800.0)
    
    assert action.impact_score > 5.0
    assert "Switch to low-carbon logistics" in action.action_description
