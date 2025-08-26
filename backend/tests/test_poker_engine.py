"""Tests for poker engine functionality."""

import pytest
from poker_engine import PokerEngine, Card


class TestCard:
    """Test Card class functionality."""
    
    def test_card_creation_valid(self):
        """Test creating valid cards."""
        card = Card("As")
        assert card.rank == "A"
        assert card.suit == "s"
        assert card.value == 14
        
        card2 = Card("2h")
        assert card2.rank == "2"
        assert card2.suit == "h"
        assert card2.value == 2
    
    def test_card_creation_invalid_rank(self):
        """Test creating cards with invalid rank."""
        with pytest.raises(ValueError, match="Invalid rank"):
            Card("Xs")
    
    def test_card_creation_invalid_suit(self):
        """Test creating cards with invalid suit."""
        with pytest.raises(ValueError, match="Invalid suit"):
            Card("Ax")
    
    def test_card_equality(self):
        """Test card equality."""
        card1 = Card("As")
        card2 = Card("As")
        card3 = Card("Ah")
        
        assert card1 == card2
        assert card1 != card3
    
    def test_card_string_representation(self):
        """Test card string representation."""
        card = Card("Kd")
        assert str(card) == "Kd"
        assert repr(card) == "Card('Kd')"


class TestPokerEngine:
    """Test PokerEngine functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = PokerEngine()
    
    def test_engine_initialization(self):
        """Test poker engine initialization."""
        assert len(self.engine.deck) == 52
        assert isinstance(self.engine.deck[0], Card)
    
    def test_parse_cards(self):
        """Test parsing card strings to Card objects."""
        cards = self.engine.parse_cards(["As", "Kh", "Qd"])
        
        assert len(cards) == 3
        assert all(isinstance(card, Card) for card in cards)
        assert str(cards[0]) == "As"
        assert str(cards[1]) == "Kh"
        assert str(cards[2]) == "Qd"
    
    def test_get_remaining_deck(self):
        """Test getting remaining cards in deck."""
        known_cards = self.engine.parse_cards(["As", "Kh"])
        remaining = self.engine.get_remaining_deck(known_cards)
        
        assert len(remaining) == 50
        assert not any(str(card) in ["As", "Kh"] for card in remaining)
    
    def test_evaluate_hand_strength_royal_flush(self):
        """Test hand evaluation with royal flush."""
        # Royal flush: As Ks Qs Js Ts
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["Qs", "Js", "Ts"])
        
        strength = self.engine.evaluate_hand_strength(hole_cards, community_cards)
        assert strength <= 10  # Royal flush is strongest
    
    def test_evaluate_hand_strength_high_card(self):
        """Test hand evaluation with high card."""
        # High card hand
        hole_cards = self.engine.parse_cards(["As", "7h"])
        community_cards = self.engine.parse_cards(["2d", "4c", "6s"])
        
        strength = self.engine.evaluate_hand_strength(hole_cards, community_cards)
        assert strength > 6185  # High card is weakest
    
    def test_evaluate_insufficient_cards(self):
        """Test hand evaluation with insufficient cards."""
        hole_cards = self.engine.parse_cards(["As", "Kh"])
        community_cards = self.engine.parse_cards(["Qd"])  # Only 3 total cards
        
        strength = self.engine.evaluate_hand_strength(hole_cards, community_cards)
        assert strength == 9999  # Should return max value for insufficient cards
    
    def test_get_hand_type_from_rank(self):
        """Test hand type classification from rank."""
        assert self.engine.get_hand_type_from_rank(1) == "straight_flush"
        assert self.engine.get_hand_type_from_rank(100) == "four_of_a_kind"
        assert self.engine.get_hand_type_from_rank(200) == "full_house"
        assert self.engine.get_hand_type_from_rank(1000) == "flush"
        assert self.engine.get_hand_type_from_rank(1605) == "straight"
        assert self.engine.get_hand_type_from_rank(2000) == "three_of_a_kind"
        assert self.engine.get_hand_type_from_rank(3000) == "two_pair"
        assert self.engine.get_hand_type_from_rank(5000) == "pair"
        assert self.engine.get_hand_type_from_rank(7000) == "high_card"
    
    def test_is_flush_draw(self):
        """Test flush draw detection."""
        # 4 spades = flush draw
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["Qs", "Js", "2h"])
        
        has_draw, suit = self.engine.is_flush_draw(hole_cards, community_cards)
        assert has_draw is True
        assert suit == "s"
        
        # No flush draw
        hole_cards = self.engine.parse_cards(["As", "Kh"])
        community_cards = self.engine.parse_cards(["Qd", "Jc", "2h"])
        
        has_draw, suit = self.engine.is_flush_draw(hole_cards, community_cards)
        assert has_draw is False
        assert suit == ""
    
    def test_is_straight_draw(self):
        """Test straight draw detection."""
        # Open-ended straight draw: 9-8-7-6, need 10 or 5
        hole_cards = self.engine.parse_cards(["9s", "8h"])
        community_cards = self.engine.parse_cards(["7d", "6c", "2h"])
        
        has_draw, needed_ranks = self.engine.is_straight_draw(hole_cards, community_cards)
        assert has_draw is True
        assert 10 in needed_ranks or 5 in needed_ranks
    
    def test_count_rank_occurrences(self):
        """Test rank counting."""
        cards = self.engine.parse_cards(["As", "Ah", "Kd", "Kc"])
        counts = self.engine.count_rank_occurrences(cards)
        
        assert counts[14] == 2  # Two aces
        assert counts[13] == 2  # Two kings
    
    def test_get_pairs_and_sets(self):
        """Test pairs and sets detection."""
        # Two pair: A-A-K-K-Q
        hole_cards = self.engine.parse_cards(["As", "Ah"])
        community_cards = self.engine.parse_cards(["Kd", "Kc", "Qs"])
        
        result = self.engine.get_pairs_and_sets(hole_cards, community_cards)
        
        assert len(result['pairs']) == 2  # Aces and Kings
        assert 14 in result['pairs']  # Aces
        assert 13 in result['pairs']  # Kings
        assert len(result['trips']) == 0
        assert len(result['quads']) == 0
    
    def test_has_royal_flush_draw(self):
        """Test royal flush draw detection."""
        # 4 to royal flush in spades
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["Qs", "Js", "2h"])
        
        has_draw, suit = self.engine.has_royal_flush_draw(hole_cards, community_cards)
        assert has_draw is True
        assert suit == "s"
    
    def test_is_nuts_when_completed_royal_flush(self):
        """Test NUTS detection with royal flush completion."""
        # Test case 1: Hole cards that DON'T complete royal flush
        # Hole cards: 9h 8c, Board: As Ks Qs Js (completing card Ts gives royal, but we don't have it)
        hole_cards = self.engine.parse_cards(["9h", "8c"])
        community_cards = self.engine.parse_cards(["As", "Ks", "Qs", "Js"])
        completing_card = Card("Ts")  # Completes royal flush, but not using our hole cards
        
        # This should be False since our hole cards (9h, 8c) don't contribute to royal flush
        is_nuts = self.engine.is_nuts_when_completed(hole_cards, community_cards, completing_card)
        assert is_nuts is False
        
        # Test case 2: Hole cards that DO complete royal flush
        # Hole cards: As 9h, Board: Ks Qs Js (completing card Ts gives royal using As)
        hole_cards = self.engine.parse_cards(["As", "9h"])
        community_cards = self.engine.parse_cards(["Ks", "Qs", "Js"])
        completing_card = Card("Ts")  # Completes royal flush using our As
        
        is_nuts = self.engine.is_nuts_when_completed(hole_cards, community_cards, completing_card)
        assert is_nuts is True
    
    def test_is_nuts_when_completed_straight_flush(self):
        """Test NUTS detection with straight flush completion."""
        # Board has potential for straight flush, but not the absolute nuts
        hole_cards = self.engine.parse_cards(["9s", "8s"])
        community_cards = self.engine.parse_cards(["7s", "6s", "2h"])
        completing_card = Card("Ts")  # Completes 10-high straight flush
        
        # This should be nuts if no royal flush is possible
        is_nuts = self.engine.is_nuts_when_completed(hole_cards, community_cards, completing_card)
        assert is_nuts is True
    
    def test_is_nuts_when_completed_not_using_both_hole_cards(self):
        """Test NUTS detection when completed hand doesn't use both hole cards."""
        # Board that makes royal flush without needing hole cards
        hole_cards = self.engine.parse_cards(["2h", "3c"])  # Irrelevant low cards
        community_cards = self.engine.parse_cards(["As", "Ks", "Qs", "Js"])
        completing_card = Card("Ts")  # Completes royal flush on board
        
        # This should be False because it doesn't use both hole cards meaningfully
        is_nuts = self.engine.is_nuts_when_completed(hole_cards, community_cards, completing_card)
        assert is_nuts is False
    
    def test_is_nuts_when_completed_quads(self):
        """Test NUTS detection with four of a kind."""
        # Pocket aces with paired board
        hole_cards = self.engine.parse_cards(["As", "Ah"])
        community_cards = self.engine.parse_cards(["Ad", "Kh", "Kd"])
        completing_card = Card("Ac")  # Completes quad aces (nuts)
        
        is_nuts = self.engine.is_nuts_when_completed(hole_cards, community_cards, completing_card)
        assert is_nuts is True
    
    def test_is_nuts_when_completed_full_house_not_nuts(self):
        """Test NUTS detection with full house that's not the nuts."""
        # Full house when four of a kind is possible
        hole_cards = self.engine.parse_cards(["3s", "3h"])
        community_cards = self.engine.parse_cards(["3d", "Kh", "Kd"])
        completing_card = Card("Kc")  # Completes full house, but four Kings is possible with Ks
        
        # This should be False because someone with Ks would have four Kings
        is_nuts = self.engine.is_nuts_when_completed(hole_cards, community_cards, completing_card)
        assert is_nuts is False
        
        # Test a case where full house IS the nuts
        # Board where no quads are possible
        hole_cards = self.engine.parse_cards(["As", "Ah"])
        community_cards = self.engine.parse_cards(["Ad", "Kh", "Qs"])
        completing_card = Card("Ac")  # Completes quad Aces (definitely nuts)
        
        is_nuts = self.engine.is_nuts_when_completed(hole_cards, community_cards, completing_card)
        assert is_nuts is True
    
    def test_is_nuts_when_completed_flush(self):
        """Test NUTS detection with nut flush."""
        # Nut flush draw on a board where no full house/quads are possible
        hole_cards = self.engine.parse_cards(["As", "Ks"])  # Ace high flush
        community_cards = self.engine.parse_cards(["Qs", "Js", "7h"])  # No pairs on board
        completing_card = Card("2s")  # Completes nut flush
        
        is_nuts = self.engine.is_nuts_when_completed(hole_cards, community_cards, completing_card)
        assert is_nuts is True
    
    def test_is_nuts_when_completed_straight(self):
        """Test NUTS detection with nut straight."""
        # Nut straight draw
        hole_cards = self.engine.parse_cards(["As", "Kd"])
        community_cards = self.engine.parse_cards(["Qh", "Jc", "2s"])
        completing_card = Card("Th")  # Completes Broadway straight (nuts)
        
        is_nuts = self.engine.is_nuts_when_completed(hole_cards, community_cards, completing_card)
        assert is_nuts is True
    
    def test_uses_both_hole_cards_simple(self):
        """Test the _uses_both_hole_cards method."""
        # Test case where hole cards are clearly used
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        board = self.engine.parse_cards(["Qs", "Js", "Ts", "2h", "3c"])  # Royal flush with hole cards
        
        uses_both = self.engine._uses_both_hole_cards(hole_cards, board)
        assert uses_both is True
        
        # Test case where board has the nuts
        hole_cards = self.engine.parse_cards(["2h", "3c"])  # Low cards
        board = self.engine.parse_cards(["As", "Ks", "Qs", "Js", "Ts"])  # Royal flush on board
        
        uses_both = self.engine._uses_both_hole_cards(hole_cards, board)
        assert uses_both is False
    
    def test_find_best_possible_hand_strength(self):
        """Test finding the best possible hand strength for a given board."""
        # Board with royal flush potential
        board = self.engine.parse_cards(["As", "Ks", "Qs", "Js", "2h"])
        
        best_strength = self.engine._find_best_possible_hand_strength(board)
        
        # Should find the royal flush as the best possible hand
        assert best_strength <= 10  # Royal flush strength