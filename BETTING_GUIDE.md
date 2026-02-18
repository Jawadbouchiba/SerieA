# 🎲 Sports Betting Guide - Best Practices & Conditions

## 📊 Model Assessment

### ✅ **Strengths of Your Current Model**

1. **Proper Data Handling**
   - ✅ Chronological feature preparation (no look-ahead bias)
   - ✅ Rolling statistics (team history updated after each match)
   - ✅ Head-to-head statistics integration

2. **Good Feature Engineering**
   - ✅ Recent form (last 5 games)
   - ✅ Expected goals (xG) metrics
   - ✅ Home/away advantage
   - ✅ Possession and shooting statistics

3. **Regularization Techniques**
   - ✅ Dropout layers (0.3-0.4)
   - ✅ Label smoothing (0.1)
   - ✅ Weight decay (1e-4)
   - ✅ Learning rate scheduling

### ⚠️ **Critical Issues Fixed**

1. **Neural Network Not Used** ❌ → ✅ **FIXED**
   - Previously: Predictions used only heuristics, ignoring the trained neural network
   - Now: Hybrid approach (70% NN + 30% heuristics)

2. **Probability Capping** ❌ → ✅ **FIXED**
   - Previously: Probabilities capped at 65% max (too conservative)
   - Now: Natural probabilities with confidence scoring

3. **No Confidence Metrics** ❌ → ✅ **FIXED**
   - Added entropy-based confidence scoring
   - Adjusts confidence based on data availability

4. **No Betting Logic** ❌ → ✅ **FIXED**
   - Added Kelly Criterion for bankroll management
   - Expected Value (EV) calculations
   - Value betting detection

---

## 🎯 Key Betting Conditions Added

### 1. **Confidence Thresholds**

```python
# Minimum confidence levels for betting
MIN_CONFIDENCE = 0.65  # 65% confidence minimum
OPTIMAL_CONFIDENCE = 0.75  # 75%+ for best bets

# Confidence calculation based on:
- Prediction entropy (lower = more confident)
- Data availability (more games = more confidence)
- Team statistics quality
```

### 2. **Expected Value (EV) Calculation**

```python
# Only bet when EV > 0
EV = (Probability × Odds) - 1

# Minimum thresholds:
MIN_EV = 0.05  # 5% positive expected value
OPTIMAL_EV = 0.10  # 10%+ for aggressive betting
```

### 3. **Kelly Criterion (Bankroll Management)**

```python
# Kelly formula: f = (bp - q) / b
# Where:
# f = fraction of bankroll to bet
# b = odds - 1
# p = probability of winning
# q = probability of losing (1 - p)

# Fractional Kelly (conservative):
kelly_stake = kelly_fraction × 0.25  # Use 25% of full Kelly

# Maximum stake cap:
MAX_STAKE = 0.05  # Never bet more than 5% of bankroll
```

### 4. **Edge Detection**

```python
# Edge = Model Probability - Implied Probability
edge = model_prob - (1 / bookmaker_odds)

# Minimum edge requirements:
MIN_EDGE = 0.08  # 8% edge minimum
OPTIMAL_EDGE = 0.15  # 15%+ for high-value bets
```

### 5. **Minimum Probability Threshold**

```python
# Don't bet on unlikely outcomes
MIN_PROBABILITY = 0.35  # 35% minimum

# This prevents betting on longshots with poor value
```

---

## 📈 Betting Decision Framework

### When to Bet ✅

A bet is recommended when **ALL** conditions are met:

1. ✅ **Confidence ≥ 65%** (model is confident in prediction)
2. ✅ **EV > 5%** (positive expected value)
3. ✅ **Edge ≥ 8%** (significant advantage over bookmaker)
4. ✅ **Probability ≥ 35%** (reasonable chance of winning)
5. ✅ **Kelly Stake > 0.5%** (bet size is meaningful)

### When NOT to Bet ❌

- ❌ Confidence < 65%
- ❌ Negative or low EV (< 5%)
- ❌ Insufficient edge (< 8%)
- ❌ Limited historical data (< 10 games per team)
- ❌ Extreme odds that don't match model probability

