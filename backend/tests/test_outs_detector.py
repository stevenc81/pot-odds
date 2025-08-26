"""Tests for outs detection functionality."""

import pytest
from poker_engine import PokerEngine
from outs_detector import OutsDetector


class TestOutsDetector:
    """Test OutsDetector functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = PokerEngine()
        self.detector = OutsDetector(self.engine)
    
    def test_detector_initialization(self):
        """Test outs detector initialization."""
        assert self.detector.engine == self.engine
    
    def test_find_outs_inside_straight_draw(self):
        """Test finding outs for inside straight draw (gutshot) - should be exactly 4 outs."""
        # Hand: 9♠ 8♥, Board: 5♣ 6♦ K♠
        # Need 7 for straight (5-6-7-8-9) - EXACTLY 4 outs (the four 7s)
        hole_cards = self.engine.parse_cards(["9s", "8h"])
        community_cards = self.engine.parse_cards(["5c", "6d", "Ks"])
        
        outs = self.detector.find_outs(hole_cards, community_cards)
        
        # Should find EXACTLY 4 outs total (only the sevens)
        assert len(outs) == 4, f"Expected 4 outs but found {len(outs)}"
        
        # All outs should be sevens
        seven_outs = [out for out in outs if out['card'][0] == '7']
        assert len(seven_outs) == 4, f"Expected 4 sevens but found {len(seven_outs)}"
        
        # All sevens should be classified as straight draws
        for out in seven_outs:
            assert 'straight' in out['draw_type']
    
    def test_find_outs_open_ended_straight_draw(self):
        """Test finding outs for open-ended straight draw - should be exactly 8 outs."""
        # Hand: 9♠ 8♥, Board: 7♣ 6♦ 2♠
        # Need 10 or 5 for straight - EXACTLY 8 outs (4 tens + 4 fives)
        hole_cards = self.engine.parse_cards(["9s", "8h"])
        community_cards = self.engine.parse_cards(["7c", "6d", "2s"])
        
        outs = self.detector.find_outs(hole_cards, community_cards)
        
        # Should find EXACTLY 8 outs total
        assert len(outs) == 8, f"Expected 8 outs but found {len(outs)}"
        
        # Should find 4 tens and 4 fives
        tens = [out for out in outs if out['card'][0] == 'T']
        fives = [out for out in outs if out['card'][0] == '5']
        
        assert len(tens) == 4, f"Expected 4 tens but found {len(tens)}"
        assert len(fives) == 4, f"Expected 4 fives but found {len(fives)}"
        
        # All should be straight draws
        for out in outs:
            assert 'straight' in out['draw_type']
    
    def test_find_outs_flush_draw(self):
        """Test finding outs for flush draw - should be exactly 9 outs."""
        # Hand: A♠ K♠, Board: 7♠ 3♠ J♦
        # Need any spade for flush - EXACTLY 9 outs (remaining spades)
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["7s", "3s", "Jd"])
        
        outs = self.detector.find_outs(hole_cards, community_cards)
        
        # Should find EXACTLY 9 outs total (only the remaining spades)
        assert len(outs) == 9, f"Expected 9 outs but found {len(outs)}"
        
        # All outs should be spades and flush draws
        for out in outs:
            assert out['card'][1] == 's', f"Expected spade but found {out['card']}"
            assert out['draw_type'] == 'flush'
    
    def test_find_outs_two_overcards(self):
        """Test finding outs for two overcards - should be exactly 6 outs."""
        # Hand: A♠ K♦, Board: Q♣ 7♥ 2♠
        # Any ace or king makes top pair - EXACTLY 6 outs (3 aces + 3 kings)
        hole_cards = self.engine.parse_cards(["As", "Kd"])
        community_cards = self.engine.parse_cards(["Qc", "7h", "2s"])
        
        outs = self.detector.find_outs(hole_cards, community_cards)
        
        # Should find EXACTLY 6 outs total
        assert len(outs) == 6, f"Expected 6 outs but found {len(outs)}"
        
        # Should find 3 aces and 3 kings
        ace_outs = [out for out in outs if out['card'][0] == 'A' and out['card'] != 'As']
        king_outs = [out for out in outs if out['card'][0] == 'K' and out['card'] != 'Kd']
        
        assert len(ace_outs) == 3, f"Expected 3 aces but found {len(ace_outs)}"
        assert len(king_outs) == 3, f"Expected 3 kings but found {len(king_outs)}"
        
        # All should be overcard draws
        for out in outs:
            assert out['draw_type'] == 'overcard'
    
    def test_find_outs_set_to_full_house(self):
        """Test finding outs for set to full house or quads - should be exactly 7 outs."""
        # Hand: K♠ K♣, Board: 8♥ K♦ 3♠
        # Current: Three kings
        # Outs: 8♠, 8♦, 8♣, 3♥, 3♦, 3♣ (full house), K♥ (quads) - EXACTLY 7 outs
        hole_cards = self.engine.parse_cards(["Ks", "Kc"])
        community_cards = self.engine.parse_cards(["8h", "Kd", "3s"])
        
        outs = self.detector.find_outs(hole_cards, community_cards)
        
        # Should find EXACTLY 7 outs total
        assert len(outs) == 7, f"Expected 7 outs but found {len(outs)}"
        
        # Check specific outs
        full_house_outs = [out for out in outs if out['draw_type'] == 'full_house']
        quads_outs = [out for out in outs if out['draw_type'] == 'four_of_a_kind']
        
        # 6 for full house (3 eights + 3 threes) + 1 for quads (1 king)
        assert len(full_house_outs) == 6, f"Expected 6 full house outs but found {len(full_house_outs)}"
        assert len(quads_outs) == 1, f"Expected 1 quads out but found {len(quads_outs)}"
    
    def test_find_outs_no_outs(self):
        """Test case with no improving outs - royal flush."""
        # Already have the nuts (royal flush)
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["Qs", "Js", "Ts"])  # Royal flush
        
        outs = self.detector.find_outs(hole_cards, community_cards)
        
        # Should find no outs (already have best possible hand)
        assert len(outs) == 0, f"Expected 0 outs but found {len(outs)}"
    
    
    def test_analyze_flush_draws(self):
        """Test detailed flush draw analysis."""
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["7s", "3s", "Jd"])
        
        flush_draws = self.detector._analyze_flush_draws(hole_cards, community_cards)
        
        # Should detect spade flush draw
        assert 's' in flush_draws, "Should detect spade flush draw"
        assert len(flush_draws['s']) == 9, f"Expected 9 spades but found {len(flush_draws['s'])}"  # 9 remaining spades
    
    def test_analyze_straight_draws(self):
        """Test detailed straight draw analysis."""
        hole_cards = self.engine.parse_cards(["9s", "8h"])
        community_cards = self.engine.parse_cards(["7c", "6d", "2s"])
        
        straight_draws = self.detector._analyze_straight_draws(hole_cards, community_cards)
        
        # Should detect ranks needed for straights
        assert 10 in straight_draws, "Should need 10 for 6-7-8-9-10 straight"
        assert 5 in straight_draws, "Should need 5 for 5-6-7-8-9 straight"
        
        # Should have exactly 2 ranks needed
        assert len(straight_draws) == 2, f"Expected 2 straight draw ranks but found {len(straight_draws)}"
    
    def test_get_pairing_outs(self):
        """Test pairing outs analysis for overcards."""
        hole_cards = self.engine.parse_cards(["As", "Kd"])
        community_cards = self.engine.parse_cards(["Qc", "7h", "2s"])
        
        pairing_outs = self.detector._get_pairing_outs(hole_cards, community_cards)
        
        # Should identify aces and kings as pairing outs (overcards)
        assert 14 in pairing_outs['pair'], "Aces should be overcard outs"
        assert 13 in pairing_outs['pair'], "Kings should be overcard outs"
    
    def test_get_detailed_outs_analysis(self):
        """Test comprehensive outs analysis for combo draw."""
        hole_cards = self.engine.parse_cards(["Js", "9s"])
        community_cards = self.engine.parse_cards(["Ts", "8c", "3s"])
        
        analysis = self.detector.get_detailed_outs_analysis(hole_cards, community_cards)
        
        # Should have comprehensive analysis structure
        assert 'flush_draws' in analysis
        assert 'straight_draws' in analysis
        assert 'pairing_outs' in analysis
        assert 'total_outs' in analysis
        assert 'unique_out_cards' in analysis
        assert 'outs_by_type' in analysis
        
        # Should detect both flush and straight draws
        assert 's' in analysis['flush_draws'], "Should detect spade flush draw"
        assert len(analysis['straight_draws']) > 0, "Should detect straight draw possibilities"
        
        # Total outs should be reasonable (combo draw typically 12-15 outs)
        assert analysis['total_outs'] > 0, "Should have some outs for this combo draw"
    
    def test_documented_examples(self):
        """Test all examples from outs.md documentation for exact counts."""
        
        # 4 outs: Inside straight draw (gutshot)
        # Hand: 9♠ 8♥, Board: 5♣ 6♦ K♠ -> Need 7 for straight
        hole_cards = self.engine.parse_cards(["9s", "8h"])
        community_cards = self.engine.parse_cards(["5c", "6d", "Ks"])
        outs = self.detector.find_outs(hole_cards, community_cards)
        assert len(outs) == 4, f"Gutshot should have 4 outs, found {len(outs)}"
        
        # 6 outs: Two overcards
        # Hand: A♠ K♦, Board: Q♣ 7♥ 2♠ -> Any ace or king makes top pair
        hole_cards = self.engine.parse_cards(["As", "Kd"])
        community_cards = self.engine.parse_cards(["Qc", "7h", "2s"])
        outs = self.detector.find_outs(hole_cards, community_cards)
        assert len(outs) == 6, f"Two overcards should have 6 outs, found {len(outs)}"
        
        # 8 outs: Open-ended straight draw
        # Hand: 9♠ 8♥, Board: 7♣ 6♦ 2♠ -> Need 10 or 5 for straight
        hole_cards = self.engine.parse_cards(["9s", "8h"])
        community_cards = self.engine.parse_cards(["7c", "6d", "2s"])
        outs = self.detector.find_outs(hole_cards, community_cards)
        assert len(outs) == 8, f"Open-ended straight should have 8 outs, found {len(outs)}"
        
        # 9 outs: Flush draw
        # Hand: A♠ K♠, Board: 7♠ 3♠ J♦ -> Any remaining spade completes flush
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["7s", "3s", "Jd"])
        outs = self.detector.find_outs(hole_cards, community_cards)
        assert len(outs) == 9, f"Flush draw should have 9 outs, found {len(outs)}"
    
    def test_count_outs_method(self):
        """Test the count_outs convenience method."""
        # Test with flush draw
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["7s", "3s", "Jd"])
        
        count = self.detector.count_outs(hole_cards, community_cards)
        outs_list = self.detector.find_outs(hole_cards, community_cards)
        
        assert count == len(outs_list), "count_outs should match find_outs length"
        assert count == 9, f"Expected 9 outs for flush draw, got {count}"
    
    def test_paired_board_fixes(self):
        """Test fixes for paired board issues - trips and two-pair outs."""
        
        # Test case: 8♠ J♠ vs T♥ 9♦ 9♣
        # Expected: 14 outs (8 straight + 6 two-pair, no trips)
        hole_cards = self.engine.parse_cards(["8s", "Js"])
        community_cards = self.engine.parse_cards(["Th", "9d", "9c"])
        
        outs = self.detector.find_outs(hole_cards, community_cards)
        
        # Should find exactly 14 outs total
        assert len(outs) == 14, f"Expected 14 outs but found {len(outs)}"
        
        # Group by draw type
        by_type = {}
        for out in outs:
            draw_type = out['draw_type']
            if draw_type not in by_type:
                by_type[draw_type] = []
            by_type[draw_type].append(out['card'])
        
        # Should have straight outs (8 total: 4 sevens + 4 queens)
        straight_outs = []
        for draw_type in ['straight', 'straight_gutshot', 'straight_open_ended']:
            if draw_type in by_type:
                straight_outs.extend(by_type[draw_type])
        
        assert len(straight_outs) == 8, f"Expected 8 straight outs but found {len(straight_outs)}"
        
        # Should have 4 sevens for 7-8-9-T-J straight
        sevens = [card for card in straight_outs if card[0] == '7']
        assert len(sevens) == 4, f"Expected 4 sevens but found {len(sevens)}"
        
        # Should have 4 queens for 8-9-T-J-Q straight
        queens = [card for card in straight_outs if card[0] == 'Q']
        assert len(queens) == 4, f"Expected 4 queens but found {len(queens)}"
        
        # Should have two-pair outs (6 total: 3 eights + 3 jacks)
        two_pair_outs = by_type.get('two_pair', [])
        assert len(two_pair_outs) == 6, f"Expected 6 two-pair outs but found {len(two_pair_outs)}"
        
        # Should have 3 eights (8h, 8d, 8c - not 8s which is in hand)
        eights = [card for card in two_pair_outs if card[0] == '8']
        assert len(eights) == 3, f"Expected 3 eights but found {len(eights)}"
        assert '8s' not in eights, "8s should not be an out (already in hand)"
        
        # Should have 3 jacks (Jh, Jd, Jc - not Js which is in hand)
        jacks = [card for card in two_pair_outs if card[0] == 'J']
        assert len(jacks) == 3, f"Expected 3 jacks but found {len(jacks)}"
        assert 'Js' not in jacks, "Js should not be an out (already in hand)"
        
        # Should NOT have trip 9 outs (9s, 9h) because board is paired
        trips_outs = by_type.get('three_of_a_kind', [])
        nines_trips = [card for card in trips_outs if card[0] == '9']
        assert len(nines_trips) == 0, f"Should not have trip 9 outs on paired board, found {nines_trips}"
    
    def test_trips_outs_on_unpaired_board(self):
        """Test that trips are still counted as outs when board is not paired."""
        
        # Test case: 8♠ 8♣ vs T♥ 9♦ 2♣ (pocket pair on unpaired board)
        # Expected: trips 8s should be counted as outs (likely to win)
        hole_cards = self.engine.parse_cards(["8s", "8c"])
        community_cards = self.engine.parse_cards(["Th", "9d", "2c"])
        
        outs = self.detector.find_outs(hole_cards, community_cards)
        
        # Group by draw type
        by_type = {}
        for out in outs:
            draw_type = out['draw_type']
            if draw_type not in by_type:
                by_type[draw_type] = []
            by_type[draw_type].append(out['card'])
        
        # Should have trip 8 outs since board is not paired
        trips_outs = by_type.get('three_of_a_kind', [])
        eights_trips = [card for card in trips_outs if card[0] == '8']
        assert len(eights_trips) == 2, f"Should have 2 trip 8 outs on unpaired board, found {len(eights_trips)}"
        
        # The specific cards should be 8h and 8d
        expected_eights = ['8h', '8d']
        for card in expected_eights:
            assert card in eights_trips, f"Expected {card} as trip out but not found"
    
    def test_two_pair_outs_simple_case(self):
        """Test two-pair outs detection with a simpler case."""
        
        # Test case: 8♥ J♣ vs 9♠ 9♦ K♠ (unpaired hole cards vs paired board)
        # Expected: 8 and J can pair to make two-pair (9s over 8s or 9s over Js)
        hole_cards = self.engine.parse_cards(["8h", "Jc"])
        community_cards = self.engine.parse_cards(["9s", "9d", "Ks"])
        
        outs = self.detector.find_outs(hole_cards, community_cards)
        
        # Group by draw type
        by_type = {}
        for out in outs:
            draw_type = out['draw_type']
            if draw_type not in by_type:
                by_type[draw_type] = []
            by_type[draw_type].append(out['card'])
        
        # Should have two-pair outs
        two_pair_outs = by_type.get('two_pair', [])
        
        # Should have 3 eights and 3 jacks (6 total)
        eights = [card for card in two_pair_outs if card[0] == '8']
        jacks = [card for card in two_pair_outs if card[0] == 'J']
        
        assert len(eights) == 3, f"Expected 3 eights for two-pair, found {len(eights)}"
        assert len(jacks) == 3, f"Expected 3 jacks for two-pair, found {len(jacks)}"
        
        # 8h already in hand, so should have 8s, 8d, 8c
        expected_eights = ['8s', '8d', '8c']
        for card in expected_eights:
            assert card in eights, f"Expected {card} as two-pair out"
        assert '8h' not in eights, "8h should not be an out (already in hand)"
        
        # Jc already in hand, so should have Js, Jh, Jd
        expected_jacks = ['Js', 'Jh', 'Jd']
        for card in expected_jacks:
            assert card in jacks, f"Expected {card} as two-pair out"
        assert 'Jc' not in jacks, "Jc should not be an out (already in hand)"
    
    def test_completed_straight_improvement_outs(self):
        """Test scenario where we already have a straight but can improve to better straight."""
        # Hand: J♠ 9♠, Board: T♥ Q♦ 8♦
        # Current: 8-9-T-J-Q straight (already completed)
        # Expected: Only 4 outs (4 Kings to make 9-T-J-Q-K straight)
        # Note: 7s would make 7-8-9-T-J straight but that's lower than current
        hole_cards = self.engine.parse_cards(["Js", "9s"])
        community_cards = self.engine.parse_cards(["Th", "Qd", "8d"])
        
        outs = self.detector.find_outs(hole_cards, community_cards)
        
        # Should find EXACTLY 4 outs (only the Kings)
        assert len(outs) == 4, f"Expected 4 outs but found {len(outs)}"
        
        # All outs should be Kings
        king_outs = [out for out in outs if out['card'][0] == 'K']
        assert len(king_outs) == 4, f"Expected 4 kings but found {len(king_outs)}"
        
        # Should NOT find Seven outs (they don't improve the hand)
        seven_outs = [out for out in outs if out['card'][0] == '7']
        assert len(seven_outs) == 0, f"Expected 0 sevens but found {len(seven_outs)}"
        
        # All outs should be straight draws
        for out in outs:
            assert 'straight' in out['draw_type']

    def test_completed_flush_improvement_outs(self):
        """Test that completed flushes can still improve with better flush cards."""
        # Test case 1: Hand: 5♠ 9♠, Board: K♠ 8♠ 3♠
        # Current: K-9-8-5-3 flush (already completed)
        # Expected: 7 outs for better flushes (4s, 6s, 7s, Ts, Js, Qs, As)
        # Note: 2s doesn't improve the flush since best 5 cards remain K-9-8-5-3
        hole_cards = self.engine.parse_cards(["5s", "9s"])
        community_cards = self.engine.parse_cards(["Ks", "8s", "3s"])
        
        outs = self.detector.find_outs(hole_cards, community_cards)
        
        # Should find exactly 7 outs (cards that actually improve the flush)
        assert len(outs) == 7, f"Expected 7 outs but found {len(outs)}"
        
        # All outs should be spades and flush improvements
        spade_outs = [out for out in outs if out['card'][1] == 's']
        assert len(spade_outs) == 7, f"Expected 7 spade outs but found {len(spade_outs)}"
        
        # All should be classified as flush
        for out in outs:
            assert out['draw_type'] == 'flush', f"Expected flush but found {out['draw_type']}"
        
        # Verify specific cards that should be outs
        found_cards = {out['card'] for out in outs}
        expected_improving_cards = {'4s', '6s', '7s', 'Ts', 'Js', 'Qs', 'As'}
        assert found_cards == expected_improving_cards, f"Expected {expected_improving_cards} but found {found_cards}"
        
        # Verify 2s is NOT an out (doesn't improve K-9-8-5-3 flush)
        assert '2s' not in found_cards, "2s should not be an out as it doesn't improve the flush"
        
        # Test case 2: Hand: T♠ 6♠, Board: 3♠ K♠ Q♠  
        # Current: K-Q-T-6-3 flush
        # Expected: 7 outs for better flushes
        hole_cards2 = self.engine.parse_cards(["Ts", "6s"])
        community_cards2 = self.engine.parse_cards(["3s", "Ks", "Qs"])
        
        outs2 = self.detector.find_outs(hole_cards2, community_cards2)
        
        # Should find exactly 7 outs
        assert len(outs2) == 7, f"Expected 7 outs for second case but found {len(outs2)}"
        
        # All should be spades and flush
        for out in outs2:
            assert out['card'][1] == 's', f"Expected spade but found {out['card']}"
            assert out['draw_type'] == 'flush'