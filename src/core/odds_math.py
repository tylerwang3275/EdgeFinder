"""
Odds conversion utilities for sports betting and prediction markets.
"""

from typing import List, Tuple
import math


def american_to_implied_probability(american_odds: int) -> float:
    """
    Convert American odds to implied probability.
    
    Args:
        american_odds: American odds (positive or negative integer)
        
    Returns:
        Implied probability as float between 0 and 1
    """
    if american_odds > 0:
        return 100 / (american_odds + 100)
    else:
        return (-american_odds) / ((-american_odds) + 100)


def decimal_to_implied_probability(decimal_odds: float) -> float:
    """
    Convert decimal odds to implied probability.
    
    Args:
        decimal_odds: Decimal odds (e.g., 2.5 for +150 American)
        
    Returns:
        Implied probability as float between 0 and 1
    """
    return 1 / decimal_odds


def implied_probability_to_american(probability: float) -> int:
    """
    Convert implied probability to American odds.
    
    Args:
        probability: Implied probability (0-1)
        
    Returns:
        American odds as integer
    """
    if probability >= 0.5:
        return int(-100 * probability / (1 - probability))
    else:
        return int(100 * (1 - probability) / probability)


def implied_probability_to_decimal(probability: float) -> float:
    """
    Convert implied probability to decimal odds.
    
    Args:
        probability: Implied probability (0-1)
        
    Returns:
        Decimal odds
    """
    return 1 / probability


def remove_vig(probabilities: List[float]) -> List[float]:
    """
    Remove vig (overround) from a set of probabilities.
    
    Args:
        probabilities: List of implied probabilities
        
    Returns:
        List of de-vigged probabilities that sum to 1.0
    """
    total_prob = sum(probabilities)
    if total_prob <= 0:
        return probabilities
    
    return [p / total_prob for p in probabilities]


def calculate_payout_ratio(probability: float) -> float:
    """
    Calculate payout ratio for a given probability.
    
    Args:
        probability: Implied probability (0-1)
        
    Returns:
        Payout ratio (e.g., 3.0 for 3:1 payout)
    """
    if probability <= 0 or probability >= 1:
        return 0.0
    return (1 - probability) / probability


def calculate_discrepancy(prediction_prob: float, book_prob: float) -> float:
    """
    Calculate absolute discrepancy between prediction and book probability.
    
    Args:
        prediction_prob: Prediction market implied probability
        book_prob: Sportsbook implied probability
        
    Returns:
        Absolute discrepancy (0-1)
    """
    return abs(prediction_prob - book_prob)


def calculate_edge_vs_best(prediction_prob: float, book_probs: List[float]) -> Tuple[float, float, float]:
    """
    Calculate edge vs best available book odds.
    
    Args:
        prediction_prob: Prediction market implied probability
        book_probs: List of sportsbook implied probabilities
        
    Returns:
        Tuple of (min_book_prob, avg_book_prob, max_book_prob)
    """
    if not book_probs:
        return 0.0, 0.0, 0.0
    
    min_prob = min(book_probs)
    max_prob = max(book_probs)
    avg_prob = sum(book_probs) / len(book_probs)
    
    return min_prob, avg_prob, max_prob


def calculate_expected_value(prediction_prob: float, book_prob: float, stake: float = 1.0) -> float:
    """
    Calculate expected value of a bet.
    
    Args:
        prediction_prob: True probability (from prediction market)
        book_prob: Book implied probability
        stake: Bet amount
        
    Returns:
        Expected value
    """
    if book_prob <= 0 or book_prob >= 1:
        return 0.0
    
    payout = stake * (1 / book_prob - 1)
    win_prob = prediction_prob
    lose_prob = 1 - prediction_prob
    
    return (win_prob * payout) - (lose_prob * stake)
