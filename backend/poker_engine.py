"""Core poker engine for hand evaluation and analysis."""

from typing import List, Tuple, Dict
from phevaluator import evaluate_cards
import logging

logger = logging.getLogger(__name__)


class Card:
    """Represents a playing card."""
    
    RANKS = '23456789TJQKA'
    SUITS = 'shdc'
    RANK_VALUES = {r: i for i, r in enumerate(RANKS, 2)}
    
    def __init__(self, card_str: str):
        """Initialize card from string notation like 'As' or 'Kh'."""
        if len(card_str) != 2:
            raise ValueError(f"Invalid card format: {card_str}")
        
        rank, suit = card_str[0], card_str[1]
        
        if rank not in self.RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        
        self.rank = rank
        self.suit = suit
        self.value = self.RANK_VALUES[rank]
    
    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Card) and str(self) == str(other)
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def __repr__(self) -> str:
        return f"Card('{self}')"


class PokerEngine:
    """Core poker engine for hand evaluation and analysis."""
    
    def __init__(self):
        """Initialize poker engine."""
        self.deck = self._create_deck()
    
    def _create_deck(self) -> List[Card]:
        """Create a standard 52-card deck."""
        deck = []
        for rank in Card.RANKS:
            for suit in Card.SUITS:
                deck.append(Card(f"{rank}{suit}"))
        return deck
    
    def parse_cards(self, card_strings: List[str]) -> List[Card]:
        """Convert card strings to Card objects."""
        return [Card(card_str) for card_str in card_strings]
    
    def get_remaining_deck(self, known_cards: List[Card]) -> List[Card]:
        """Get remaining cards in deck excluding known cards."""
        known_set = set(str(card) for card in known_cards)
        return [card for card in self.deck if str(card) not in known_set]
    
    def evaluate_hand_strength(self, hole_cards: List[Card], community_cards: List[Card]) -> int:
        """
        Evaluate hand strength using phevaluator.
        Lower numbers = stronger hands.
        """
        try:
            # Convert to phevaluator format
            all_cards = [str(card) for card in hole_cards + community_cards]
            
            if len(all_cards) < 5:
                # Not enough cards for evaluation
                return 9999
            
            # Use phevaluator to get hand strength
            hand_rank = evaluate_cards(*all_cards)
            return hand_rank
            
        except Exception as e:
            logger.error(f"Error evaluating hand: {e}")
            return 9999
    
    def get_hand_type_from_rank(self, rank: int) -> str:
        """Get hand type string from phevaluator rank."""
        if rank <= 10:
            return "straight_flush"
        elif rank <= 166:
            return "four_of_a_kind"
        elif rank <= 322:
            return "full_house"
        elif rank <= 1599:
            return "flush"
        elif rank <= 1609:
            return "straight"
        elif rank <= 2467:
            return "three_of_a_kind"
        elif rank <= 3325:
            return "two_pair"
        elif rank <= 6185:
            return "pair"
        else:
            return "high_card"
    
    def is_flush_draw(self, hole_cards: List[Card], community_cards: List[Card]) -> Tuple[bool, str]:
        """Check if there's a flush draw and return the suit."""
        suit_counts = {}
        all_cards = hole_cards + community_cards
        
        for card in all_cards:
            suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
        
        # Need 4 cards of same suit for flush draw
        for suit, count in suit_counts.items():
            if count == 4:
                return True, suit
        
        return False, ""
    
    def is_straight_draw(self, hole_cards: List[Card], community_cards: List[Card]) -> Tuple[bool, List[int]]:
        """
        Check for straight draws and return the ranks needed.
        Returns (has_draw, needed_ranks).
        """
        all_cards = hole_cards + community_cards
        ranks = sorted(set(card.value for card in all_cards))
        
        # Check for open-ended straight draws
        needed_ranks = []
        
        # Check all possible 5-card straights
        for start in range(2, 11):  # 2 to 10 (A-5 straight starts at 1)
            straight_ranks = list(range(start, start + 5))
            missing = [r for r in straight_ranks if r not in ranks]
            
            if len(missing) == 1:  # Need exactly 1 card for straight
                needed_ranks.extend(missing)
        
        # Special case for A-5 straight (wheel)
        wheel_ranks = [14, 2, 3, 4, 5]  # A, 2, 3, 4, 5
        missing_wheel = [r for r in wheel_ranks if r not in ranks]
        if len(missing_wheel) == 1:
            needed_ranks.extend(missing_wheel)
        
        # Check for open-ended draws (need 2 cards on ends)
        for start in range(2, 10):
            straight_ranks = list(range(start, start + 5))
            missing = [r for r in straight_ranks if r not in ranks]
            
            if len(missing) == 2 and missing == [start - 1, start + 4]:
                # Open-ended draw
                needed_ranks.extend(missing)
        
        return len(needed_ranks) > 0, list(set(needed_ranks))
    
    def count_rank_occurrences(self, cards: List[Card]) -> Dict[int, int]:
        """Count occurrences of each rank."""
        rank_counts = {}
        for card in cards:
            rank_counts[card.value] = rank_counts.get(card.value, 0) + 1
        return rank_counts
    
    def get_pairs_and_sets(self, hole_cards: List[Card], community_cards: List[Card]) -> Dict[str, List[int]]:
        """Get information about pairs, trips, and quads."""
        all_cards = hole_cards + community_cards
        rank_counts = self.count_rank_occurrences(all_cards)
        
        pairs = []
        trips = []
        quads = []
        
        for rank, count in rank_counts.items():
            if count == 2:
                pairs.append(rank)
            elif count == 3:
                trips.append(rank)
            elif count == 4:
                quads.append(rank)
        
        return {
            'pairs': pairs,
            'trips': trips,
            'quads': quads
        }
    
    def has_royal_flush_draw(self, hole_cards: List[Card], community_cards: List[Card]) -> Tuple[bool, str]:
        """Check for royal flush draw (need A, K, Q, J, 10 of same suit)."""
        suit_cards = {}
        all_cards = hole_cards + community_cards
        
        # Group cards by suit
        for card in all_cards:
            if card.suit not in suit_cards:
                suit_cards[card.suit] = []
            suit_cards[card.suit].append(card.value)
        
        # Check each suit for royal flush potential
        royal_ranks = {14, 13, 12, 11, 10}  # A, K, Q, J, 10
        
        for suit, ranks in suit_cards.items():
            if len(ranks) >= 4:  # Need at least 4 cards of same suit
                suit_ranks = set(ranks)
                missing = royal_ranks - suit_ranks
                if len(missing) <= 1:  # Missing 0 or 1 card for royal
                    return True, suit
        
        return False, ""
    
    def is_nuts_when_completed(self, hole_cards: List[Card], community_cards: List[Card], completing_card: Card = None) -> bool:
        """
        Check if completing the hand with the given card results in the absolute nuts,
        or if the current hand is already the nuts (when completing_card is None).
        
        This method determines if the completed 5-card hand (using both hole cards and community cards)
        would be the best possible hand given the current board state.
        
        Args:
            hole_cards: Player's hole cards (exactly 2)
            community_cards: Current community cards (3-5 cards) 
            completing_card: The card that would complete the draw (None for river scenarios)
            
        Returns:
            bool: True if the completed hand is the absolute nuts and uses both hole cards
        """
        # Must have exactly 2 hole cards
        if len(hole_cards) != 2:
            return False
            
        # For river scenarios (no completing card needed)
        if completing_card is None:
            # Must have exactly 5 community cards for river
            if len(community_cards) != 5:
                return False
                
            # Check current hand directly
            player_hand_strength = self.evaluate_hand_strength(hole_cards, community_cards)
            
            # Check if the player's hand uses at least one hole card
            if not self._uses_at_least_one_hole_card(hole_cards, community_cards):
                return False
                
            # Find the absolute best possible hand given the board
            # Use the fixed version that excludes already known cards
            all_known_cards = hole_cards + community_cards
            best_possible_strength = self._find_best_possible_hand_strength_excluding_known(community_cards, all_known_cards)
            
            # Return true if player's hand is the best possible hand (or tied for best)
            # In phevaluator, lower numbers are better, so nuts means player_strength <= best_possible
            return player_hand_strength <= best_possible_strength
        
        # For non-river scenarios (completing card provided)
        # Create the completed board - Fix eight-card bug by limiting to 5 cards max
        completed_board = community_cards + [completing_card]
        
        # Fix: Ensure we don't exceed 5 community cards (avoid eight-card hands)
        if len(completed_board) > 5:
            logger.warning(f"Attempted to create board with {len(completed_board)} cards - limiting to 5")
            return False
        
        # Special handling for flush NUTS detection
        if self._is_flush_nuts_scenario(hole_cards, completed_board, completing_card):
            return self._check_flush_nuts(hole_cards, completed_board, completing_card)
        
        # Evaluate the player's best 5-card hand using both hole cards
        player_hand_strength = self.evaluate_hand_strength(hole_cards, completed_board)
        
        # Check if the player's hand uses at least one hole card (not just playing the board)
        if not self._uses_at_least_one_hole_card(hole_cards, completed_board):
            return False
            
        # Find the absolute best possible hand given the completed board
        # Use the fixed version that excludes already known cards
        all_known_for_completed = hole_cards + completed_board
        best_possible_strength = self._find_best_possible_hand_strength_excluding_known(completed_board, all_known_for_completed)
        
        # Return true if player's hand is the best possible hand (or tied for best)
        # In phevaluator, lower numbers are better, so nuts means player_strength <= best_possible
        return player_hand_strength <= best_possible_strength
    
    def _uses_both_hole_cards(self, hole_cards: List[Card], board: List[Card]) -> bool:
        """
        Check if the best 5-card hand uses both hole cards (not just playing the board).
        
        A hand "uses both hole cards" if both hole cards are part of the best 5-card combination.
        """
        if len(hole_cards) != 2:
            return False
            
        # If board has fewer than 5 cards, hole cards must be used
        if len(board) < 5:
            return True
        
        # For boards with 5+ cards, we need to determine if both hole cards
        # are part of the best 5-card hand
        if len(board) >= 5:
            all_cards = hole_cards + board
            player_strength = self.evaluate_hand_strength(hole_cards, board)
            
            # Test what happens if we use only one hole card
            for i, hole_card in enumerate(hole_cards):
                other_hole_card = hole_cards[1-i]
                
                # Find the best possible hand using only one hole card and the board
                remaining = self.get_remaining_deck(all_cards)
                if remaining:
                    # Try with a dummy card instead of the second hole card
                    dummy_card = remaining[0]  # Use first available card as dummy
                    single_hole_strength = self.evaluate_hand_strength([hole_card, dummy_card], board)
                    
                    # If using only one hole card gives the same strength,
                    # then not both hole cards are needed
                    if single_hole_strength <= player_strength:
                        return False
            
            # Test if board-only hand (5 cards from board) is as good
            if len(board) == 5:
                # Create dummy hole cards that won't interfere
                remaining = self.get_remaining_deck(all_cards)
                if len(remaining) >= 2:
                    dummy_cards = remaining[:2]
                    board_only_strength = self.evaluate_hand_strength(dummy_cards, board)
                    
                    # If board-only is as good or better, hole cards aren't both used
                    if board_only_strength <= player_strength:
                        return False
        
        return True
    
    def _uses_at_least_one_hole_card(self, hole_cards: List[Card], board: List[Card]) -> bool:
        """
        Check if the best 5-card hand uses at least one hole card (not just playing the board).
        
        A hand "uses at least one hole card" if one or both hole cards are part of the best 5-card combination.
        This is less restrictive than requiring both hole cards.
        """
        if len(hole_cards) != 2:
            return False
            
        # If board has fewer than 5 cards, hole cards must be used
        if len(board) < 5:
            return True
        
        # For boards with 5+ cards, we need to determine if at least one hole card
        # is part of the best 5-card hand
        if len(board) >= 5:
            all_cards = hole_cards + board
            player_strength = self.evaluate_hand_strength(hole_cards, board)
            
            # Test if board-only hand (5 cards from board) is as good
            if len(board) == 5:
                # Create dummy hole cards that won't interfere
                remaining = self.get_remaining_deck(all_cards)
                if len(remaining) >= 2:
                    dummy_cards = remaining[:2]
                    board_only_strength = self.evaluate_hand_strength(dummy_cards, board)
                    
                    # If board-only is as good or better, no hole cards are used
                    if board_only_strength <= player_strength:
                        return False
            
            # If we reach here, at least one hole card is being used
            return True
        
        return True
    
    def _find_best_possible_hand_strength(self, board: List[Card]) -> int:
        """
        Find the best possible 5-card hand strength given the board.
        
        This evaluates all possible hole card combinations to find the absolute nuts.
        Fixed to handle 5-card boards properly without creating 8-card hands.
        """
        best_strength = 9999  # Worst possible hand
        remaining_deck = self.get_remaining_deck(board)
        
        # Ensure we don't have too many cards
        if len(board) > 5:
            logger.error(f"Board has too many cards: {len(board)}")
            return best_strength
        
        # Try all possible 2-card combinations from remaining deck
        for i in range(len(remaining_deck)):
            for j in range(i + 1, len(remaining_deck)):
                test_hole_cards = [remaining_deck[i], remaining_deck[j]]
                # This ensures we have at most 2 + 5 = 7 cards for evaluation
                try:
                    hand_strength = self.evaluate_hand_strength(test_hole_cards, board)
                    
                    # Lower number = better hand
                    if hand_strength < best_strength:
                        best_strength = hand_strength
                except Exception as e:
                    # Skip invalid combinations and continue
                    continue
        
        return best_strength
    
    def _is_flush_nuts_scenario(self, hole_cards: List[Card], completed_board: List[Card], completing_card: Card) -> bool:
        """
        Check if this is a flush scenario that requires special NUTS handling.
        
        Returns True if:
        1. The completing card makes a flush
        2. There are no pairs on the board (no full house/quads possible)
        3. No straight flush is possible
        """
        all_cards = hole_cards + completed_board
        
        # Check if we have a flush
        suit_counts = {}
        for card in all_cards:
            suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
        
        flush_suit = None
        for suit, count in suit_counts.items():
            if count >= 5:
                flush_suit = suit
                break
        
        if not flush_suit:
            return False
        
        # Check if board has pairs (full house/quads possible)
        board_rank_counts = self.count_rank_occurrences(completed_board)
        board_has_pairs = any(count >= 2 for count in board_rank_counts.values())
        
        if board_has_pairs:
            return False  # Full house/quads possible, not a simple flush scenario
        
        # Check for straight flush possibility
        flush_cards = [card for card in all_cards if card.suit == flush_suit]
        flush_ranks = sorted([card.value for card in flush_cards])
        
        # Simple check for straight flush - if 5 consecutive ranks in flush suit
        if self._has_straight_flush_potential(flush_ranks):
            return False  # Straight flush possible, use general evaluation
        
        return True
    
    def _has_straight_flush_potential(self, flush_ranks: List[int]) -> bool:
        """
        Check if the flush ranks have straight flush potential.
        """
        if len(flush_ranks) < 5:
            return False
        
        # Check for consecutive sequences of 5 or more
        for i in range(len(flush_ranks) - 4):
            if flush_ranks[i+4] - flush_ranks[i] == 4:
                return True
        
        # Check for wheel straight flush (A,2,3,4,5)
        if 14 in flush_ranks and 2 in flush_ranks and 3 in flush_ranks and 4 in flush_ranks and 5 in flush_ranks:
            return True
        
        return False
    
    def _check_flush_nuts(self, hole_cards: List[Card], completed_board: List[Card], completing_card: Card) -> bool:
        """
        Check if the player has the nut flush.
        
        For a flush to be nuts:
        1. The completed flush must be ace-high (Ace either in hole cards or completing card)
        2. At least one hole card must contribute to the flush (not board-only)
        """
        all_cards = hole_cards + completed_board
        
        # Find the flush suit
        suit_counts = {}
        for card in all_cards:
            suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
        
        flush_suit = None
        for suit, count in suit_counts.items():
            if count >= 5:
                flush_suit = suit
                break
        
        if not flush_suit:
            return False
        
        # Check if the flush is ace-high (ace can be in hole cards OR the completing card)
        player_has_ace_of_suit = any(
            card.rank == 'A' and card.suit == flush_suit 
            for card in hole_cards
        )
        
        completing_card_is_ace = (
            completing_card.rank == 'A' and completing_card.suit == flush_suit
        )
        
        if not (player_has_ace_of_suit or completing_card_is_ace):
            return False
        
        # Check if at least one hole card contributes to the flush
        hole_cards_in_flush = [
            card for card in hole_cards 
            if card.suit == flush_suit
        ]
        
        if len(hole_cards_in_flush) == 0:
            return False  # No hole cards contribute to flush
        
        # Special case: if board (excluding completing card) already has 4 cards of flush suit,
        # and completing card makes 5th, then hole cards must be meaningful
        original_board_flush_cards = [
            card for card in completed_board 
            if card.suit == flush_suit and card != completing_card
        ]
        
        # If original board + completing card = 5 flush cards, this is board-only
        if len(original_board_flush_cards) + (1 if completing_card.suit == flush_suit else 0) >= 5:
            return False  # Board-only flush
        
        # If we get here, player has ace-high flush with meaningful hole card contribution
        return True
    
    def _find_best_possible_hand_strength_excluding_known(self, board: List[Card], all_known_cards: List[Card]) -> int:
        """
        Find the best possible 5-card hand strength given the board, excluding all known cards.
        
        This properly excludes both hole cards and community cards from the remaining deck.
        Used for river NUTS detection where we need to check if anyone else could have a better hand.
        """
        best_strength = 9999  # Worst possible hand
        remaining_deck = self.get_remaining_deck(all_known_cards)
        
        # Ensure we don't have too many cards
        if len(board) > 5:
            logger.error(f"Board has too many cards: {len(board)}")
            return best_strength
        
        # Try all possible 2-card combinations from remaining deck
        for i in range(len(remaining_deck)):
            for j in range(i + 1, len(remaining_deck)):
                test_hole_cards = [remaining_deck[i], remaining_deck[j]]
                # This ensures we have at most 2 + 5 = 7 cards for evaluation
                try:
                    hand_strength = self.evaluate_hand_strength(test_hole_cards, board)
                    
                    # Lower number = better hand
                    if hand_strength < best_strength:
                        best_strength = hand_strength
                except Exception as e:
                    # Skip invalid combinations and continue
                    continue
        
        return best_strength