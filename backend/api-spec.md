## API Overview

The Pot Odds Calculator API is a high-performance REST API for poker analytics, focused on calculating pot odds and identifying "outs" with their specific draw types. The API is built with FastAPI for real-time response and is designed for sub-second analytics.

### Base URL

```
http://localhost:8000
```
*Production URL will depend on deployment.*

### API Version

Current version: `0.1.0`

---

## Authentication

The API does **not** require authentication. All endpoints are publicly accessible.

---

## Rate Limiting

Rate limiting is **not** enforced in the current implementation.

---

## CORS Configuration

- **Allowed Origins**: `http://localhost:3000`, `http://localhost:3001`
- **Allowed Methods**: All (`*`)
- **Allowed Headers**: All (`*`)
- **Allow Credentials**: `true`

---

## Endpoints

### 1. Root Endpoint

#### GET /

Returns basic API information and available endpoints.

**Response:**
```json
{
  "message": "Pot Odds Calculator API",
  "version": "0.1.0",
  "endpoints": {
    "calculate": "/api/calculate",
    "health": "/health"
  }
}
```

**Status Codes:** `200 OK`

---

### 2. Health Check

#### GET /health

Provides API version and status.

**Response Model:** `HealthResponse`

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

| Field             | Type    | Description                                            |
|-------------------|---------|--------------------------------------------------------|
| status            | string  | API health status ("healthy")                          |
| version           | string  | API version                                            |

**Status Codes:** `200 OK`

---

### 3. Calculate Pot Odds

#### POST /api/calculate

Calculates pot odds and identifies outs with their draw types for a given poker hand.

**Primary Purpose:**  
Calculates the risk-reward ratio (pot odds) based on poker outs, allowing players to make mathematically sound decisions. Results include a single pot odds ratio and outs categorized by draw type.

---

#### Calculation Algorithm

- Your hole cards and any community cards are analyzed.
- The algorithm identifies all possible outs that improve your hand.
- Each out is categorized by the type of draw it represents (flush, straight, pair, etc.).
- Pot odds are calculated based on the probability of hitting these outs.
- The pot odds ratio is simplified to be based on 1 and rounded to the first decimal point (e.g., "5.1:1" instead of "8353:1646"). If the decimal is .0, it's rounded up to the integer (e.g., "4:1" instead of "4.0:1").
- Special case: The API returns `"NUTS!"` for `pot_odds_ratio` when the player's current best 5-card hand (using their hole cards and community cards) cannot be beaten by any other possible 5-card hand given the current board.
  - The player's hand must be complete and unbeatable (the "nuts")
  - At least one hole card must be part of the best 5-card hand
  - Board-only hands (where hole cards are not used) do not qualify
  - This applies to completed hands at any stage (flop, turn, or river)
  - Tied hands (where other players could have the same best hand) still qualify as "NUTS!"
  - Note: "Completes" refers to the player's current hand being complete and unbeatable, not about completing a draw or improving their hand

**Pot Odds Calculation:**
- Pot odds ratio formula:  
  \[
    \text{Pot Odds Ratio} = \frac{\text{Chance of losing}}{\text{Chance of winning}}
  \]
- The ratio is always simplified to be based on 1 and rounded to the first decimal point
- If the decimal is .0, it's rounded up to the integer (e.g., 4.0:1 becomes 4:1)
- If win probability is 20%:  
  80:20 = 4:1
- If win probability is 16.47%:  
  8353:1646 ≈ 5.1:1

---

#### Request Model: `CalculateRequest`

**Request Body:**
```json
{
  "hole_cards": ["As", "Kh"],
  "community_cards": ["Qs", "Jd", "Tc"]
}
```

| Field            | Type            | Required | Constraints           | Description                |
|------------------|-----------------|----------|-----------------------|----------------------------|
| hole_cards       | array[string]   | Yes      | Length: exactly 2     | Player's hole cards        |
| community_cards  | array[string]   | No       | Length: 0-5           | Community cards on board   |

---

#### Response Model: `CalculationResponse`

**Response:**
```json
{
  "pot_odds_ratio": "3.0:1",
  "outs": [
    {
      "card": "9s",
      "draw_type": "straight"
    },
    {
      "card": "Ah",
      "draw_type": "pair"
    },
    {
      "card": "Kd",
      "draw_type": "pair"
    }
  ]
}
```

**Example 1b - Nuts Completion (Special Case):**
```json
{
  "pot_odds_ratio": "NUTS!",
  "outs": [
    {
      "card": "9s",
      "draw_type": "straight_flush"
    }
  ]
}
```