---

## 💰 Bankroll Management Rules

### Conservative Strategy (Recommended)

```python
- Use fractional Kelly: 25% of full Kelly
- Maximum stake: 5% of bankroll
- Minimum stake: 0.5% of bankroll
- Stop-loss: -20% of initial bankroll
- Target: +50% ROI over season
```

### Aggressive Strategy (Higher Risk)

```python
- Use fractional Kelly: 50% of full Kelly
- Maximum stake: 8% of bankroll
- Minimum confidence: 70%
- Minimum edge: 10%
```

### Ultra-Conservative Strategy (Low Risk)

```python
- Use fractional Kelly: 15% of full Kelly
- Maximum stake: 2% of bankroll
- Minimum confidence: 75%
- Minimum edge: 12%
```

---

## 🔧 How to Use the Enhanced Model

### 1. Basic Prediction with Confidence

```python
from model import FootballPredictor

predictor = FootballPredictor('data20202025.csv')
predictor.load_model('best_model.pth')

# Get prediction with confidence score
prediction = predictor.predict('Team A', 'Team B', venue='Home', use_neural_network=True)

print(f"Win: {prediction['win']*100:.1f}%")
print(f"Draw: {prediction['draw']*100:.1f}%")
print(f"Loss: {prediction['loss']*100:.1f}%")
print(f"Confidence: {prediction['confidence']*100:.1f}%")
```

### 2. Betting Value Analysis

```python
from model import FootballPredictor

predictor = FootballPredictor('data20202025.csv')
predictor.load_model('best_model.pth')

# Your bookmaker's odds
bookmaker_odds = {
    'win': 2.10,   # Decimal odds for Team A win
    'draw': 3.40,  # Decimal odds for draw
    'loss': 3.50   # Decimal odds for Team B win
}

# Get prediction
prediction = predictor.predict('Team A', 'Team B', venue='Home')

# Calculate betting value
betting_analysis = predictor.calculate_betting_value(prediction, bookmaker_odds)

# Check if bet is recommended
should_bet, reason = predictor.should_bet(prediction, bookmaker_odds, 
                                         min_confidence=0.65, min_edge=0.08)

if should_bet:
    best_bet = betting_analysis['best_bet']
    details = betting_analysis['outcomes'][best_bet]
    
    print(f"✅ BET on {best_bet}")
    print(f"Stake: {details['kelly_stake']*100:.2f}% of bankroll")
    print(f"Expected Value: {details['expected_value']*100:+.2f}%")
    print(f"Edge: {details['edge']*100:+.2f}%")
else:
    print(f"❌ NO BET: {reason}")
```

### 3. Advanced Strategy with Betting Module

```python
from betting_strategy import BettingStrategy, analyze_betting_conditions

predictor = FootballPredictor('data20202025.csv')
predictor.load_model('best_model.pth')

# Create betting strategy with $1000 bankroll
strategy = BettingStrategy(predictor, initial_bankroll=1000)

# Analyze a match
analyze_betting_conditions(predictor, 'Team A', 'Team B', venue='Home')

# Get betting recommendation
bookmaker_odds = {'win': 2.10, 'draw': 3.40, 'loss': 3.50}
recommendation = strategy.evaluate_match('Team A', 'Team B', 'Home', bookmaker_odds)

if recommendation['should_bet']:
    details = recommendation['bet_details']
    print(f"Bet ${details['stake_amount']:.2f} on {details['outcome']}")
    
    # Simulate the bet (after match result is known)
    actual_result = 'win'  # The actual match result
    result = strategy.simulate_bet(recommendation, actual_result)
    
    print(f"Profit: ${result['profit']:+.2f}")
    print(f"New bankroll: ${result['new_bankroll']:.2f}")

# View performance stats
strategy.print_performance_report()
```

---

## 📊 Model Calibration & Validation

### Check Model Calibration

```python
# Load test data
X_test, y_test = predictor.load_and_prepare_data()
X_train, X_test, y_train, y_test = train_test_split(X_test, y_test, test_size=0.2)

# Get calibration curve
calibration = predictor.calibration_curve(X_test, y_test, n_bins=10)

# A well-calibrated model should have predicted ≈ observed
# If model says 70% win probability, it should win ~70% of the time
```

