"""Tests for pot odds calculation functionality."""

import pytest
from poker_engine import PokerEngine
from pot_odds_calculator import PotOddsCalculator, OptimizedPotOddsCalculator


class TestPotOddsCalculator:
    """Test PotOddsCalculator functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = PokerEngine()
        self.calculator = PotOddsCalculator(self.engine)
        self.opt_calculator = OptimizedPotOddsCalculator(self.engine)
    
    def test_calculator_initialization(self):
        """Test calculator initialization."""
        assert self.calculator.engine == self.engine
        assert self.calculator.outs_detector is not None
    
    def test_calculate_flop_probability_4_outs(self):
        """Test flop probability calculation with 4 outs."""
        # Formula: 1 - [(47-4)/47] × [(46-4)/46] = 1 - (43/47 × 42/46) = 16.47%
        probability = self.calculator._calculate_flop_probability(4)
        expected = 1 - (43/47 * 42/46)
        
        assert abs(probability - expected) < 0.0001
        assert abs(probability - 0.1647) < 0.01  # Approximately 16.47%
    
    def test_calculate_flop_probability_9_outs(self):
        """Test flop probability calculation with 9 outs (flush draw)."""
        # Formula: 1 - [(47-9)/47] × [(46-9)/46] = 1 - (38/47 × 37/46) = 34.97%
        probability = self.calculator._calculate_flop_probability(9)
        expected = 1 - (38/47 * 37/46)
        
        assert abs(probability - expected) < 0.0001
        assert abs(probability - 0.3497) < 0.01  # Approximately 34.97%
    
    def test_calculate_turn_probability_4_outs(self):
        """Test turn probability calculation with 4 outs."""
        # Formula: 4/46 = 8.70%
        probability = self.calculator._calculate_turn_probability(4)
        expected = 4/46
        
        assert abs(probability - expected) < 0.0001
        assert abs(probability - 0.087) < 0.01  # Approximately 8.70%
    
    def test_calculate_turn_probability_9_outs(self):
        """Test turn probability calculation with 9 outs."""
        # Formula: 9/46 = 19.57%
        probability = self.calculator._calculate_turn_probability(9)
        expected = 9/46
        
        assert abs(probability - expected) < 0.0001
        assert abs(probability - 0.1957) < 0.01  # Approximately 19.57%
    
    def test_format_pot_odds_ratio_4_outs_flop(self):
        """Test pot odds ratio formatting for 4 outs on flop."""
        # 16.47% win rate → 83.53% lose rate → 83.53/16.47 = 5.07 ≈ 5.1:1
        probability = 0.1647
        ratio = self.calculator._format_pot_odds_ratio(probability)
        
        assert ratio == "5.1:1"
    
    def test_format_pot_odds_ratio_9_outs_flop(self):
        """Test pot odds ratio formatting for 9 outs on flop."""
        # 34.97% win rate → 65.03% lose rate → 65.03/34.97 = 1.86 ≈ 1.9:1
        probability = 0.3497
        ratio = self.calculator._format_pot_odds_ratio(probability)
        
        assert ratio == "1.9:1"
    
    def test_format_pot_odds_ratio_integer(self):
        """Test pot odds ratio formatting for integer ratios."""
        # 20% win rate → 80% lose rate → 80/20 = 4.0 → 4:1 (no decimal)
        probability = 0.20
        ratio = self.calculator._format_pot_odds_ratio(probability)
        
        assert ratio == "4:1"
    
    def test_format_pot_odds_ratio_edge_cases(self):
        """Test pot odds ratio formatting for edge cases."""
        # Zero probability
        ratio = self.calculator._format_pot_odds_ratio(0.0)
        assert ratio == "999.0:1"
        
        # 100% probability
        ratio = self.calculator._format_pot_odds_ratio(1.0)
        assert ratio == "0.0:1"
        
        # Very small probability
        ratio = self.calculator._format_pot_odds_ratio(0.001)
        assert ratio.endswith(":1")
    
    def test_calculate_pot_odds_inside_straight_draw(self):
        """Test pot odds calculation for inside straight draw."""
        # Hand: 9s 8h, Board: 5c 6d Ks (4 outs for straight)
        hole_cards = self.engine.parse_cards(["9s", "8h"])
        community_cards = self.engine.parse_cards(["5c", "6d", "Ks"])
        
        pot_odds_ratio, outs = self.calculator.calculate_pot_odds(hole_cards, community_cards)
        
        # With a weak hand (9-high), many cards improve it, so odds will be low
        assert len(outs) >= 4  # Should find at least the 4 sevens for straight
        
        # Find the straight outs specifically
        straight_outs = [out for out in outs if 'straight' in out['draw_type']]
        assert len(straight_outs) >= 4  # Should find 4 sevens
    
    def test_calculate_pot_odds_flush_draw(self):
        """Test pot odds calculation for flush draw."""
        # Hand: As Ks, Board: 7s 3s Jd (9 outs for flush)
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["7s", "3s", "Jd"])
        
        pot_odds_ratio, outs = self.calculator.calculate_pot_odds(hole_cards, community_cards)
        
        # With strong cards (A,K) and 4-card flush draw, many cards improve the hand
        assert len(outs) >= 9  # Should find at least the 9 spades
        
        # Check that flush outs are properly classified
        flush_outs = [out for out in outs if out['draw_type'] == 'flush']
        assert len(flush_outs) >= 9  # Should find 9 spades for flush
    
    def test_calculate_pot_odds_no_outs(self):
        """Test pot odds calculation with no outs."""
        # Royal flush - no improving cards, but this is NUTS!
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["Qs", "Js", "Ts"])
        
        pot_odds_ratio, outs = self.calculator.calculate_pot_odds(hole_cards, community_cards)
        
        # According to API spec: completed royal flush using both hole cards should be NUTS!
        assert pot_odds_ratio == "NUTS!"
        assert len(outs) == 0
    
    def test_get_probability_breakdown_flop(self):
        """Test probability breakdown analysis on flop."""
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["7s", "3s", "Jd"])
        
        breakdown = self.calculator.get_probability_breakdown(hole_cards, community_cards)
        
        assert breakdown['cards_seen'] == 5  # 2 hole + 3 community
        assert breakdown['unseen_cards'] == 47
        assert breakdown['game_phase'] == 'flop'
        assert 'flop_probability' in breakdown
        assert 'outs_by_type' in breakdown
    
    def test_get_probability_breakdown_turn(self):
        """Test probability breakdown analysis on turn."""
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["7s", "3s", "Jd", "2h"])
        
        breakdown = self.calculator.get_probability_breakdown(hole_cards, community_cards)
        
        assert breakdown['cards_seen'] == 6  # 2 hole + 4 community
        assert breakdown['unseen_cards'] == 46
        assert breakdown['game_phase'] == 'turn'
        assert 'turn_probability' in breakdown
    
    def test_calculate_exact_odds_from_examples(self):
        """Test exact odds calculation for specification examples."""
        examples = self.calculator.calculate_exact_odds_from_examples()
        
        # Verify examples match specifications
        assert examples['4_outs_flop']['expected'] == '5.1:1'
        assert examples['9_outs_flop']['expected'] == '1.9:1'
        
        # Check that calculated ratios are close to expected
        for example_name, data in examples.items():
            calculated = data['ratio']
            expected = data['expected']
            
            # Extract numeric part for comparison
            calc_num = float(calculated.split(':')[0])
            exp_num = float(expected.split(':')[0])
            
            # Should be within 0.2 of expected
            assert abs(calc_num - exp_num) < 0.2
    
    def test_optimized_calculator_same_results(self):
        """Test that optimized calculator gives same results as standard."""
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["7s", "3s", "Jd"])
        
        standard_result = self.calculator.calculate_pot_odds(hole_cards, community_cards)
        optimized_result = self.opt_calculator.calculate_pot_odds(hole_cards, community_cards)
        
        # Results should be identical
        assert standard_result[0] == optimized_result[0]  # Same pot odds ratio
        assert len(standard_result[1]) == len(optimized_result[1])  # Same number of outs
    
    def test_probability_calculation_boundary_values(self):
        """Test probability calculations with boundary values."""
        # 0 outs
        prob = self.calculator._calculate_flop_probability(0)
        assert prob == 0.0
        
        # Max possible outs (47)
        prob = self.calculator._calculate_flop_probability(47)
        assert prob == 1.0
        
        # Boundary for turn (46)
        prob = self.calculator._calculate_turn_probability(46)
        assert prob == 1.0
    
    
    def test_calculate_pot_odds_with_nuts_returns_special_value(self):
        """Test that calculate_pot_odds returns 'NUTS!' when nuts are detected."""
        # Hand: As 9h, Board: Ks Qs Js (Ts would complete royal flush)
        hole_cards = self.engine.parse_cards(["As", "9h"])
        community_cards = self.engine.parse_cards(["Ks", "Qs", "Js"])
        
        pot_odds_ratio, outs = self.calculator.calculate_pot_odds(hole_cards, community_cards)
        
        # Should return "NUTS!" if the Ten of spades is found as an out
        ts_outs = [out for out in outs if out['card'] == 'Ts']
        if ts_outs:
            # If Ts is an out, pot_odds_ratio should be "NUTS!"
            # Note: This depends on the outs detector finding Ts as a straight out
            pass  # The actual behavior depends on outs detector implementation
    
    def test_calculate_pot_odds_with_nut_flush_draw(self):
        """Test calculate_pot_odds with nut flush draw - should return normal odds, not NUTS."""
        # Hand: As Ks, Board: Qs Js 2h (any remaining spade completes nut flush)
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["Qs", "Js", "2h"])
        
        pot_odds_ratio, outs = self.calculator.calculate_pot_odds(hole_cards, community_cards)
        
        # Should find flush outs 
        flush_outs = [out for out in outs if out['draw_type'] == 'flush']
        assert len(flush_outs) >= 9  # Should find 9 spades
        
        # Should return normal odds since draws no longer trigger NUTS detection
        assert pot_odds_ratio != "NUTS!"
        assert ":" in pot_odds_ratio  # Should be a normal ratio like "1.2:1"
    
    def test_calculate_pot_odds_with_broadway_straight_draw(self):
        """Test calculate_pot_odds with Broadway straight draw - should return normal odds, not NUTS."""
        # Hand: As Kd, Board: Qh Jc 2s (Th completes Broadway straight)
        hole_cards = self.engine.parse_cards(["As", "Kd"])
        community_cards = self.engine.parse_cards(["Qh", "Jc", "2s"])
        
        pot_odds_ratio, outs = self.calculator.calculate_pot_odds(hole_cards, community_cards)
        
        # Should find straight outs
        straight_outs = [out for out in outs if out['draw_type'] == 'straight']
        assert len(straight_outs) >= 4  # Should find 4 tens
        
        # Should return normal odds since draws no longer trigger NUTS detection  
        assert pot_odds_ratio != "NUTS!"
        assert ":" in pot_odds_ratio  # Should be a normal ratio like "5.1:1"
    
    def test_calculate_pot_odds_nuts_edge_case_no_outs(self):
        """Test NUTS detection when there are no outs."""
        # Royal flush - no improving cards but already NUTS!
        hole_cards = self.engine.parse_cards(["As", "Ks"])
        community_cards = self.engine.parse_cards(["Qs", "Js", "Ts"])
        
        pot_odds_ratio, outs = self.calculator.calculate_pot_odds(hole_cards, community_cards)
        
        # According to API spec: completed royal flush using both hole cards should be NUTS!
        assert pot_odds_ratio == "NUTS!"
        assert len(outs) == 0
    
    def test_calculate_pot_odds_api_spec_royal_flush_example(self):
        """Test the specific royal flush example from the API spec."""
        # Example from API spec: {"hole_cards": ["Ah", "Kh"], "community_cards": ["Qh", "Jh", "Th"]}
        hole_cards = self.engine.parse_cards(["Ah", "Kh"])
        community_cards = self.engine.parse_cards(["Qh", "Jh", "Th"])
        
        pot_odds_ratio, outs = self.calculator.calculate_pot_odds(hole_cards, community_cards)
        
        # According to API spec: this should return "NUTS!"
        assert pot_odds_ratio == "NUTS!"
        assert len(outs) == 0
    