| Field           | Type               | Description                       |
|-----------------|--------------------|-----------------------------------|
| pot_odds_ratio  | string             | Calculated pot odds ratio (simplified to X.X:1 format, rounded to first decimal; .0 decimals become integers). May be `"NUTS!"` when the player's current best 5-card hand (using at least one hole card) cannot be beaten by any other possible 5-card hand given the current board. |
| outs            | array[OutCard]     | List of cards that improve hand   |

**OutCard Object:**
| Field      | Type    | Description                        |
|------------|---------|------------------------------------|
| card       | string  | Card notation (e.g., "As", "Kh")   |
| draw_type  | string  | Type of draw (flush, straight, pair, full_house, etc.) |

**Draw Types:**
- `flush` - Completes a flush
- `straight` - Completes a straight
- `pair` - Makes a pair
- `two_pair` - Makes two pair
- `three_of_a_kind` - Makes three of a kind
- `full_house` - Makes a full house
- `four_of_a_kind` - Makes four of a kind
- `straight_flush` - Makes a straight flush
- `royal_flush` - Makes a royal flush

**Status Codes:**  
- `200 OK`: Calculation successful  
- `422 Unprocessable Entity`: Validation error  
- `500 Internal Server Error`: Calculation error

---

#### Validation Rules

1. All cards must use valid notation (`^[2-9TJQKA][shdc]$`)
2. No duplicates across hole_cards and community_cards
3. Respect array length constraints

**Error Response (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "hole_cards", 0],
      "msg": "Invalid card notation: XX. Use format like 'As', 'Kh', '7d'",
      "type": "value_error"
    }
  ]
}
```

---

## Data Models

### Card Notation Format

- Two-character string: Rank then Suit
- Valid ranks: `2-9`, `T`, `J`, `Q`, `K`, `A`
- Valid suits: `s` (Spades), `h` (Hearts), `d` (Diamonds), `c` (Clubs)
- Example: `"As"` (Ace of Spades)

---

## Error Handling

All errors use FastAPI's error format:
```json
{
  "detail": "Error message or validation details"
}
```
Common errors: invalid card, duplicates, invalid length, calculation failures.

---

## Example Requests

#### cURL

```bash
curl -X POST "http://localhost:8000/api/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "hole_cards": ["As", "Kh"],
    "community_cards": ["Qs", "Jd", "Tc"]
  }'
```

#### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/calculate",
    json={
        "hole_cards": ["As", "Kh"],
        "community_cards": ["Qs", "Jd", "Tc"]
    }
)
if response.status_code == 200:
    result = response.json()
    print(f"Pot Odds Ratio: {result['pot_odds_ratio']}")
    print(f"Outs: {[(out['card'], out['draw_type']) for out in result['outs']]}")
else:
    print(f"Error: {response.json()['detail']}")
```

#### JavaScript

```javascript
const calculatePotOdds = async () => {
  const response = await fetch('http://localhost:8000/api/calculate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      hole_cards: ['As', 'Kh'],
      community_cards: ['Qs', 'Jd', 'Tc']
    })
  });
  if (response.ok) {
    const data = await response.json();
    console.log('Pot Odds:', data.pot_odds_ratio);
    console.log('Outs:', data.outs);
  } else {
    const error = await response.json();
    console.error('Error:', error.detail);
  }
};
```

---

## Performance Characteristics

### Response Times

The API is designed for sub-second response times:
- **Typical Response Time**: <100ms
- **Complex Hand Analysis**: <500ms

### Optimization Features

1. **Fast Hand Evaluation**: Optimized algorithms for hand strength calculation
2. **Efficient Outs Detection**: Quick identification of improving cards
3. **Draw Type Classification**: Fast categorization of draw types

---

## WebSocket/Streaming Endpoints

The current API version does not include WebSocket or streaming endpoints. All calculations are performed via synchronous REST endpoints.

---

## API Documentation

Interactive API documentation is available via FastAPI's built-in tools:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces provide:
- Interactive endpoint testing
- Request/response schema details
- Model definitions
- Try-it-out functionality

---

## Monitoring and Observability

### Logging

The API uses Python's standard logging with the following configuration:
- **Default Level**: INFO
- **Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Errors**: Logged at ERROR level with full stack traces

### Health Monitoring

The `/health` endpoint provides:
- API health status
- API version information

This endpoint can be used for:
- Load balancer health checks
- Monitoring system integration
- Deployment verification

---

## Version History

- **v0.1.0** (Current) - Initial release with REST API endpoints for pot odds calculation
