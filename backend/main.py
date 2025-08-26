"""Main FastAPI application for Pot Odds Calculator."""

import os
import logging
import json
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from models import (
    CalculateRequest, 
    CalculationResponse, 
    HealthResponse,
    OutCard,
    ErrorResponse
)
from poker_engine import PokerEngine
from pot_odds_calculator import OptimizedPotOddsCalculator

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global instances
poker_engine = None
calculator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    global poker_engine, calculator
    
    logger.info("Starting Pot Odds Calculator API...")
    
    # Initialize components
    poker_engine = PokerEngine()
    calculator = OptimizedPotOddsCalculator(poker_engine)
    
    logger.info("Application startup complete")
    
    yield
    
    logger.info("Application shutdown")


# Create FastAPI app
app = FastAPI(
    title="Pot Odds Calculator API",
    description="High-performance poker pot odds calculation service",
    version="0.1.0",
    lifespan=lifespan
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://localhost:3001"]')
try:
    origins = json.loads(cors_origins)
except json.JSONDecodeError:
    origins = ["http://localhost:3000", "http://localhost:3001"]
    logger.warning(f"Invalid CORS_ORIGINS format, using default: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors."""
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle value errors (e.g., invalid card notation)."""
    logger.warning(f"Value error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred during calculation"}
    )


# API Endpoints
@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Pot Odds Calculator API",
        "version": "0.1.0",
        "endpoints": {
            "calculate": "/api/calculate",
            "health": "/health"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="0.1.0")


@app.get("/api/", response_model=dict)
async def api_info():
    """API information endpoint - shows available API endpoints."""
    return {
        "message": "Pot Odds Calculator API endpoints",
        "version": "0.1.0",
        "endpoints": {
            "calculate_pot_odds": {
                "path": "/api/calculate",
                "method": "POST",
                "description": "Calculate pot odds and identify outs for a poker hand",
                "example_request": {
                    "hole_cards": ["Ah", "Kh"],
                    "community_cards": ["Qh", "Jh", "Ts"]
                }
            }
        },
        "hint": "Did you mean to POST to /api/calculate instead?"
    }


@app.post("/api/", response_model=dict)
async def api_post_redirect():
    """Handle POST requests to /api/ with helpful error message."""
    raise HTTPException(
        status_code=404, 
        detail={
            "error": "No POST endpoint at /api/",
            "hint": "Did you mean to POST to /api/calculate?",
            "correct_endpoint": "/api/calculate",
            "required_fields": ["hole_cards", "community_cards"],
            "example_request": {
                "hole_cards": ["Ah", "Kh"],
                "community_cards": ["Qh", "Jh", "Ts"]
            }
        }
    )


@app.post("/api/calculate", response_model=CalculationResponse)
async def calculate_pot_odds(request: CalculateRequest):
    """
    Calculate pot odds and identify outs for a poker hand.
    
    This endpoint analyzes a poker hand (hole cards + community cards) and:
    1. Identifies all "outs" (cards that improve the hand)
    2. Classifies each out by draw type (flush, straight, pair, etc.)
    3. Calculates precise pot odds ratio based on probability
    
    The pot odds ratio follows the format X.X:1, rounded to first decimal.
    If the decimal is .0, it's shown as integer (e.g., 4:1 instead of 4.0:1).
    """
    try:
        logger.info(f"Calculating pot odds for hole_cards={request.hole_cards}, "
                   f"community_cards={request.community_cards}")
        
        # Parse cards
        hole_cards = poker_engine.parse_cards(request.hole_cards)
        community_cards = poker_engine.parse_cards(request.community_cards)
        
        # Validate hand (no duplicates across all cards)
        all_card_strs = request.hole_cards + request.community_cards
        if len(all_card_strs) != len(set(all_card_strs)):
            raise ValueError("Duplicate cards found")
        
        # Calculate pot odds and outs
        pot_odds_ratio, outs_data = calculator.calculate_pot_odds(hole_cards, community_cards)
        
        # Convert to response format
        outs = [OutCard(card=out['card'], draw_type=out['draw_type']) for out in outs_data]
        
        response = CalculationResponse(
            pot_odds_ratio=pot_odds_ratio,
            outs=outs
        )
        
        logger.info(f"Calculation complete: {len(outs)} outs, ratio={pot_odds_ratio}")
        
        return response
        
    except ValueError as e:
        logger.warning(f"Invalid request: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    
    except Exception as e:
        logger.error(f"Calculation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error during pot odds calculation")


# Development and debugging endpoints (only in debug mode)
@app.get("/api/debug/examples")
async def debug_examples():
    """Debug endpoint to show calculation examples."""
    if os.getenv("LOG_LEVEL") != "DEBUG":
        raise HTTPException(status_code=404, detail="Not found")
    
    examples = calculator.calculate_exact_odds_from_examples()
    return examples


@app.get("/api/debug/probability/{hole_cards}/{community_cards}")
async def debug_probability_breakdown(hole_cards: str, community_cards: str = ""):
    """Debug endpoint for probability breakdown."""
    if os.getenv("LOG_LEVEL") != "DEBUG":
        raise HTTPException(status_code=404, detail="Not found")
    
    try:
        hole_list = hole_cards.split(",")
        community_list = community_cards.split(",") if community_cards else []
        
        hole_card_objects = poker_engine.parse_cards(hole_list)
        community_card_objects = poker_engine.parse_cards(community_list)
        
        breakdown = calculator.get_probability_breakdown(hole_card_objects, community_card_objects)
        return breakdown
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=log_level == "debug"
    )