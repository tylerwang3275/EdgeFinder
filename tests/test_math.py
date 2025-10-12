"""
Tests for odds math utilities.
"""

import pytest
from src.core.odds_math import (
    american_to_implied_probability,
    decimal_to_implied_probability,
    implied_probability_to_american,
    implied_probability_to_decimal,
    remove_vig,
    calculate_payout_ratio,
    calculate_discrepancy,
    calculate_edge_vs_best,
    calculate_expected_value
)


class TestOddsMath:
    """Test odds conversion functions."""
    
    def test_american_to_implied_probability_positive(self):
        """Test positive American odds conversion."""
        # +150 should be 100/(150+100) = 0.4
        assert american_to_implied_probability(150) == pytest.approx(0.4, rel=1e-3)
        
        # +200 should be 100/(200+100) = 0.333
        assert american_to_implied_probability(200) == pytest.approx(0.333333, rel=1e-3)
    
    def test_american_to_implied_probability_negative(self):
        """Test negative American odds conversion."""
        # -150 should be 150/(150+100) = 0.6
        assert american_to_implied_probability(-150) == pytest.approx(0.6, rel=1e-3)
        
        # -200 should be 200/(200+100) = 0.667
        assert american_to_implied_probability(-200) == pytest.approx(0.667, rel=1e-3)
    
    def test_decimal_to_implied_probability(self):
        """Test decimal odds conversion."""
        # 2.5 decimal should be 1/2.5 = 0.4
        assert decimal_to_implied_probability(2.5) == pytest.approx(0.4, rel=1e-3)
        
        # 3.0 decimal should be 1/3.0 = 0.333
        assert decimal_to_implied_probability(3.0) == pytest.approx(0.333333, rel=1e-3)
    
    def test_implied_probability_to_american(self):
        """Test probability to American odds conversion."""
        # 0.4 should be +150
        assert implied_probability_to_american(0.4) == 150
        
        # 0.6 should be -150
        assert implied_probability_to_american(0.6) == -150
    
    def test_implied_probability_to_decimal(self):
        """Test probability to decimal odds conversion."""
        # 0.4 should be 2.5
        assert implied_probability_to_decimal(0.4) == pytest.approx(2.5, rel=1e-3)
        
        # 0.333 should be 3.0
        assert implied_probability_to_decimal(0.333333) == pytest.approx(3.0, rel=1e-3)
    
    def test_remove_vig(self):
        """Test vig removal."""
        # Two outcomes with 5% vig
        probs = [0.52, 0.48]  # Total 1.0 (no vig)
        de_vigged = remove_vig(probs)
        assert sum(de_vigged) == pytest.approx(1.0, rel=1e-3)
        assert de_vigged[0] == pytest.approx(0.52, rel=1e-3)
        assert de_vigged[1] == pytest.approx(0.48, rel=1e-3)
        
        # Two outcomes with vig
        probs_with_vig = [0.55, 0.50]  # Total 1.05 (5% vig)
        de_vigged = remove_vig(probs_with_vig)
        assert sum(de_vigged) == pytest.approx(1.0, rel=1e-3)
        assert de_vigged[0] == pytest.approx(0.524, rel=1e-2)
        assert de_vigged[1] == pytest.approx(0.476, rel=1e-2)
    
    def test_calculate_payout_ratio(self):
        """Test payout ratio calculation."""
        # 0.4 probability should give 1.5x payout
        assert calculate_payout_ratio(0.4) == pytest.approx(1.5, rel=1e-3)
        
        # 0.25 probability should give 3.0x payout
        assert calculate_payout_ratio(0.25) == pytest.approx(3.0, rel=1e-3)
    
    def test_calculate_discrepancy(self):
        """Test discrepancy calculation."""
        # 0.6 vs 0.5 should be 0.1
        assert calculate_discrepancy(0.6, 0.5) == pytest.approx(0.1, rel=1e-3)
        
        # 0.4 vs 0.5 should be 0.1 (absolute)
        assert calculate_discrepancy(0.4, 0.5) == pytest.approx(0.1, rel=1e-3)
    
    def test_calculate_edge_vs_best(self):
        """Test edge vs best calculation."""
        book_probs = [0.45, 0.50, 0.55]
        min_prob, avg_prob, max_prob = calculate_edge_vs_best(0.6, book_probs)
        
        assert min_prob == 0.45
        assert avg_prob == 0.50
        assert max_prob == 0.55
    
    def test_calculate_expected_value(self):
        """Test expected value calculation."""
        # True prob 0.6, book prob 0.5, stake 1.0
        # EV = (0.6 * 1.0) - (0.4 * 1.0) = 0.2
        ev = calculate_expected_value(0.6, 0.5, 1.0)
        assert ev == pytest.approx(0.2, rel=1e-3)
        
        # True prob 0.4, book prob 0.5, stake 1.0
        # EV = (0.4 * 1.0) - (0.6 * 1.0) = -0.2
        ev = calculate_expected_value(0.4, 0.5, 1.0)
        assert ev == pytest.approx(-0.2, rel=1e-3)
