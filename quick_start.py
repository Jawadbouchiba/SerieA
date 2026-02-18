#!/usr/bin/env python3
"""
Quick Start Example for Sports Betting Model
Run this to see a complete betting workflow
"""

from model import FootballPredictor
from betting_strategy import BettingStrategy, analyze_betting_conditions


def main():
    print("\n" + "="*70)
    print("⚽ SPORTS BETTING MODEL - QUICK START GUIDE")
    print("="*70)
    
    # Step 1: Load the model
    print("\n📥 Step 1: Loading trained model...")
    predictor = FootballPredictor('data20202025.csv')
    predictor.load_model('best_model.pth')
    print("✅ Model loaded successfully!")
    
    # Step 2: Get teams
    teams = predictor.get_all_teams()
    print(f"✅ Found {len(teams)} teams")
    
    # Example match
    if "Juventus" in teams and "Milan" in teams:
        team1, team2 = "Juventus", "Milan"
    else:
        team1, team2 = teams[0], teams[1]
    venue = "Home"
    
    print(f"\n{'='*70}")
    print(f"🎯 Example Match: {team1} vs {team2} ({venue})")
    print(f"{'='*70}")
    
    # Step 3: Deep analysis
    print("\n📊 Step 2: Analyzing match conditions...")
    analyze_betting_conditions(predictor, team1, team2, venue)
    
    # Step 4: Get prediction with confidence
    print("\n🔮 Step 3: Getting model prediction...")
    prediction = predictor.predict(team1, team2, venue, use_neural_network=True)
    
    print(f"\n📈 Prediction Results:")
    print(f"   {team1} Win: {prediction['win']*100:.1f}%")
    print(f"   Draw: {prediction['draw']*100:.1f}%")
    print(f"   {team2} Win: {prediction['loss']*100:.1f}%")
    print(f"   Confidence: {prediction['confidence']*100:.1f}%")
    
    # Step 5: Simulate bookmaker odds
    print("\n💰 Step 4: Checking betting value...")
    
    # Example odds (you would get these from your bookmaker)
    bookmaker_odds = {
        'win': 2.10,   # Odds for team1 to win
        'draw': 3.40,  # Odds for draw
        'loss': 3.50   # Odds for team2 to win
    }
    
    print(f"\n📊 Bookmaker Odds:")
    print(f"   {team1} Win: {bookmaker_odds['win']:.2f}")
    print(f"   Draw: {bookmaker_odds['draw']:.2f}")
    print(f"   {team2} Win: {bookmaker_odds['loss']:.2f}")
    
    # Step 6: Betting value analysis
    betting_analysis = predictor.calculate_betting_value(prediction, bookmaker_odds)
    
    print(f"\n💡 Betting Value Analysis:")
    for outcome, data in betting_analysis['outcomes'].items():
        outcome_name = team1 if outcome == 'win' else (team2 if outcome == 'loss' else 'Draw')
        
        if data['bet']:
            print(f"\n   ✅ {outcome_name}:")
            print(f"      Expected Value: {data['expected_value']*100:+.2f}%")
            print(f"      Edge over bookmaker: {data['edge']*100:+.2f}%")
            print(f"      Recommended stake: {data['kelly_stake']*100:.2f}% of bankroll")
            print(f"      Model prob: {data['model_prob']*100:.1f}% vs Implied prob: {data['implied_prob']*100:.1f}%")
        else:
            print(f"\n   ❌ {outcome_name}: No value (EV: {data['expected_value']*100:+.2f}%)")
    
    # Step 7: Final recommendation
    should_bet, reason = predictor.should_bet(
        prediction, 
        bookmaker_odds, 
        min_confidence=0.65,
        min_edge=0.08
    )
    
    print(f"\n{'='*70}")
    print(f"🎲 BETTING RECOMMENDATION")
    print(f"{'='*70}")
    
    if should_bet:
        best_bet = betting_analysis['best_bet']
        best_data = betting_analysis['outcomes'][best_bet]
        outcome_name = team1 if best_bet == 'win' else (team2 if best_bet == 'loss' else 'Draw')
        
        print(f"\n✅ RECOMMENDED BET: {outcome_name}")
        print(f"\n📋 Bet Details:")
        print(f"   Outcome: {outcome_name}")
        print(f"   Odds: {bookmaker_odds[best_bet]:.2f}")
        print(f"   Expected Value: {best_data['expected_value']*100:+.2f}%")
        print(f"   Edge: {best_data['edge']*100:+.2f}%")
        print(f"   Stake: {best_data['kelly_stake']*100:.2f}% of your bankroll")
        
        print(f"\n💡 Example with $1000 bankroll:")
        stake_amount = 1000 * best_data['kelly_stake']
        potential_profit = stake_amount * (bookmaker_odds[best_bet] - 1)
        print(f"   Stake: ${stake_amount:.2f}")
        print(f"   Potential profit: ${potential_profit:.2f}")
        print(f"   Potential return: ${stake_amount + potential_profit:.2f}")
        
    else:
        print(f"\n❌ NO BET RECOMMENDED")
        print(f"\n📋 Reason: {reason}")
        print(f"\n💡 Why not to bet:")
        print(f"   - Look for better odds from other bookmakers")
        print(f"   - Wait for more favorable matches")
        print(f"   - The expected value is not high enough")
    
    # Step 8: Show strategy tracking
    print(f"\n{'='*70}")
    print(f"📊 BANKROLL MANAGEMENT EXAMPLE")
    print(f"{'='*70}")
    
    strategy = BettingStrategy(predictor, initial_bankroll=1000)
    
    print(f"\n💰 Starting Bankroll: $1000.00")
    print(f"\n🎯 Strategy Parameters:")
    print(f"   - Minimum Confidence: 65%")
    print(f"   - Minimum Edge: 8%")
    print(f"   - Maximum Stake per Bet: 5%")
    print(f"   - Fractional Kelly: 25% (conservative)")
    
    recommendation = strategy.evaluate_match(team1, team2, venue, bookmaker_odds)
    
    if recommendation['should_bet']:
        details = recommendation['bet_details']
        print(f"\n✅ This bet meets all criteria:")
        print(f"   Confidence: {prediction['confidence']*100:.1f}% ≥ 65% ✓")
        print(f"   Edge: {details['edge']*100:.1f}% ≥ 8% ✓")
        print(f"   EV: {details['expected_value']*100:.1f}% > 5% ✓")
        print(f"   Stake: {details['stake_pct']*100:.2f}% ≤ 5% ✓")
    
    print(f"\n{'='*70}")
    print(f"📚 NEXT STEPS")
    print(f"{'='*70}")
    print(f"""
1. 📖 Read BETTING_GUIDE.md for detailed information
2. 🧪 Run test_betting_model.py to validate everything works
3. 📊 Paper trade for 50+ matches to test strategy
4. 💰 Start with small stakes (1-2% of bankroll)
5. 📈 Track performance using BettingStrategy class
6. ⚖️ Adjust parameters based on results

⚠️  IMPORTANT WARNINGS:
   - Never bet more than you can afford to lose
   - Don't chase losses
   - Follow Kelly Criterion strictly
   - Track at least 100 bets before judging strategy
   - Update model regularly with new data
   - Past performance doesn't guarantee future results
   - Sports betting involves risk - bet responsibly
    """)
    
    print(f"{'='*70}\n")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print(f"\n💡 Make sure to:")
        print(f"   1. Train the model first: python3 train_model.py")
        print(f"   2. Ensure best_model.pth exists")
        print(f"   3. Check data20202025.csv is in the current directory\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
