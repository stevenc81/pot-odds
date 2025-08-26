"""Pot odds calculator with precise probability formulas."""

from typing import List, Tuple
from poker_engine import PokerEngine, Card
from outs_detector import OutsDetector
import logging

logger = logging.getLogger(__name__)


class PotOddsCalculator:
    """Calculate pot odds with precise probability formulas."""
    
    def __init__(self, poker_engine: PokerEngine):
        """Initialize with poker engine."""
        self.engine = poker_engine
        self.outs_detector = OutsDetector(poker_engine)
    
    def calculate_pot_odds(self, hole_cards: List[Card], community_cards: List[Card]) -> Tuple[str, List[dict]]:
        """
        Calculate pot odds ratio and find outs.
        Returns (pot_odds_ratio, outs_list).
        
        Special case: If completing a five-card draw results in the absolute nuts 
        and uses both hole cards, returns "NUTS!" as pot_odds_ratio.
        For river scenarios (7 cards total), checks if the current completed hand is the nuts.
        """
        cards_seen = len(hole_cards) + len(community_cards)
        
        # Check for NUTS scenario BEFORE outs detection
        nuts_detected = False
        
        if cards_seen == 7:  # River - check current completed hand
            nuts_detected = self._check_for_river_nuts(hole_cards, community_cards)
            # On the river, there are no more cards to come, so no outs
            if nuts_detected:
                return "NUTS!", []
            else:
                return "999.0:1", []
        elif cards_seen >= 5:  # No outs but 5+ cards - check if current hand is already nuts
            # This handles cases like a completed royal flush on the flop
            nuts_detected = self._check_for_completed_nuts(hole_cards, community_cards)
            if nuts_detected:
                # If current hand is already nuts, don't look for outs
                return "NUTS!", []
        
        # Find all outs (only when not on river)
        outs = self.outs_detector.find_outs(hole_cards, community_cards)
        
        if not outs:
            return "999.0:1", []
        
        num_outs = len(outs)
        
        # Calculate win probability based on game phase
        if cards_seen == 5:  # Flop (2 cards to come)
            win_probability = self._calculate_flop_probability(num_outs)
        elif cards_seen == 6:  # Turn (1 card to come)
            win_probability = self._calculate_turn_probability(num_outs)
        else:
            # Pre-flop or other situations - use flop calculation as default
            win_probability = self._calculate_flop_probability(num_outs)
        
        # Calculate pot odds ratio
        pot_odds_ratio = self._format_pot_odds_ratio(win_probability)
        
        return pot_odds_ratio, outs
    
    
    
    def _check_for_river_nuts(self, hole_cards: List[Card], community_cards: List[Card]) -> bool:
        """
        Check if the current completed hand (at river) is the absolute nuts.
        
        This is used when all 7 cards are known and no outs exist.
        Returns True if the current 5-card hand is the best possible and uses at least one hole card.
        """
        try:
            # Must have exactly 2 hole cards and 5 community cards
            if len(hole_cards) != 2 or len(community_cards) != 5:
                return False
            
            # Evaluate the player's best 5-card hand
            player_hand_strength = self.engine.evaluate_hand_strength(hole_cards, community_cards)
            
            # Check if the player's hand uses at least one hole card
            if not self.engine._uses_at_least_one_hole_card(hole_cards, community_cards):
                return False
            
            # Find the absolute best possible hand given the board
            # Pass all known cards (hole + community) to exclude them from remaining deck
            all_known_cards = hole_cards + community_cards
            best_possible_strength = self.engine._find_best_possible_hand_strength_excluding_known(community_cards, all_known_cards)
            
            # Return true if player's hand is the best possible hand (or tied for best)
            # In phevaluator, lower numbers are better, so nuts means player_strength <= best_possible
            return player_hand_strength <= best_possible_strength
            
        except Exception as e:
            logger.warning(f"Error checking river nuts: {e}")
            return False
    
    def _check_for_completed_nuts(self, hole_cards: List[Card], community_cards: List[Card]) -> bool:
        """
        Check if the current hand is already the absolute nuts (no outs needed).
        
        This is used when we have 5+ cards total and no outs, but the hand might already be nuts.
        For example, a completed royal flush on the flop.
        Returns True if the current 5-card hand is the best possible and uses at least one hole card.
        """
        try:
            # Must have exactly 2 hole cards
            if len(hole_cards) != 2:
                return False
            
            # Must have at least 3 community cards to form a 5-card hand
            if len(community_cards) < 3:
                return False
            
            # Evaluate the player's best 5-card hand
            player_hand_strength = self.engine.evaluate_hand_strength(hole_cards, community_cards)
            
            # Check if the player's hand uses at least one hole card
            if not self.engine._uses_at_least_one_hole_card(hole_cards, community_cards):
                return False
            
            # Find the absolute best possible hand given the current board
            # Pass all known cards (hole + community) to exclude them from remaining deck
            all_known_cards = hole_cards + community_cards
            best_possible_strength = self.engine._find_best_possible_hand_strength_excluding_known(community_cards, all_known_cards)
            
            # Return true if player's hand is the best possible hand (or tied for best)
            # In phevaluator, lower numbers are better, so nuts means player_strength <= best_possible
            result = player_hand_strength <= best_possible_strength
            
            if result:
                logger.info(f"NUTS detected for completed hand: player_strength={player_hand_strength}, best_possible={best_possible_strength}")
            
            return result
            
        except Exception as e:
            logger.warning(f"Error checking completed nuts: {e}")
            return False
    
    def _calculate_flop_probability(self, num_outs: int) -> float:
        """
        Calculate probability with 2 cards to come (flop).
        Formula: 1 - [(47-outs)/47] × [(46-outs)/46]
        """
        if num_outs <= 0:
            return 0.0
        if num_outs >= 47:
            return 1.0
        
        miss_turn = (47 - num_outs) / 47
        miss_river = (46 - num_outs) / 46
        miss_both = miss_turn * miss_river
        win_probability = 1 - miss_both
        
        return win_probability
    
    def _calculate_turn_probability(self, num_outs: int) -> float:
        """
        Calculate probability with 1 card to come (turn).
        Formula: outs / 46
        """
        if num_outs <= 0:
            return 0.0
        if num_outs >= 46:
            return 1.0
        
        return num_outs / 46
    
    def _format_pot_odds_ratio(self, win_probability: float) -> str:
        """
        Format pot odds ratio as X.X:1, rounded to first decimal.
        If decimal is .0, show as integer (e.g., 4:1 instead of 4.0:1).
        """
        if win_probability <= 0:
            return "999.0:1"
        if win_probability >= 1:
            return "0.0:1"
        
        lose_probability = 1 - win_probability
        ratio = lose_probability / win_probability
        
        # Round to 1 decimal place
        ratio_rounded = round(ratio, 1)
        
        # Format as string
        if ratio_rounded == int(ratio_rounded):
            return f"{int(ratio_rounded)}:1"
        else:
            return f"{ratio_rounded}:1"
    
    def get_probability_breakdown(self, hole_cards: List[Card], community_cards: List[Card]) -> dict:
        """Get detailed probability breakdown for analysis."""
        outs = self.outs_detector.find_outs(hole_cards, community_cards)
        num_outs = len(outs)
        cards_seen = len(hole_cards) + len(community_cards)
        
        breakdown = {
            'num_outs': num_outs,
            'cards_seen': cards_seen,
            'unseen_cards': 52 - cards_seen,
            'outs_by_type': {}
        }
        
        # Group outs by draw type
        for out in outs:
            draw_type = out['draw_type']
            if draw_type not in breakdown['outs_by_type']:
                breakdown['outs_by_type'][draw_type] = []
            breakdown['outs_by_type'][draw_type].append(out['card'])
        
        # Calculate probabilities for different scenarios
        if cards_seen == 5:  # Flop
            breakdown['flop_probability'] = self._calculate_flop_probability(num_outs)
            breakdown['turn_probability'] = self._calculate_turn_probability(num_outs)
            breakdown['game_phase'] = 'flop'
        elif cards_seen == 6:  # Turn
            breakdown['turn_probability'] = self._calculate_turn_probability(num_outs)
            breakdown['game_phase'] = 'turn'
        else:
            breakdown['estimated_probability'] = self._calculate_flop_probability(num_outs)
            breakdown['game_phase'] = 'other'
        
        return breakdown
    
    def calculate_exact_odds_from_examples(self) -> dict:
        """
        Calculate exact odds for the examples from specifications.
        Used for verification and testing.
        """
        examples = {
            '4_outs_flop': {
                'probability': self._calculate_flop_probability(4),
                'ratio': self._format_pot_odds_ratio(self._calculate_flop_probability(4)),
                'expected': '5.1:1'
            },
            '4_outs_turn': {
                'probability': self._calculate_turn_probability(4),
                'ratio': self._format_pot_odds_ratio(self._calculate_turn_probability(4)),
                'expected': '10.5:1'
            },
            '6_outs_flop': {
                'probability': self._calculate_flop_probability(6),
                'ratio': self._format_pot_odds_ratio(self._calculate_flop_probability(6)),
                'expected': '3.1:1'
            },
            '8_outs_flop': {
                'probability': self._calculate_flop_probability(8),
                'ratio': self._format_pot_odds_ratio(self._calculate_flop_probability(8)),
                'expected': '2.2:1'
            },
            '9_outs_flop': {
                'probability': self._calculate_flop_probability(9),
                'ratio': self._format_pot_odds_ratio(self._calculate_flop_probability(9)),
                'expected': '1.9:1'
            },
            '15_outs_flop': {
                'probability': self._calculate_flop_probability(15),
                'ratio': self._format_pot_odds_ratio(self._calculate_flop_probability(15)),
                'expected': '0.85:1'
            }
        }
        
        return examples


