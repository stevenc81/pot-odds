# Poker for LLMs: Core Rules & Decision Logic

## Game Overview
**Objective**: Make the best 5-card hand using 2 private cards + 5 community cards
**Players**: 2-9 players per hand
**Deck**: Standard 52-card deck
**Goal**: Win chips by having the best hand or making others fold

## Hand Structure (4 Phases)

### Phase 1: Preflop
- **Input**: Each player gets 2 private cards
- **Action**: Bet, call, raise, or fold (starting left of big blind)
- **State**: No community cards visible
- **Decision Logic**: Evaluate hand strength based on hole cards only

### Phase 2: Flop  
- **Input**: 3 community cards dealt face-up
- **Action**: Bet, check, call, raise, or fold
- **State**: 5 total cards visible (2 private + 3 community)
- **Decision Logic**: Calculate best 5-card hand from available cards

### Phase 3: Turn
- **Input**: 1 additional community card (4 total)
- **Action**: Same betting options
- **State**: 6 total cards visible (2 private + 4 community)
- **Decision Logic**: Recalculate hand strength with new card

### Phase 4: River
- **Input**: Final community card (5 total)
- **Action**: Final betting round
- **State**: 7 total cards visible (2 private + 5 community)
- **Decision Logic**: Determine final best 5-card hand

## Hand Rankings (Strongest to Weakest)

| Rank | Hand Type | Example | Frequency |
|------|-----------|---------|-----------|
| 1 | Royal Flush | A♠ K♠ Q♠ J♠ 10♠ | 1:649,740 |
| 2 | Straight Flush | 9♥ 8♥ 7♥ 6♥ 5♥ | 1:72,193 |
| 3 | Four of a Kind | K♠ K♥ K♦ K♣ 3♦ | 1:4,165 |
| 4 | Full House | J♠ J♥ J♦ 7♣ 7♦ | 1:694 |
| 5 | Flush | A♦ J♦ 9♦ 5♦ 3♦ | 1:508 |
| 6 | Straight | 10♠ 9♥ 8♦ 7♣ 6♠ | 1:255 |
| 7 | Three of a Kind | 8♠ 8♥ 8♦ A♣ 5♦ | 1:47 |
| 8 | Two Pair | A♠ A♥ 6♦ 6♣ K♦ | 1:21 |
| 9 | One Pair | Q♠ Q♥ 10♦ 7♣ 4♠ | 1:2.37 |
| 10 | High Card | A♠ K♦ Q♥ J♣ 9♠ | 1:1.39 |


## Key Concepts for Implementation

### Hand Evaluation
- Always use best 5 cards from available 7 (2 hole + 5 community)
- Compare hands by rank first, then by highest card in rank
- Aces can be high (A-K-Q-J-10) or low (5-4-3-2-A)

### Pot Odds
```
pot_odds = call_amount / (pot_size + call_amount)
IF pot_odds < hand_equity THEN call
ELSE fold
```

### Position Value
- **Early**: Act first, less information
- **Middle**: Moderate information
- **Late**: Act last, most information (advantageous)

### Betting Actions
- **Fold**: Exit hand, lose chips invested
- **Check**: Pass action (only if no bet made)
- **Call**: Match current bet
- **Raise**: Increase bet amount
- **All-in**: Bet all remaining chips

## Implementation Notes

1. **State Management**: Track current phase, pot size, active players, and community cards
2. **Hand Comparison**: Implement ranking system with tie-breakers
3. **Probability**: Calculate drawing odds for incomplete hands
4. **Strategy**: Consider position, stack sizes, and opponent tendencies
5. **Validation**: Ensure all actions are legal for current game state
