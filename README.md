# ⚽ Football Prediction Model for Sports Betting

Advanced machine learning model for football match predictions with comprehensive betting analysis and bankroll management.

## 🎯 Overview

This project implements a neural network-based football prediction system optimized for **sports betting**. It includes:

- ✅ **Neural Network Predictions** with confidence scoring
- ✅ **Expected Value (EV) Calculations** for betting decisions
- ✅ **Kelly Criterion** bankroll management
- ✅ **Edge Detection** against bookmaker odds
- ✅ **Value Betting** recommendations
- ✅ **Performance Tracking** and analytics

## 🚀 Quick Start

### 1. Install Dependencies
```bash
source .venv/bin/activate
pip install torch pandas numpy scikit-learn
```

### 2. Train the Model (if needed)
```bash
python3 train_model.py
```

### 3. Run Example
```bash
python3 quick_start.py
```

### 4. Run Tests
```bash
python3 test_betting_model.py
```

## 📊 Features

### Core Prediction Model
- **Chronological data handling** (no look-ahead bias)
- **Head-to-head statistics** integration
- **Recent form tracking** (last 5 games)
- **xG (expected goals)** metrics
- **Home/away advantage** calculation
- **Confidence scoring** based on entropy and data quality

### Betting Features
- **Expected Value** calculation
- **Kelly Criterion** stake sizing (fractional)
- **Edge detection** (model vs bookmaker)
- **Minimum thresholds** for betting decisions
- **Bankroll management** with risk controls
- **Performance tracking** (ROI, win rate, etc.)

## 🎲 Usage Examples

### Basic Prediction
```python
from model import FootballPredictor

predictor = FootballPredictor('data20202025.csv')
predictor.load_model('best_model.pth')

# Get prediction with confidence
prediction = predictor.predict('Juventus', 'Milan', venue='Home', use_neural_network=True)

print(f"Win: {prediction['win']*100:.1f}%")
print(f"Draw: {prediction['draw']*100:.1f}%")
print(f"Loss: {prediction['loss']*100:.1f}%")
print(f"Confidence: {prediction['confidence']*100:.1f}%")
```

### Betting Value Analysis
```python
# Your bookmaker's odds
bookmaker_odds = {
    'win': 2.10,   # Decimal odds
    'draw': 3.40,
    'loss': 3.50
}

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

### Advanced Strategy
```python
from betting_strategy import BettingStrategy, analyze_betting_conditions

# Create betting strategy with $1000 bankroll
strategy = BettingStrategy(predictor, initial_bankroll=1000)

# Analyze match
analyze_betting_conditions(predictor, 'Juventus', 'Milan', 'Home')

# Get recommendation
recommendation = strategy.evaluate_match('Juventus', 'Milan', 'Home', bookmaker_odds)

if recommendation['should_bet']:
    details = recommendation['bet_details']
    print(f"Bet ${details['stake_amount']:.2f} on {details['outcome']}")

# Track performance
strategy.print_performance_report()
```

## 📈 Betting Conditions

### When to Bet ✅

A bet is recommended when **ALL** conditions are met:

1. **Confidence ≥ 65%** - Model is confident in prediction
2. **EV > 5%** - Positive expected value
3. **Edge ≥ 8%** - Significant advantage over bookmaker
4. **Probability ≥ 35%** - Reasonable chance of winning
5. **Kelly Stake > 0.5%** - Bet size is meaningful

### Bankroll Management 💰

- **Fractional Kelly:** Use 25% of full Kelly (conservative)
- **Max Stake:** Never bet > 5% of bankroll
- **Min Stake:** Don't bet < 0.5% of bankroll
- **Stop-loss:** -20% of initial bankroll

## 📁 Project Structure

```
SerieA/
├── model.py                          # Core prediction model
├── betting_strategy.py               # Betting strategy module
├── train_model.py                    # Model training script
├── test_betting_model.py            # Validation tests
├── quick_start.py                    # Quick start example
├── data20202025.csv                  # Training data
├── best_model.pth                    # Trained model weights
├── BETTING_GUIDE.md                  # Comprehensive betting guide
├── MODEL_IMPROVEMENTS_SUMMARY.md     # Improvements documentation
└── README.md                         # This file
```

## 🧪 Testing

Run the complete test suite:

```bash
python3 test_betting_model.py
```

Expected output:
```
✅ ALL TESTS PASSED!

💡 Your model is ready for sports betting with:
   ✅ Confidence scoring
   ✅ Expected value calculations
   ✅ Kelly Criterion bankroll management
   ✅ Edge detection
   ✅ Value betting analysis
```

## 📚 Documentation

- **[BETTING_GUIDE.md](BETTING_GUIDE.md)** - Complete betting guide with best practices
- **[MODEL_IMPROVEMENTS_SUMMARY.md](MODEL_IMPROVEMENTS_SUMMARY.md)** - Detailed improvements documentation
- **[quick_start.py](quick_start.py)** - Interactive example with explanations

## 🎯 Key Improvements

### Fixed Critical Issues
1. ✅ **Neural Network Now Used** - Previously only used heuristics
2. ✅ **Natural Probabilities** - Removed artificial 65% cap
3. ✅ **Confidence Scoring** - Know when to trust predictions
4. ✅ **Complete Betting Logic** - EV, Kelly, edge detection

### New Features
- Confidence scoring (entropy-based)
- Expected value calculations
- Kelly Criterion stake sizing
- Edge detection
- Value betting recommendations
- Bankroll management
- Performance tracking
- Model calibration checks

## ⚠️ Important Warnings

1. **Start Small** - Test with paper trading first (50+ matches)
2. **Track Everything** - Need 100+ bets to evaluate strategy
3. **Be Selective** - Only bet when ALL conditions are met
4. **Shop Odds** - Use multiple bookmakers for best odds
5. **Update Regularly** - Retrain model every 2-3 months
6. **Bet Responsibly** - Never bet more than you can afford to lose

## 🎓 Success Metrics

After 100+ bets, aim for:

- ✅ ROI > 5% (sustainable long-term)
- ✅ Win Rate > 50% (for odds ~2.00)
- ✅ Confidence correlation with actual results
- ✅ Positive average EV across all bets
- ✅ Bankroll growth consistent with Kelly expectations
- ✅ Maximum drawdown < 25%

## 📞 Support

For questions or issues:
1. Check [BETTING_GUIDE.md](BETTING_GUIDE.md) for detailed information
2. Review [MODEL_IMPROVEMENTS_SUMMARY.md](MODEL_IMPROVEMENTS_SUMMARY.md) for technical details
3. Run `python3 quick_start.py` for interactive examples

## 📜 License

This project is for educational purposes. Always bet responsibly and within your means.

**Remember: Past performance doesn't guarantee future results.**

---

Made with ⚽ for sports betting enthusiasts
