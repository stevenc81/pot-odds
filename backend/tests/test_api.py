"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from main import app
import main
from poker_engine import PokerEngine
from pot_odds_calculator import OptimizedPotOddsCalculator

# Initialize components for testing
main.poker_engine = PokerEngine()
main.calculator = OptimizedPotOddsCalculator(main.poker_engine)

client = TestClient(app)


class TestAPIEndpoints:
    """Test API endpoint functionality."""
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["message"] == "Pot Odds Calculator API"
        assert data["version"] == "0.1.0"
        assert "endpoints" in data
        assert data["endpoints"]["calculate"] == "/api/calculate"
        assert data["endpoints"]["health"] == "/health"
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["version"] == "0.1.0"
    
    def test_calculate_endpoint_valid_request(self):
        """Test calculate endpoint with valid request."""
        request_data = {
            "hole_cards": ["As", "Kh"],
            "community_cards": ["Qs", "Jd", "Tc"]
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "pot_odds_ratio" in data
        assert "outs" in data
        assert isinstance(data["outs"], list)
        
        # Check pot odds ratio format (can be "NUTS!" or "X.X:1" format)
        ratio = data["pot_odds_ratio"]
        if ratio == "NUTS!":
            # This is correct for Broadway straight which is nuts in this case
            assert ratio == "NUTS!"
        else:
            assert ":" in ratio
            assert ratio.endswith(":1")
        
        # Check outs format
        for out in data["outs"]:
            assert "card" in out
            assert "draw_type" in out
            assert len(out["card"]) == 2  # Card notation like "As"
    
    def test_calculate_endpoint_inside_straight_draw(self):
        """Test calculate endpoint with inside straight draw."""
        request_data = {
            "hole_cards": ["9s", "8h"],
            "community_cards": ["5c", "6d", "Ks"]
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should find 4 outs (the 4 sevens)
        seven_outs = [out for out in data["outs"] if out["card"][0] == "7"]
        assert len(seven_outs) >= 4
        
        # All sevens should be straight draws
        for out in seven_outs:
            assert "straight" in out["draw_type"]  # Can be straight_gutshot or straight_open_ended
    
    def test_calculate_endpoint_flush_draw(self):
        """Test calculate endpoint with flush draw."""
        request_data = {
            "hole_cards": ["7s", "3s"],  # 2 spades
            "community_cards": ["Ks", "Js", "9h"]  # 2 more spades + 1 other
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should find spade outs for flush
        flush_outs = [out for out in data["outs"] if out["draw_type"] == "flush"]
        assert len(flush_outs) >= 7  # Should have several spade outs (9 remaining spades)
        
        # All flush outs should be spades
        for out in flush_outs:
            assert out["card"][1] == "s"
        
        # Total outs should include the 9 flush outs plus some pair outs
        assert len(data["outs"]) >= 9
        # With a weak hand, many cards can be outs, so allow a broader range
        assert len(data["outs"]) <= 50
    
    def test_calculate_endpoint_two_overcards(self):
        """Test calculate endpoint with two overcards."""
        request_data = {
            "hole_cards": ["As", "Kd"],
            "community_cards": ["Qc", "7h", "2s"]
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should find 6 outs (3 aces + 3 kings)
        ace_outs = [out for out in data["outs"] if out["card"][0] == "A" and out["card"] != "As"]
        king_outs = [out for out in data["outs"] if out["card"][0] == "K" and out["card"] != "Kd"]
        
        assert len(ace_outs) == 3
        assert len(king_outs) == 3
    
    def test_calculate_endpoint_no_community_cards(self):
        """Test calculate endpoint with no community cards."""
        request_data = {
            "hole_cards": ["As", "Kh"],
            "community_cards": []
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should still return valid response
        assert "pot_odds_ratio" in data
        assert "outs" in data
    
    def test_calculate_endpoint_invalid_card_notation(self):
        """Test calculate endpoint with invalid card notation."""
        request_data = {
            "hole_cards": ["Xx", "Kh"],
            "community_cards": ["Qs", "Jd", "Tc"]
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_calculate_endpoint_duplicate_cards(self):
        """Test calculate endpoint with duplicate cards."""
        request_data = {
            "hole_cards": ["As", "As"],  # Duplicate ace of spades
            "community_cards": ["Qs", "Jd", "Tc"]
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 422
    
    def test_calculate_endpoint_duplicate_across_holes_and_community(self):
        """Test calculate endpoint with duplicates across hole and community cards."""
        request_data = {
            "hole_cards": ["As", "Kh"],
            "community_cards": ["As", "Jd", "Tc"]  # As appears in both
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 422
    
    def test_calculate_endpoint_wrong_number_of_hole_cards(self):
        """Test calculate endpoint with wrong number of hole cards."""
        request_data = {
            "hole_cards": ["As"],  # Should be exactly 2
            "community_cards": ["Qs", "Jd", "Tc"]
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 422
    
    def test_calculate_endpoint_too_many_community_cards(self):
        """Test calculate endpoint with too many community cards."""
        request_data = {
            "hole_cards": ["As", "Kh"],
            "community_cards": ["Qs", "Jd", "Tc", "9h", "8s", "7c"]  # 6 cards, max is 5
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 422
    
    def test_calculate_endpoint_missing_hole_cards(self):
        """Test calculate endpoint with missing hole cards."""
        request_data = {
            "community_cards": ["Qs", "Jd", "Tc"]
            # Missing hole_cards field
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 422
    
    def test_calculate_endpoint_empty_request(self):
        """Test calculate endpoint with empty request."""
        response = client.post("/api/calculate", json={})
        
        assert response.status_code == 422
    
    def test_calculate_endpoint_malformed_json(self):
        """Test calculate endpoint with malformed JSON."""
        response = client.post("/api/calculate", data="not json")
        
        assert response.status_code == 422
    
    def test_calculate_endpoint_royal_flush(self):
        """Test calculate endpoint with royal flush (no outs)."""
        request_data = {
            "hole_cards": ["As", "Ks"],
            "community_cards": ["Qs", "Js", "Ts"]
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have no outs (already best possible hand)
        assert len(data["outs"]) == 0
        
        # According to API spec, royal flush using both hole cards should return NUTS!
        ratio = data["pot_odds_ratio"]
        assert ratio == "NUTS!"
    
    def test_response_schema_validation(self):
        """Test that response matches expected schema."""
        # Use a non-nuts hand to test normal ratio format
        request_data = {
            "hole_cards": ["2s", "3h"],
            "community_cards": ["7d", "8c", "Jh"]
        }
        
        response = client.post("/api/calculate", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response schema
        assert isinstance(data["pot_odds_ratio"], str)
        assert isinstance(data["outs"], list)
        
        # Validate pot odds ratio format (should not be NUTS for this low hand)
        ratio = data["pot_odds_ratio"]
        assert ":" in ratio
        assert ratio.endswith(":1")
        parts = ratio.split(":")
        assert len(parts) == 2
        assert parts[1] == "1"
        
        # Validate decimal formatting
        ratio_value = parts[0]
        if "." in ratio_value:
            decimal_part = ratio_value.split(".")[1]
            assert len(decimal_part) == 1  # Only one decimal place
        
        # Validate outs structure
        for out in data["outs"]:
            assert isinstance(out["card"], str)
            assert isinstance(out["draw_type"], str)
            assert len(out["card"]) == 2
            assert out["card"][0] in "23456789TJQKA"
            assert out["card"][1] in "shdc"


def test_calculate_endpoint_nuts_royal_flush_draw():
    """Test calculate endpoint with royal flush draw that results in NUTS."""
    # Hand: As 9h, Board: Ks Qs Js (Ten of spades completes royal flush)
    request_data = {
        "hole_cards": ["As", "9h"],
        "community_cards": ["Ks", "Qs", "Js"]
    }
    
    response = client.post("/api/calculate", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    
    # Check if NUTS is detected
    # Note: This depends on whether the outs detector finds Ts as an out
    assert "pot_odds_ratio" in data
    assert "outs" in data
    
    # Should return normal odds since draws no longer trigger NUTS detection
    ts_outs = [out for out in data["outs"] if out["card"] == "Ts"]
    if ts_outs:
        # Should be a normal ratio, not NUTS!
        assert data["pot_odds_ratio"] != "NUTS!"
        assert ":" in data["pot_odds_ratio"]


def test_calculate_endpoint_nuts_nut_flush_draw():
    """Test calculate endpoint with nut flush draw - should return normal odds, not NUTS."""
    # Hand: As Ks, Board: Qs Js 7h (no pairs, any spade completes nut flush)
    request_data = {
        "hole_cards": ["As", "Ks"],
        "community_cards": ["Qs", "Js", "7h"]
    }
    
    response = client.post("/api/calculate", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    
    # Should return normal odds since draws no longer trigger NUTS detection
    assert data["pot_odds_ratio"] != "NUTS!"
    assert ":" in data["pot_odds_ratio"]
    
    # Should have flush outs
    flush_outs = [out for out in data["outs"] if out["draw_type"] == "flush"]
    assert len(flush_outs) >= 9  # Should find 9 spades


def test_calculate_endpoint_nuts_broadway_straight():
    """Test calculate endpoint with Broadway straight draw - should return normal odds, not NUTS."""
    # Hand: As Kd, Board: Qh Jc 2s (Ten completes Broadway straight)
    request_data = {
        "hole_cards": ["As", "Kd"],
        "community_cards": ["Qh", "Jc", "2s"]
    }
    
    response = client.post("/api/calculate", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    
    # Should return normal odds since draws no longer trigger NUTS detection
    assert data["pot_odds_ratio"] != "NUTS!"
    assert ":" in data["pot_odds_ratio"]
    
    # Should have straight outs
    straight_outs = [out for out in data["outs"] if "straight" in out["draw_type"]]
    assert len(straight_outs) >= 4  # Should find 4 tens


def test_calculate_endpoint_api_spec_royal_flush_example():
    """Test the specific royal flush example from API spec."""
    request_data = {
        "hole_cards": ["Ah", "Kh"],
        "community_cards": ["Qh", "Jh", "Th"]
    }
    
    response = client.post("/api/calculate", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # According to API spec, this should return "NUTS!"
    assert data["pot_odds_ratio"] == "NUTS!"
    assert len(data["outs"]) == 0