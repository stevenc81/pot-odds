# Pot Odds Calculator Backend

A high-performance poker pot odds calculation service built with FastAPI, featuring real-time outs detection and Monte Carlo simulations optimized for multi-core processors.

## Features

- **Real-time Pot Odds Calculation**: Instant calculation of pot odds ratios based on current hand
- **Comprehensive Outs Detection**: Identifies all cards that improve your hand with specific draw types
- **NUTS Detection**: Automatically detects when you have an unbeatable hand
- **High Performance**: Multi-threaded Monte Carlo simulations using Numba JIT compilation
- **RESTful API**: Clean, well-documented API with interactive Swagger UI
- **Draw Type Classification**: Categorizes outs by improvement type (flush, straight, pairs, etc.)

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- uv package manager

### Docker Development (Recommended)

The easiest way to get started:

```bash
# Clone the repository
git clone https://github.com/stevenc81/pot-odds.git
cd pot-odds/backend

# Start the backend service
docker-compose up

# The API will be available at:
# - http://localhost:8000 (API endpoints)
# - http://localhost:8000/docs (Swagger UI)
# - http://localhost:8000/redoc (ReDoc documentation)
```

### Local Development Setup

For local development without Docker:

1. **Install uv package manager:**
```bash
pip install uv
```

2. **Create and activate virtual environment:**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
uv sync
```

4. **Run the development server:**
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Technical Architecture

### Core Components

- **`poker_engine.py`**: Core poker logic with hand evaluation using phevaluator library
- **`pot_odds_calculator.py`**: Optimized Monte Carlo simulations with Numba JIT compilation
- **`outs_detector.py`**: Pattern detection for poker draws (straight, flush, full house, etc.)
- **`main.py`**: FastAPI application with CORS configuration
- **`models.py`**: Pydantic models for request/response validation

### Performance Optimizations

- **Numba JIT Compilation**: Critical simulation code compiled to machine code for 10x+ speedup
- **Multi-threading**: Parallel Monte Carlo simulations across 10 threads by default
- **Efficient Hand Evaluation**: Using phevaluator for lightning-fast 5-card hand evaluation
- **Smart Caching**: Reuses evaluation results where possible

## Environment Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `NUMBA_NUM_THREADS` | Numba parallel threads | `10` |
| `OMP_NUM_THREADS` | OpenMP thread count | `10` |
| `CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:3000", "http://localhost:3001"]` |

### Local Development Environment

Create a `.env` file for local development:
```bash
LOG_LEVEL=DEBUG
NUMBA_NUM_THREADS=10
OMP_NUM_THREADS=10
```

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=. --cov-report=html

# Run specific test categories
uv run pytest tests/test_poker_engine.py  # Engine tests
uv run pytest tests/test_api.py           # API endpoint tests

# Run tests in Docker container
docker exec -it pot-odds-backend pytest
```

## Development Commands

### Working with uv

This project uses `uv` for Python package management:

```bash
# Run Python scripts
uv run python script.py

# Access Python REPL
uv run python


# Add new dependencies
uv add package-name

# Update dependencies
uv sync
```

### Docker Development Commands

```bash
# Build and start services
docker-compose up --build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f backend

# Access container shell
docker exec -it pot-odds-backend /bin/bash


# Stop services
docker-compose down
```

### Code Quality

```bash
# Format code with black
uv run black .

# Sort imports
uv run isort .

# Type checking
uv run mypy .

# Linting
uv run flake8 .
```

## Production Deployment

### Docker Production Deployment

1. **Using pre-built Docker Hub image:**
```bash
docker pull stevenc81/pot-odds-backend:latest
docker run -d \
  -p 8000:8000 \
  -e LOG_LEVEL=INFO \
  --name pot-odds-backend \
  stevenc81/pot-odds-backend:latest
```

2. **Or build your own image:**
```bash
docker build -t pot-odds-backend:latest .
docker run -d \
  -p 8000:8000 \
  -e LOG_LEVEL=INFO \
  --name pot-odds-backend \
  pot-odds-backend:latest
```

### Docker Compose Production

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    image: pot-odds-backend:latest
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=INFO
    restart: unless-stopped
```

### Health Checks and Monitoring

The service provides health endpoints for monitoring:

- `/health` - Overall service health
- `/` - Basic API information and version

Configure your load balancer or monitoring system to use these endpoints.

## API Documentation

### Quick API Example

```bash
# Calculate pot odds for a flush draw
curl -X POST "http://localhost:8000/api/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "hole_cards": ["As", "Ks"],
    "community_cards": ["Qs", "Js", "4h"]
  }'

# Response:
{
  "pot_odds_ratio": "3.9:1",
  "outs": [
    {"card": "Ts", "draw_type": "straight flush"},
    {"card": "2s", "draw_type": "flush"},
    {"card": "3s", "draw_type": "flush"},
    ...
  ]
}
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and version |
| `/health` | GET | Service health check |
| `/api/calculate` | POST | Calculate pot odds and detect outs |

### Special Features

- **NUTS Detection**: When your hand is unbeatable, the API returns `"NUTS!"` as the pot odds ratio
- **Draw Type Classification**: Each out is categorized (flush, straight, pair, two pair, three of a kind, full house, four of a kind, straight flush, royal flush)
- **Simplified Ratios**: Pot odds are displayed in X:1 format, rounded to first decimal

For detailed API specifications, request/response formats, and usage examples, see:
- **[API Specification](./api-spec.md)** - Comprehensive API documentation
- **Interactive Docs**: 
  - Swagger UI: http://localhost:8000/docs
  - ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Common Issues

**Import Errors with phevaluator:**
```bash
# Reinstall with proper compilation
uv pip uninstall phevaluator
uv pip install phevaluator --no-binary :all:
```

**Port Already in Use:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── poker_engine.py         # Core poker hand evaluation logic
├── pot_odds_calculator.py  # Monte Carlo simulation engine
├── outs_detector.py        # Outs detection and classification
├── models.py              # Pydantic models for API
├── api-spec.md            # Comprehensive API documentation
├── tests/                 # Test suite with 100+ tests
│   ├── test_api.py
│   ├── test_poker_engine.py
│   ├── test_pot_odds_calculator.py
│   └── test_outs_detector.py
├── Dockerfile             # Production Docker image
├── docker-compose.yml     # Development environment
└── pyproject.toml         # Project dependencies

```

## Performance Benchmarks

| Scenario | Response Time | Accuracy |
|----------|--------------|----------|
| Simple pot odds (2 cards) | < 50ms | 99.9% |
| Complex hand (7 cards) | < 100ms | 99.9% |
| Monte Carlo (10k iterations) | < 200ms | 98%+ |
| NUTS detection | < 30ms | 100% |

## Contributing

### Development Guidelines

1. **Code Style**: Follow PEP 8, use type hints
2. **Testing**: Write tests for new features, maintain >80% coverage
3. **Documentation**: Update API spec for endpoint changes
4. **Performance**: Benchmark significant changes
5. **Commits**: Use conventional commit format

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass: `uv run pytest`
4. Update documentation if needed
5. Submit PR with clear description

## License

MIT License - See LICENSE file for details