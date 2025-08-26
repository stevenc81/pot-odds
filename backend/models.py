"""Pydantic models for request and response validation."""

from typing import List
from pydantic import BaseModel, Field, field_validator, model_validator
import re

# Card notation regex pattern
CARD_PATTERN = re.compile(r'^[2-9TJQKA][shdc]$')


class CalculateRequest(BaseModel):
    """Request model for pot odds calculation."""
    
    hole_cards: List[str] = Field(
        ..., 
        min_length=2, 
        max_length=2,
        description="Player's two hole cards in format like 'As', 'Kh'"
    )
    community_cards: List[str] = Field(
        default_factory=list,
        min_length=0,
        max_length=5,
        description="Community cards on the board (0-5 cards)"
    )
    
    @field_validator('hole_cards', 'community_cards')
    @classmethod
    def validate_cards(cls, cards):
        """Validate card notation and check for duplicates."""
        if not cards:
            return cards
            
        # Validate card notation
        for card in cards:
            if not CARD_PATTERN.match(card):
                raise ValueError(f"Invalid card notation: {card}. Use format like 'As', 'Kh', '7d'")
        
        # Check for duplicates
        if len(cards) != len(set(cards)):
            raise ValueError("Duplicate cards are not allowed")
        
        return cards
    
    @model_validator(mode='after')
    def validate_no_duplicate_across_all_cards(self):
        """Ensure no duplicates across hole cards and community cards."""
        all_cards = self.hole_cards + self.community_cards
        if len(all_cards) != len(set(all_cards)):
            raise ValueError("Duplicate cards found across hole cards and community cards")
        return self


class OutCard(BaseModel):
    """Model for an out card with its draw type."""
    
    card: str = Field(
        ...,
        description="Card notation (e.g., 'As', 'Kh')"
    )
    draw_type: str = Field(
        ...,
        description="Type of draw this card completes"
    )
    
    @field_validator('card')
    @classmethod
    def validate_card_notation(cls, card):
        """Validate card notation."""
        if not CARD_PATTERN.match(card):
            raise ValueError(f"Invalid card notation: {card}")
        return card


class CalculationResponse(BaseModel):
    """Response model for pot odds calculation."""
    
    pot_odds_ratio: str = Field(
        ...,
        description="Pot odds ratio in X.X:1 format, rounded to first decimal"
    )
    outs: List[OutCard] = Field(
        ...,
        description="List of cards that improve the hand with their draw types"
    )


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(default="healthy", description="API health status")
    version: str = Field(default="0.1.0", description="API version")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    detail: str = Field(..., description="Error message")