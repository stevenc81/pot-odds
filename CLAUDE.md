# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A full-stack poker pot odds calculator with real-time outs detection and Monte Carlo simulations. The application consists of:
- **Backend**: FastAPI service with high-performance poker engine using Numba optimization
- **Frontend**: React + TypeScript SPA with responsive design and real-time calculations

## Common Development Commands

### Backend (Python/FastAPI)
```bash
# Navigate to backend
cd backend/

# Run development server
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_outs_detector.py

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Format code
uv run black .
uv run isort .

# Type checking
uv run mypy .

# Linting
uv run flake8 .

# Add dependencies
uv add package-name

# Update dependencies
uv sync
```

### Frontend (React/TypeScript)
```bash
# Navigate to frontend
cd frontend/

# Run development server
npm run dev

# Build for production
npm run build

# Run type checking
npm run type-check

# Run linting
npm run lint
npm run lint:fix

# Install dependencies
npm install
```

### Docker Commands
```bash
# Backend
cd backend && docker-compose up

# Frontend
cd frontend && docker-compose up --build

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Architecture & Key Components

### Backend Architecture
- **main.py**: FastAPI application entry point with CORS configuration
- **poker_engine.py**: Core poker logic with hand evaluation using phevaluator library
- **pot_odds_calculator.py**: Pot odds calculation with NUTS detection
- **outs_detector.py**: Detects all draw types including royal flush, straight flush, flush, straight, pairs, etc.
- **models.py**: Pydantic models for request/response validation

Key technical decisions:
- Card representation: 2-letter strings (e.g., "Ah" for Ace of hearts)
- NUTS detection when current hand is unbeatable (requires at least one hole card)
- Draw types use spaces not underscores (e.g., "royal flush" not "royal_flush")

### Frontend Architecture
- **State Management**: Zustand stores for card selection and theme
- **API Integration**: React Query for server state with debouncing (150ms)
- **Component Structure**:
  - `components/ui/`: Reusable UI primitives
  - `components/card-selection/`: Card grid and selection logic
  - `components/results/`: Outs display and pot odds visualization
  - `components/layout/`: Page structure and responsive grid
- **Hooks**: Custom hooks for debouncing, API calls, and theme management

Key technical patterns:
- Touch-friendly card selection with visual feedback
- Responsive grid layout adapting to screen size
- Error boundaries for graceful error handling
- Accessibility features with ARIA labels and keyboard navigation

### API Endpoints
- `GET /`: API info and version
- `GET /health`: Service health check
- `POST /api/calculate`: Calculate pot odds and detect outs
  - Request: hole_cards (list of 2), community_cards (list of 0-5)
  - Response: pot_odds_ratio (string like "3.1:1" or "NUTS!"), outs (list with card and draw_type)

## Performance Considerations
- Pot odds calculated using mathematical formulas (not Monte Carlo)
- Frontend implements 150ms debouncing for API calls
- Hand evaluation using fast phevaluator library
- React Query caching reduces redundant API calls

## Testing Strategy
- Backend: Comprehensive pytest suite with 110+ tests
- Test files mirror source files (test_poker_engine.py, test_outs_detector.py, etc.)
- Coverage maintained above 80%
- Run tests with: `uv run pytest`