### Key Metrics to Monitor

1. **ROI (Return on Investment)**
   - Target: +10% to +30% per season
   - Break-even: 0%
   - Warning: < -10%

2. **Win Rate**
   - Target: > 52% for -110 odds (American)
   - Target: > 50% for 2.00 odds (Decimal)

3. **Expected Value**
   - Average EV per bet: > +5%
   - Only bet positive EV

4. **Kelly Stake**
   - Average: 1-3% of bankroll
   - If consistently > 5%, model may be overconfident

---

## ⚠️ Important Warnings

### 1. **Overconfidence Risk**
- The model can be overconfident on limited data
- Always check team statistics (minimum 10 games recommended)
- Lower confidence for new teams or early season

### 2. **Bookmaker Margins**
- Bookmakers have 3-7% margins built into odds
- You need significant edge to overcome this
- Shop for best odds across multiple bookmakers

### 3. **Sample Size**
- Track at least 100 bets before evaluating strategy
- Short-term variance is high in sports betting
- Don't adjust strategy based on < 50 bets

### 4. **Emotional Control**
- Never chase losses
- Stick to Kelly Criterion
- Never bet more than 5% on single bet
- Take breaks after big wins/losses

### 5. **Data Quality**
- Model quality depends on data quality
- Update model regularly with new data
- Retrain every 2-3 months or after major roster changes

---

## 🚀 Next Steps for Improvement

### Short-term Improvements

1. **Add More Features**
   - Player injuries and suspensions
   - Weather conditions
   - Travel distance
   - Rest days between matches
   - Referee statistics

2. **Enhanced Head-to-Head**
   - Weight recent H2H more heavily
   - Consider venue-specific H2H
   - Time decay for older matches

3. **Market Analysis**
   - Track opening vs closing odds
   - Line movement analysis
   - Sharp vs public money detection

### Long-term Improvements

1. **Ensemble Models**
   - Combine multiple models (NN, XGBoost, LightGBM)
   - Weighted voting based on confidence

2. **Live Betting**
   - In-play prediction updates
   - Current score integration
   - Momentum tracking

3. **Alternative Markets**
   - Over/Under goals
   - Both teams to score
   - Asian handicaps
   - Correct score

4. **Advanced Bankroll Management**
   - Dynamic Kelly based on confidence
   - Portfolio theory for multiple bets
   - Risk-adjusted returns

---

## 📚 Recommended Reading

- **"Trading Bases"** by Joe Peta - Sports betting bankroll management
- **"Sharp Sports Betting"** by Stanford Wong - Value betting principles
- **"The Kelly Capital Growth Investment Criterion"** - Mathematical foundations
- **"Thinking in Bets"** by Annie Duke - Decision making under uncertainty

---

## 🎯 Success Metrics (Track These)

```python
# After 100+ bets, you should see:
✅ ROI > 5% (long-term sustainable)
✅ Win Rate > 50% (for decimal odds ~2.00)
✅ Confidence Score correlation with actual win rate
✅ Positive EV on average across all bets
✅ Bankroll growth consistent with Kelly Criterion expectations
✅ Maximum drawdown < 25%
```

---

## 💡 Pro Tips

1. **Start Small**: Test with small stakes for first 50 bets
2. **Track Everything**: Use the betting_strategy.py module to log all bets
3. **Be Selective**: Only bet when ALL conditions are met
4. **Shop Odds**: Use odds comparison sites (Oddschecker, etc.)
5. **Specialize**: Focus on specific leagues/competitions you know well
6. **Ignore Emotion**: Never bet on your favorite team with bias
7. **Value > Winning**: Focus on +EV bets, not just winning bets
8. **Compound Growth**: Reinvest profits using Kelly Criterion

---

## 📞 Support

For questions about the model or betting strategy:
1. Check IMPROVEMENTS.md for recent changes
2. Review example predictions in betting_strategy.py
3. Test with paper trading before using real money

**Remember: Past performance doesn't guarantee future results. Bet responsibly.**
