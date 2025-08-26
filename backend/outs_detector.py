"""Outs detection algorithm with draw type classification."""

from typing import List, Dict, Tuple
from poker_engine import PokerEngine, Card
import logging

logger = logging.getLogger(__name__)


class OutsDetector:
    """Detects outs and classifies draw types for poker hands."""
    
    def __init__(self, poker_engine: PokerEngine):
        """Initialize outs detector with poker engine."""
        self.engine = poker_engine
    
    def find_outs(self, hole_cards: List[Card], community_cards: List[Card]) -> List[Dict[str, str]]:
        """
        Find all outs for the given hand that create hands likely to win the pot.
        Returns list of dictionaries with 'card' and 'draw_type' keys.
        
        An 'out' is specifically a card that creates a strong draw (straight, flush, 
        top pair, trips, etc.) that would likely win the pot - not just any improvement.
        """
        # Get current hand strength for validation
        current_strength = self.engine.evaluate_hand_strength(hole_cards, community_cards)
        
        outs = []
        outs_dict = {}  # Track cards with their best draw type
        
        # Find royal flush draws FIRST (highest priority - special case of straight flush)
        royal_flush_outs = self._find_royal_flush_outs(hole_cards, community_cards)
        for card_str, draw_type in royal_flush_outs:
            if self._validates_as_out(hole_cards, community_cards, card_str, current_strength):
                outs_dict[card_str] = 'royal flush'  # Royal flush has highest priority
        
        # Find straight flush draws (second highest priority)
        straight_flush_outs = self._find_straight_flush_outs(hole_cards, community_cards)
        for card_str, draw_type in straight_flush_outs:
            # Only add if not already a royal flush out
            if card_str not in outs_dict and self._validates_as_out(hole_cards, community_cards, card_str, current_strength):
                outs_dict[card_str] = 'straight flush'
        
        # Find flush draws (9 outs)
        flush_outs = self._find_flush_outs(hole_cards, community_cards)
        for card_str, draw_type in flush_outs:
            # Only add if not already a royal/straight flush out
            if card_str not in outs_dict and self._validates_as_out(hole_cards, community_cards, card_str, current_strength):
                outs_dict[card_str] = draw_type
        
        # Find straight draws (4 or 8 outs)
        straight_outs = self._find_straight_outs(hole_cards, community_cards)
        for card_str, draw_type in straight_outs:
            if card_str not in outs_dict and self._validates_as_out(hole_cards, community_cards, card_str, current_strength):
                outs_dict[card_str] = draw_type
        
        # Find overcard outs (typically 6 outs for two overcards)
        overcard_outs = self._find_overcard_outs(hole_cards, community_cards)
        for card_str, draw_type in overcard_outs:
            if card_str not in outs_dict and self._validates_as_out(hole_cards, community_cards, card_str, current_strength):
                outs_dict[card_str] = 'pair'  # Overcards make pairs
        
        # Find set/trips to full house or quads (4-7 outs)
        improvement_outs = self._find_improvement_outs(hole_cards, community_cards)
        for card_str, draw_type in improvement_outs:
            if card_str not in outs_dict and self._validates_as_out(hole_cards, community_cards, card_str, current_strength):
                # Normalize the draw type  
                normalized_type = draw_type.replace('_', ' ')
                outs_dict[card_str] = normalized_type
        
        # Find two-pair outs (when unpaired hole cards can pair with board)
        two_pair_outs = self._find_two_pair_outs(hole_cards, community_cards)
        for card_str, draw_type in two_pair_outs:
            if card_str not in outs_dict and self._validates_as_out(hole_cards, community_cards, card_str, current_strength):
                outs_dict[card_str] = 'two pair'
        
        # Convert dict to list of dicts
        for card_str, draw_type in outs_dict.items():
            outs.append({'card': card_str, 'draw_type': draw_type})
        
        return outs
    
    def _validates_as_out(self, hole_cards: List[Card], community_cards: List[Card], card_str: str, current_strength: int) -> bool:
        """Validate that a potential out actually improves the hand strength."""
        try:
            out_card = Card(card_str)
            new_strength = self.engine.evaluate_hand_strength(hole_cards, community_cards + [out_card])
            # Lower rank = better hand in phevaluator
            return new_strength < current_strength
        except:
            return False
    
    def _find_flush_outs(self, hole_cards: List[Card], community_cards: List[Card]) -> List[Tuple[str, str]]:
        """Find cards that complete a flush draw or improve an existing flush."""
        outs = []
        all_cards = hole_cards + community_cards
        
        # Count cards by suit
        suit_counts = {}
        for card in all_cards:
            suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
        
        # Find suits with 4 or more cards (flush draws or completed flushes)
        for suit, count in suit_counts.items():
            if count >= 4:
                # Find all remaining cards of this suit
                remaining_deck = self.engine.get_remaining_deck(all_cards)
                for card in remaining_deck:
                    if card.suit == suit:
                        # For both completed flushes and flush draws, classify as flush
                        draw_type = 'flush'
                        outs.append((str(card), draw_type))
        
        return outs
    
    def _find_straight_outs(self, hole_cards: List[Card], community_cards: List[Card]) -> List[Tuple[str, str]]:
        """Find cards that complete straight draws (gutshot=4 outs, open-ended=8 outs)."""
        outs = []
        all_cards = hole_cards + community_cards
        ranks = sorted(set(card.value for card in all_cards))
        remaining_deck = self.engine.get_remaining_deck(all_cards)
        
        # All possible 5-card straights
        possible_straights = [
            [2, 3, 4, 5, 6],   # 6-high
            [3, 4, 5, 6, 7],   # 7-high  
            [4, 5, 6, 7, 8],   # 8-high
            [5, 6, 7, 8, 9],   # 9-high
            [6, 7, 8, 9, 10],  # 10-high
            [7, 8, 9, 10, 11], # J-high
            [8, 9, 10, 11, 12], # Q-high
            [9, 10, 11, 12, 13], # K-high
            [10, 11, 12, 13, 14], # A-high
            [2, 3, 4, 5, 14]   # wheel (A-5)
        ]
        
        straight_completing_ranks = set()
        
        for straight in possible_straights:
            missing = [rank for rank in straight if rank not in ranks]
            
            # Only count straights missing exactly 1 card
            if len(missing) == 1:
                missing_rank = missing[0]
                
                # Check if we have exactly 4 cards from this straight
                present = [rank for rank in straight if rank in ranks]
                if len(present) == 4:
                    straight_completing_ranks.add(missing_rank)
        
        # Convert ranks to actual cards
        for rank in straight_completing_ranks:
            for card in remaining_deck:
                if card.value == rank:
                    # Determine if it's gutshot (inside) or open-ended
                    draw_type = self._classify_straight_draw(rank, ranks)
                    outs.append((str(card), draw_type))
        
        return outs
    
    def _classify_straight_draw(self, completing_rank: int, current_ranks: List[int]) -> str:
        """Classify straight draws - returns 'straight' for both gutshot and open-ended."""
        # Return 'straight' for all straight draws, keeping the detail in descriptions
        return 'straight'
    
    def _find_overcard_outs(self, hole_cards: List[Card], community_cards: List[Card]) -> List[Tuple[str, str]]:
        """Find overcards that would make top pair (typically 6 outs for two overcards)."""
        outs = []
        
        if not community_cards:  # Pre-flop, no overcards to consider
            return outs
        
        # Check if we already have a stronger draw (like flush draw or strong straight draw)
        # If we have a strong draw, don't count overcards
        all_cards = hole_cards + community_cards
        
        # Check for flush draws (exactly 4 cards of same suit)
        suit_counts = {}
        for card in all_cards:
            suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
        
        # If we have a flush draw (exactly 4 cards of same suit), don't count overcards
        # But allow overcards if we already have completed flush (5+ cards)
        for count in suit_counts.values():
            if count == 4:
                return outs  # Return empty list - flush draw takes priority
        
        # Check for straight draws - if we have a strong straight draw, don't count overcards
        straight_outs = self._find_straight_outs(hole_cards, community_cards)
        if len(straight_outs) >= 4:  # If we have 4+ straight outs, prioritize that
            return outs  # Return empty list - straight draw takes priority
        
        # Find highest card on board
        board_ranks = [card.value for card in community_cards]
        highest_board = max(board_ranks)
        
        # Check hole cards for overcards
        hole_ranks = [card.value for card in hole_cards]
        remaining_deck = self.engine.get_remaining_deck(hole_cards + community_cards)
        
        for hole_rank in hole_ranks:
            if hole_rank > highest_board:
                # This is an overcard - count remaining cards of this rank
                for card in remaining_deck:
                    if card.value == hole_rank:
                        outs.append((str(card), 'overcard'))
        
        return outs
    
    def _find_improvement_outs(self, hole_cards: List[Card], community_cards: List[Card]) -> List[Tuple[str, str]]:
        """Find outs for sets to full house/quads, pairs to trips, etc."""
        outs = []
        all_cards = hole_cards + community_cards
        rank_counts = self.engine.count_rank_occurrences(all_cards)
        remaining_deck = self.engine.get_remaining_deck(all_cards)
        
        # Check if board is paired (has any rank with count >= 2 in community cards only)
        board_rank_counts = self.engine.count_rank_occurrences(community_cards)
        board_has_pair = any(count >= 2 for count in board_rank_counts.values())
        
        for rank, count in rank_counts.items():
            if count == 2:  # Pair can become trips
                # Skip trips outs on paired boards - not "likely to win" due to full house threats
                if board_has_pair and board_rank_counts.get(rank, 0) >= 1:
                    # This pair involves board cards on an already paired board - skip
                    continue
                    
                for card in remaining_deck:
                    if card.value == rank:
                        outs.append((str(card), 'three of a kind'))
            elif count == 3:  # Trips can become quads or make full house
                # Quads
                for card in remaining_deck:
                    if card.value == rank:
                        outs.append((str(card), 'four of a kind'))
                
                # Full house - need another pair
                for other_rank, other_count in rank_counts.items():
                    if other_rank != rank and other_count >= 1:
                        for card in remaining_deck:
                            if card.value == other_rank:
                                # Only count if it would make a new pair (not already counted)
                                current_count = rank_counts.get(other_rank, 0)
                                if current_count == 1:  # Making a second pair for full house
                                    outs.append((str(card), 'full house'))
        
        return outs
    
    def _find_two_pair_outs(self, hole_cards: List[Card], community_cards: List[Card]) -> List[Tuple[str, str]]:
        """Find outs where unpaired hole cards can pair to make meaningful two-pair hands."""
        outs = []
        
        if len(community_cards) == 0:
            return outs  # No community cards to pair with
            
        # Get rank counts for all cards and board only
        all_cards = hole_cards + community_cards
        all_rank_counts = self.engine.count_rank_occurrences(all_cards)
        board_rank_counts = self.engine.count_rank_occurrences(community_cards)
        hole_rank_counts = self.engine.count_rank_occurrences(hole_cards)
        remaining_deck = self.engine.get_remaining_deck(all_cards)
        
        # Only proceed if we don't already have a pair or better
        # (two-pair outs are only relevant when we have high card or single pair)
        has_pair_or_better = any(count >= 2 for count in all_rank_counts.values())
        
        # If we already have two pair or better, two-pair outs aren't meaningful
        if sum(1 for count in all_rank_counts.values() if count >= 2) >= 2:
            return outs
        
        # Find unpaired hole cards that can pair with board ranks to make two pair
        for hole_card in hole_cards:
            hole_rank = hole_card.value
            
            # Skip if this hole card rank is already paired (count >= 2)
            if all_rank_counts.get(hole_rank, 0) >= 2:
                continue
                
            # Check if this hole card can pair to make meaningful two-pair
            # We need at least one pair on board to make two-pair meaningful
            if not any(count >= 2 for count in board_rank_counts.values()):
                continue
                
            # Count remaining cards of this rank as outs
            for card in remaining_deck:
                if card.value == hole_rank:
                    outs.append((str(card), 'two pair'))
                    
        return outs
    
    def _find_straight_flush_outs(self, hole_cards: List[Card], community_cards: List[Card]) -> List[Tuple[str, str]]:
        """Find cards that complete a straight flush draw (non-royal)."""
        outs = []
        all_cards = hole_cards + community_cards
        
        # Group cards by suit
        suit_cards = {}
        for card in all_cards:
            if card.suit not in suit_cards:
                suit_cards[card.suit] = []
            suit_cards[card.suit].append(card.value)
        
        # All possible 5-card straights (excluding royal)
        possible_straights = [
            [2, 3, 4, 5, 6],   # 6-high
            [3, 4, 5, 6, 7],   # 7-high  
            [4, 5, 6, 7, 8],   # 8-high
            [5, 6, 7, 8, 9],   # 9-high
            [6, 7, 8, 9, 10],  # 10-high
            [7, 8, 9, 10, 11], # J-high
            [8, 9, 10, 11, 12], # Q-high
            [9, 10, 11, 12, 13], # K-high
            # Skip [10, 11, 12, 13, 14] as that's royal flush
            [2, 3, 4, 5, 14]   # wheel (A-5)
        ]
        
        remaining_deck = self.engine.get_remaining_deck(all_cards)
        
        # Check each suit for straight flush potential
        for suit, ranks in suit_cards.items():
            ranks_set = set(ranks)
            
            # Check each possible straight
            for straight in possible_straights:
                missing = [rank for rank in straight if rank not in ranks_set]
                
                # Need exactly 4 cards from this straight in the same suit
                if len(missing) == 1:
                    missing_rank = missing[0]
                    # Find the card of this rank and suit
                    for card in remaining_deck:
                        if card.value == missing_rank and card.suit == suit:
                            outs.append((str(card), 'straight flush'))
        
        return outs
    
    def _find_royal_flush_outs(self, hole_cards: List[Card], community_cards: List[Card]) -> List[Tuple[str, str]]:
        """Find cards that complete a royal flush draw (A, K, Q, J, 10 of same suit)."""
        outs = []
        all_cards = hole_cards + community_cards
        
        # Royal flush cards for each suit
        royal_ranks = [14, 13, 12, 11, 10]  # A, K, Q, J, 10
        
        # Group cards by suit
        suit_cards = {}
        for card in all_cards:
            if card.suit not in suit_cards:
                suit_cards[card.suit] = set()
            suit_cards[card.suit].add(card.value)
        
        # Check each suit for royal flush potential
        remaining_deck = self.engine.get_remaining_deck(all_cards)
        
        for suit, ranks in suit_cards.items():
            # Check how many royal cards we have in this suit
            royal_cards_held = ranks.intersection(set(royal_ranks))
            
            # Need at least 4 royal cards to have a royal flush draw
            if len(royal_cards_held) >= 4:
                # Find the missing royal card(s)
                missing_royal = set(royal_ranks) - royal_cards_held
                
                # Add the missing royal card(s) as outs if available in deck
                for missing_rank in missing_royal:
                    for card in remaining_deck:
                        if card.value == missing_rank and card.suit == suit:
                            outs.append((str(card), 'royal flush'))
        
        return outs
    
    def count_outs(self, hole_cards: List[Card], community_cards: List[Card]) -> int:
        """Get the total number of outs for the given hand."""
        outs = self.find_outs(hole_cards, community_cards)
        return len(outs)
    
    
    def _analyze_flush_draws(self, hole_cards: List[Card], community_cards: List[Card]) -> Dict[str, List[str]]:
        """Analyze flush draws and return cards that complete them."""
        # Use the new flush outs method
        flush_outs_list = self._find_flush_outs(hole_cards, community_cards)
        
        # Group by suit for backward compatibility
        flush_outs = {}
        for card_str, draw_type in flush_outs_list:
            suit = card_str[1]  # Get suit from card string (e.g., 'As' -> 's')
            if suit not in flush_outs:
                flush_outs[suit] = []
            flush_outs[suit].append(card_str)
        
        return flush_outs
    
    def _analyze_straight_draws(self, hole_cards: List[Card], community_cards: List[Card]) -> List[int]:
        """Analyze straight draws and return ranks that complete them."""
        # Use the new straight outs method and extract ranks
        straight_outs_list = self._find_straight_outs(hole_cards, community_cards)
        
        # Extract unique ranks from the card strings
        ranks = set()
        for card_str, draw_type in straight_outs_list:
            # Convert card string back to rank value
            card = Card(card_str)
            ranks.add(card.value)
        
        return list(ranks)
    
    def _get_pairing_outs(self, hole_cards: List[Card], community_cards: List[Card]) -> Dict[str, List[int]]:
        """Get outs that make pairs, trips, or quads - only for meaningful improvements."""
        # Use new methods to get overcard and improvement outs
        overcard_outs = self._find_overcard_outs(hole_cards, community_cards)
        improvement_outs = self._find_improvement_outs(hole_cards, community_cards)
        
        # Categorize by improvement type
        pair_outs = []
        trips_outs = []
        quads_outs = []
        
        # Process overcard outs (these make top pair)
        for card_str, draw_type in overcard_outs:
            card = Card(card_str)
            pair_outs.append(card.value)
        
        # Process improvement outs
        for card_str, draw_type in improvement_outs:
            card = Card(card_str)
            if draw_type == 'three of a kind':
                trips_outs.append(card.value)
            elif draw_type == 'four of a kind':
                quads_outs.append(card.value)
            elif draw_type == 'full house':
                # These could be categorized as trips for the purpose of making full house
                trips_outs.append(card.value)
        
        return {
            'pair': list(set(pair_outs)),
            'trips': list(set(trips_outs)),
            'quads': list(set(quads_outs))
        }
    
    def get_detailed_outs_analysis(self, hole_cards: List[Card], community_cards: List[Card]) -> Dict:
        """Get detailed analysis of all possible outs by category."""
        # Use the main find_outs method for accurate counting
        outs_list = self.find_outs(hole_cards, community_cards)
        
        analysis = {
            'flush_draws': self._analyze_flush_draws(hole_cards, community_cards),
            'straight_draws': self._analyze_straight_draws(hole_cards, community_cards),
            'pairing_outs': self._get_pairing_outs(hole_cards, community_cards),
            'total_outs': len(outs_list),
            'unique_out_cards': [out['card'] for out in outs_list],
            'outs_by_type': {}
        }
        
        # Group outs by draw type
        for out in outs_list:
            draw_type = out['draw_type']
            if draw_type not in analysis['outs_by_type']:
                analysis['outs_by_type'][draw_type] = []
            analysis['outs_by_type'][draw_type].append(out['card'])
        
        return analysis
