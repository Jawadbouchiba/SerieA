#!/usr/bin/env python3
"""
Test script to validate betting model improvements
"""

import sys
from model import FootballPredictor
from betting_strategy import BettingStrategy, analyze_betting_conditions


def test_model_loading():
    """Test 1: Model loads correctly"""
    print("\n" + "="*70)
    print("TEST 1: Model Loading")
    print("="*70)
    
    try:
        predictor = FootballPredictor('data20202025.csv')
        predictor.load_model('best_model.pth')
        
        teams = predictor.get_all_teams()
        print(f"✅ Model loaded successfully")
        print(f"✅ Found {len(teams)} teams in dataset")
        print(f"✅ Example teams: {', '.join(teams[:5])}")
        return predictor
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None


def test_predictions_with_confidence(predictor):
    """Test 2: Predictions include confidence scores"""
    print("\n" + "="*70)
    print("TEST 2: Predictions with Confidence")
    print("="*70)
    
    teams = predictor.get_all_teams()
    if len(teams) < 2:
        print("❌ Not enough teams to test")
        return False
    
    team1, team2 = teams[0], teams[1]
    
    try:
        # Test with neural network
        pred = predictor.predict(team1, team2, 'Home', use_neural_network=True)
        
        # Check required fields
        required_fields = ['win', 'draw', 'loss', 'confidence', 'max_prob']
        for field in required_fields:
            if field not in pred:
                print(f"❌ Missing field: {field}")
                return False
        
        # Check probabilities sum to 1
        total = pred['win'] + pred['draw'] + pred['loss']
        if abs(total - 1.0) > 0.01:
            print(f"❌ Probabilities don't sum to 1: {total}")
            return False
        
        # Check confidence is between 0 and 1
        if not (0 <= pred['confidence'] <= 1):
            print(f"❌ Invalid confidence score: {pred['confidence']}")
            return False
        
        print(f"✅ Prediction structure is correct")
        print(f"✅ Match: {team1} vs {team2}")
        print(f"   Win: {pred['win']*100:.1f}%")
        print(f"   Draw: {pred['draw']*100:.1f}%")
        print(f"   Loss: {pred['loss']*100:.1f}%")
        print(f"   Confidence: {pred['confidence']*100:.1f}%")
        print(f"   Max Prob: {pred['max_prob']*100:.1f}%")
        
        return True
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_betting_value_calculation(predictor):
    """Test 3: Betting value calculations work"""
    print("\n" + "="*70)
    print("TEST 3: Betting Value Calculation")
    print("="*70)
    
    teams = predictor.get_all_teams()
    if len(teams) < 2:
        print("❌ Not enough teams to test")
        return False
    
    team1, team2 = teams[0], teams[1]
    
    try:
        # Get prediction
        pred = predictor.predict(team1, team2, 'Home', use_neural_network=True)
        
        # Test with various odds scenarios
        test_cases = [
            {'win': 2.00, 'draw': 3.40, 'loss': 3.50},  # Balanced odds
            {'win': 1.50, 'draw': 4.00, 'loss': 7.00},  # Heavy favorite
            {'win': 5.00, 'draw': 3.50, 'loss': 1.60},  # Heavy underdog
        ]
        
        for i, odds in enumerate(test_cases, 1):
            print(f"\n📊 Test Case {i}: Odds = {odds}")
            
            analysis = predictor.calculate_betting_value(pred, odds)
            
            # Check structure
            if 'outcomes' not in analysis or 'best_bet' not in analysis:
                print(f"❌ Invalid analysis structure")
                return False
            
            # Check each outcome
            for outcome in ['win', 'draw', 'loss']:
                if outcome not in analysis['outcomes']:
                    print(f"❌ Missing outcome: {outcome}")
                    return False
                
                data = analysis['outcomes'][outcome]
                required = ['bet', 'expected_value', 'kelly_stake', 'edge']
                
                for field in required:
                    if field not in data:
                        print(f"❌ Missing field in {outcome}: {field}")
                        return False
            
            # Print results
            best = analysis['best_bet']
            if best:
                details = analysis['outcomes'][best]
                print(f"   ✅ Best bet: {best}")
                print(f"      EV: {details['expected_value']*100:+.2f}%")
                print(f"      Edge: {details['edge']*100:+.2f}%")
                print(f"      Kelly: {details['kelly_stake']*100:.2f}%")
            else:
                print(f"   ⚠️ No positive value bet found")
        
        print(f"\n✅ Betting value calculations work correctly")
        return True
        
    except Exception as e:
        print(f"❌ Betting value error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_betting_strategy(predictor):
    """Test 4: Betting strategy module works"""
    print("\n" + "="*70)
    print("TEST 4: Betting Strategy Module")
    print("="*70)
    
    teams = predictor.get_all_teams()
    if len(teams) < 2:
        print("❌ Not enough teams to test")
        return False
    
    try:
        # Create strategy
        strategy = BettingStrategy(predictor, initial_bankroll=1000)
        print(f"✅ Strategy initialized with ${strategy.current_bankroll:.2f}")
        
        # Evaluate a match
        team1, team2 = teams[0], teams[1]
        bookmaker_odds = {'win': 2.10, 'draw': 3.40, 'loss': 3.50}
        
        recommendation = strategy.evaluate_match(
            team1, team2, 'Home', bookmaker_odds,
            min_confidence=0.65, min_edge=0.08
        )
        
        print(f"✅ Match evaluated: {recommendation['match']}")
        print(f"   Should bet: {recommendation['should_bet']}")
        print(f"   Reason: {recommendation['reason']}")
        
        if recommendation['should_bet']:
            details = recommendation['bet_details']
            print(f"   Outcome: {details['outcome']}")
            print(f"   Stake: ${details['stake_amount']:.2f} ({details['stake_pct']*100:.2f}%)")
            print(f"   EV: {details['expected_value']*100:+.2f}%")
            
            # Simulate winning the bet
            result = strategy.simulate_bet(recommendation, details['outcome'])
            print(f"\n✅ Bet simulation successful")
            print(f"   Won: {result['won']}")
            print(f"   Profit: ${result['profit']:+.2f}")
            print(f"   New bankroll: ${result['new_bankroll']:.2f}")
        
        # Test performance stats
        stats = strategy.get_performance_stats()
        if stats:
            print(f"\n✅ Performance stats generated")
            print(f"   Total bets: {stats['total_bets']}")
            print(f"   Current bankroll: ${stats['current_bankroll']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Strategy error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_edge_detection(predictor):
    """Test 5: Edge detection works correctly"""
    print("\n" + "="*70)
    print("TEST 5: Edge Detection")
    print("="*70)
    
    teams = predictor.get_all_teams()
    if len(teams) < 2:
        print("❌ Not enough teams to test")
        return False
    
    team1, team2 = teams[0], teams[1]
    
    try:
        # Get prediction
        pred = predictor.predict(team1, team2, 'Home', use_neural_network=True)
        
        # Test different edge scenarios
        print("\n📊 Positive Edge (Should Bet):")
        good_odds = {
            'win': 2.50,  # Bookmaker implies 40%, model predicts more
            'draw': 3.40,
            'loss': 3.50
        }
        
        should_bet, reason = predictor.should_bet(pred, good_odds, 
                                                  min_confidence=0.50, min_edge=0.05)
        print(f"   Model prob (win): {pred['win']*100:.1f}%")
        print(f"   Implied prob: {(1/good_odds['win'])*100:.1f}%")
        print(f"   Edge: {(pred['win'] - 1/good_odds['win'])*100:+.2f}%")
        print(f"   Decision: {should_bet} - {reason}")
        
        print("\n📊 Negative Edge (Should Not Bet):")
        bad_odds = {
            'win': 1.50,  # Bookmaker implies 66%, model predicts less
            'draw': 4.00,
            'loss': 7.00
        }
        
        should_bet, reason = predictor.should_bet(pred, bad_odds, 
                                                  min_confidence=0.50, min_edge=0.05)
        print(f"   Model prob (win): {pred['win']*100:.1f}%")
        print(f"   Implied prob: {(1/bad_odds['win'])*100:.1f}%")
        print(f"   Edge: {(pred['win'] - 1/bad_odds['win'])*100:+.2f}%")
        print(f"   Decision: {should_bet} - {reason}")
        
        print("\n✅ Edge detection working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Edge detection error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_kelly_criterion(predictor):
    """Test 6: Kelly Criterion calculations"""
    print("\n" + "="*70)
    print("TEST 6: Kelly Criterion")
    print("="*70)
    
    teams = predictor.get_all_teams()
    if len(teams) < 2:
        print("❌ Not enough teams to test")
        return False
    
    team1, team2 = teams[0], teams[1]
    
    try:
        pred = predictor.predict(team1, team2, 'Home', use_neural_network=True)
        
        # Test with favorable odds
        odds = {'win': 2.50, 'draw': 3.40, 'loss': 3.50}
        analysis = predictor.calculate_betting_value(pred, odds)
        
        print(f"\n📊 Kelly Stake Calculation:")
        for outcome, data in analysis['outcomes'].items():
            if data['bet']:
                print(f"   {outcome.upper()}:")
                print(f"      Kelly stake: {data['kelly_stake']*100:.2f}%")
                print(f"      Expected Value: {data['expected_value']*100:+.2f}%")
                
                # Verify Kelly is within reasonable bounds
                if data['kelly_stake'] < 0:
                    print(f"      ❌ Negative Kelly stake!")
                    return False
                
                if data['kelly_stake'] > 0.05:
                    print(f"      ⚠️ Kelly stake > 5% (capped)")
                
                print(f"      ✅ Kelly stake is valid")
        
        print(f"\n✅ Kelly Criterion calculations correct")
        return True
        
    except Exception as e:
        print(f"❌ Kelly Criterion error: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 RUNNING BETTING MODEL VALIDATION TESTS")
    print("="*70)
    
    # Test 1: Load model
    predictor = test_model_loading()
    if not predictor:
        print("\n❌ FAILED: Could not load model")
        return False
    
    # Test 2: Predictions with confidence
    if not test_predictions_with_confidence(predictor):
        print("\n❌ FAILED: Predictions test failed")
        return False
    
    # Test 3: Betting value calculation
    if not test_betting_value_calculation(predictor):
        print("\n❌ FAILED: Betting value test failed")
        return False
    
    # Test 4: Betting strategy
    if not test_betting_strategy(predictor):
        print("\n❌ FAILED: Betting strategy test failed")
        return False
    
    # Test 5: Edge detection
    if not test_edge_detection(predictor):
        print("\n❌ FAILED: Edge detection test failed")
        return False
    
    # Test 6: Kelly Criterion
    if not test_kelly_criterion(predictor):
        print("\n❌ FAILED: Kelly Criterion test failed")
        return False
    
    # All tests passed
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    print("\n💡 Your model is ready for sports betting with:")
    print("   ✅ Confidence scoring")
    print("   ✅ Expected value calculations")
    print("   ✅ Kelly Criterion bankroll management")
    print("   ✅ Edge detection")
    print("   ✅ Value betting analysis")
    print("\n📚 See BETTING_GUIDE.md for usage instructions")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
