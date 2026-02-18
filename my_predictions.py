#!/usr/bin/env python3
"""
Custom script for your daily betting predictions
Edit the matches list below with today's games
"""

from model import FootballPredictor
from betting_strategy import BettingStrategy, analyze_betting_conditions

# Load the model
print("📥 Loading model...\n")
predictor = FootballPredictor('data20202025.csv')
predictor.load_model('best_model.pth')

# Initialize betting strategy with your bankroll
strategy = BettingStrategy(predictor, initial_bankroll=1000)  # Change to your actual bankroll

print("="*70)
print("⚽ TODAY'S MATCH PREDICTIONS")
print("="*70)

# ==========================================
# EDIT THIS SECTION WITH TODAY'S MATCHES
# ==========================================
matches = [
    {
        'team1': 'Juventus',
        'team2': 'Milan', 
        'venue': 'Home',  # 'Home' or 'Away'
        'odds': {'win': 2.10, 'draw': 3.40, 'loss': 3.50}  # Get from your bookmaker
    },
    {
        'team1': 'Inter',
        'team2': 'Napoli',
        'venue': 'Home',
        'odds': {'win': 1.85, 'draw': 3.60, 'loss': 4.20}
    },
    # Add more matches here...
]

# Process each match
recommendations = []

for i, match in enumerate(matches, 1):
    print(f"\n{'='*70}")
    print(f"MATCH {i}: {match['team1']} vs {match['team2']} ({match['venue']})")
    print(f"{'='*70}")
    
    # Get prediction
    prediction = predictor.predict(
        match['team1'], 
        match['team2'], 
        match['venue'],
        use_neural_network=True
    )
    
    print(f"\n📊 Model Prediction:")
    print(f"   {match['team1']} Win: {prediction['win']*100:.1f}%")
    print(f"   Draw: {prediction['draw']*100:.1f}%")
    print(f"   {match['team2']} Win: {prediction['loss']*100:.1f}%")
    print(f"   Confidence: {prediction['confidence']*100:.1f}%")
    
    print(f"\n💰 Bookmaker Odds: Win={match['odds']['win']}, Draw={match['odds']['draw']}, Loss={match['odds']['loss']}")
    
    # Get betting recommendation
    recommendation = strategy.evaluate_match(
        match['team1'],
        match['team2'],
        match['venue'],
        match['odds'],
        min_confidence=0.65,  # Adjust these thresholds
        min_edge=0.08
    )
    
    # Show recommendation
    if recommendation['should_bet']:
        details = recommendation['bet_details']
        outcome_name = match['team1'] if details['outcome'] == 'win' else (
            match['team2'] if details['outcome'] == 'loss' else 'Draw'
        )
        
        print(f"\n✅ RECOMMENDED BET: {outcome_name}")
        print(f"   Stake: ${details['stake_amount']:.2f} ({details['stake_pct']*100:.2f}% of bankroll)")
        print(f"   Odds: {details['odds']:.2f}")
        print(f"   Expected Value: {details['expected_value']*100:+.2f}%")
        print(f"   Edge: {details['edge']*100:+.2f}%")
        
        recommendations.append({
            'match': f"{match['team1']} vs {match['team2']}",
            'bet': outcome_name,
            'stake': details['stake_amount'],
            'odds': details['odds'],
            'ev': details['expected_value']
        })
    else:
        print(f"\n❌ NO BET RECOMMENDED")
        print(f"   Reason: {recommendation['reason']}")

# Summary
print(f"\n{'='*70}")
print(f"📋 BETTING SUMMARY")
print(f"{'='*70}")

if recommendations:
    print(f"\n✅ {len(recommendations)} bet(s) recommended:\n")
    total_stake = 0
    for rec in recommendations:
        print(f"   • {rec['match']}")
        print(f"     Bet: {rec['bet']} @ {rec['odds']:.2f}")
        print(f"     Stake: ${rec['stake']:.2f} | EV: {rec['ev']*100:+.2f}%")
        total_stake += rec['stake']
    
    print(f"\n   💵 Total stake: ${total_stake:.2f}")
    print(f"   💰 Remaining bankroll: ${strategy.current_bankroll - total_stake:.2f}")
else:
    print(f"\n⚠️ No value bets found today.")
    print(f"   Tips:")
    print(f"   - Shop for better odds at different bookmakers")
    print(f"   - Wait for more favorable matches")
    print(f"   - Lower min_confidence or min_edge thresholds (if comfortable with risk)")

print(f"\n{'='*70}\n")

# Optional: For detailed analysis of a specific match
print("💡 For detailed analysis of any match, uncomment below:\n")
print("# analyze_betting_conditions(predictor, 'Juventus', 'Milan', 'Home')")
