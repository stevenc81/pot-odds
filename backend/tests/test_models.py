"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError
from models import (
    CalculateRequest,
    CalculationResponse, 
    HealthResponse,
    OutCard,
    ErrorResponse
)


class TestCalculateRequest:
    """Test CalculateRequest model validation."""
    
    def test_valid_request(self):
        """Test valid request creation."""
        request = CalculateRequest(
            hole_cards=["As", "Kh"],
            community_cards=["Qs", "Jd", "Tc"]
        )
        
        assert request.hole_cards == ["As", "Kh"]
        assert request.community_cards == ["Qs", "Jd", "Tc"]
    
    def test_valid_request_no_community_cards(self):
        """Test valid request with no community cards."""
        request = CalculateRequest(hole_cards=["As", "Kh"])
        
        assert request.hole_cards == ["As", "Kh"]
        assert request.community_cards == []
    
    def test_valid_card_notations(self):
        """Test various valid card notations."""
        valid_cards = [
            ["As", "2h"],     # Ace and deuce
            ["Kd", "Qc"],     # King and queen  
            ["Js", "Th"],     # Jack and ten
            ["9s", "8h"],     # Numbers
            ["7d", "6c"],     # More numbers
            ["5s", "4h"],     # More numbers
            ["3d", "2c"],     # Low cards
        ]
        
        for cards in valid_cards:
            request = CalculateRequest(hole_cards=cards)
            assert request.hole_cards == cards
    
    def test_invalid_hole_cards_count(self):
        """Test invalid hole cards count."""
        # Too few
        with pytest.raises(ValidationError):
            CalculateRequest(hole_cards=["As"])
        
        # Too many
        with pytest.raises(ValidationError):
            CalculateRequest(hole_cards=["As", "Kh", "Qd"])
    
    def test_invalid_community_cards_count(self):
        """Test invalid community cards count."""
        # Too many (max 5)
        with pytest.raises(ValidationError):
            CalculateRequest(
                hole_cards=["As", "Kh"],
                community_cards=["Qs", "Jd", "Tc", "9h", "8s", "7c"]
            )
    
    def test_invalid_card_notation_rank(self):
        """Test invalid card notation - bad rank."""
        with pytest.raises(ValidationError, match="Invalid card notation"):
            CalculateRequest(hole_cards=["Xs", "Kh"])
        
        with pytest.raises(ValidationError, match="Invalid card notation"):
            CalculateRequest(hole_cards=["1s", "Kh"])  # 1 is not valid rank
    
    def test_invalid_card_notation_suit(self):
        """Test invalid card notation - bad suit."""
        with pytest.raises(ValidationError, match="Invalid card notation"):
            CalculateRequest(hole_cards=["Ax", "Kh"])  # x is not valid suit
        
        with pytest.raises(ValidationError, match="Invalid card notation"):
            CalculateRequest(hole_cards=["Az", "Kh"])  # z is not valid suit
    
    def test_invalid_card_notation_length(self):
        """Test invalid card notation - wrong length."""
        with pytest.raises(ValidationError, match="Invalid card notation"):
            CalculateRequest(hole_cards=["A", "Kh"])  # Too short
        
        with pytest.raises(ValidationError, match="Invalid card notation"):
            CalculateRequest(hole_cards=["Ass", "Kh"])  # Too long
    
    def test_duplicate_hole_cards(self):
        """Test duplicate cards in hole cards."""
        with pytest.raises(ValidationError, match="Duplicate cards are not allowed"):
            CalculateRequest(hole_cards=["As", "As"])
    
    def test_duplicate_community_cards(self):
        """Test duplicate cards in community cards."""
        with pytest.raises(ValidationError, match="Duplicate cards are not allowed"):
            CalculateRequest(
                hole_cards=["As", "Kh"],
                community_cards=["Qs", "Qs", "Tc"]
            )
    
    def test_duplicate_across_hole_and_community(self):
        """Test duplicate cards across hole and community cards."""
        with pytest.raises(ValidationError, match="Duplicate cards found"):
            CalculateRequest(
                hole_cards=["As", "Kh"],
                community_cards=["As", "Jd", "Tc"]  # As appears in both
            )