# Numba optimized version for better performance
try:
    from numba import jit
    
    @jit(nopython=True)
    def _numba_calculate_flop_probability(num_outs: int) -> float:
        """Numba-optimized flop probability calculation."""
        if num_outs <= 0:
            return 0.0
        if num_outs >= 47:
            return 1.0
        
        miss_turn = (47 - num_outs) / 47
        miss_river = (46 - num_outs) / 46
        miss_both = miss_turn * miss_river
        return 1 - miss_both
    
    @jit(nopython=True)
    def _numba_calculate_turn_probability(num_outs: int) -> float:
        """Numba-optimized turn probability calculation."""
        if num_outs <= 0:
            return 0.0
        if num_outs >= 46:
            return 1.0
        
        return num_outs / 46
    
    class OptimizedPotOddsCalculator(PotOddsCalculator):
        """Numba-optimized version of pot odds calculator."""
        
        def _calculate_flop_probability(self, num_outs: int) -> float:
            return _numba_calculate_flop_probability(num_outs)
        
        def _calculate_turn_probability(self, num_outs: int) -> float:
            return _numba_calculate_turn_probability(num_outs)
        
        # NUTS detection doesn't need optimization since it's not performance-critical
        # and relies on complex object operations that aren't easily optimized with Numba

except ImportError:
    logger.warning("Numba not available, using standard calculator")
    OptimizedPotOddsCalculator = PotOddsCalculator