class TestOutCard:
    """Test OutCard model validation."""
    
    def test_valid_out_card(self):
        """Test valid out card creation."""
        out = OutCard(card="As", draw_type="flush")
        
        assert out.card == "As"
        assert out.draw_type == "flush"
    
    def test_valid_draw_types(self):
        """Test various valid draw types."""
        draw_types = [
            "flush", "straight", "pair", "two_pair",
            "three_of_a_kind", "full_house", "four_of_a_kind",
            "straight_flush", "royal_flush"
        ]
        
        for draw_type in draw_types:
            out = OutCard(card="As", draw_type=draw_type)
            assert out.draw_type == draw_type
    
    def test_invalid_card_notation(self):
        """Test invalid card notation in out card."""
        with pytest.raises(ValidationError, match="Invalid card notation"):
            OutCard(card="Xs", draw_type="flush")


class TestCalculationResponse:
    """Test CalculationResponse model validation."""
    
    def test_valid_response(self):
        """Test valid response creation."""
        outs = [
            OutCard(card="As", draw_type="flush"),
            OutCard(card="Kh", draw_type="pair")
        ]
        
        response = CalculationResponse(
            pot_odds_ratio="3.1:1",
            outs=outs
        )
        
        assert response.pot_odds_ratio == "3.1:1"
        assert len(response.outs) == 2
        assert response.outs[0].card == "As"
    
    def test_empty_outs(self):
        """Test response with no outs."""
        response = CalculationResponse(
            pot_odds_ratio="999.0:1",
            outs=[]
        )
        
        assert response.pot_odds_ratio == "999.0:1"
        assert len(response.outs) == 0
    
    def test_various_pot_odds_ratios(self):
        """Test various pot odds ratio formats."""
        ratios = ["1.9:1", "3.1:1", "5.1:1", "4:1", "0.85:1", "999.0:1"]
        
        for ratio in ratios:
            response = CalculationResponse(pot_odds_ratio=ratio, outs=[])
            assert response.pot_odds_ratio == ratio


class TestHealthResponse:
    """Test HealthResponse model validation."""
    
    def test_default_health_response(self):
        """Test default health response."""
        response = HealthResponse()
        
        assert response.status == "healthy"
        assert response.version == "0.1.0"
    
    def test_custom_health_response(self):
        """Test custom health response."""
        response = HealthResponse(status="unhealthy", version="0.2.0")
        
        assert response.status == "unhealthy"
        assert response.version == "0.2.0"


class TestErrorResponse:
    """Test ErrorResponse model validation."""
    
    def test_error_response(self):
        """Test error response creation."""
        response = ErrorResponse(detail="Test error message")
        
        assert response.detail == "Test error message"


class TestModelIntegration:
    """Test model integration scenarios."""
    
    def test_full_request_response_cycle(self):
        """Test complete request-response cycle with models."""
        # Create request
        request = CalculateRequest(
            hole_cards=["As", "Kh"],
            community_cards=["Qs", "Jd", "Tc"]
        )
        
        # Create response
        outs = [
            OutCard(card="9s", draw_type="straight"),
            OutCard(card="9h", draw_type="straight"),
        ]
        
        response = CalculationResponse(
            pot_odds_ratio="3.0:1",
            outs=outs
        )
        
        # Validate both models work together
        assert len(request.hole_cards) == 2
        assert len(request.community_cards) == 3
        assert response.pot_odds_ratio == "3.0:1"
        assert len(response.outs) == 2
    
    def test_json_serialization(self):
        """Test JSON serialization of models."""
        request = CalculateRequest(
            hole_cards=["As", "Kh"],
            community_cards=["Qs"]
        )
        
        # Should be able to convert to dict/JSON
        request_dict = request.model_dump()
        assert request_dict["hole_cards"] == ["As", "Kh"]
        assert request_dict["community_cards"] == ["Qs"]
        
        # Should be able to create from dict
        request2 = CalculateRequest(**request_dict)
        assert request2.hole_cards == request.hole_cards
        assert request2.community_cards == request.community_cards