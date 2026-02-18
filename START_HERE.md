# 🚀 Project Startup Guide

## Quick Start (3 Steps)

### Step 1: Activate Virtual Environment

```bash
cd /Users/jawadbouchiba/SerieA
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt.

---

### Step 2: Choose Your Starting Point

#### **Option A: See Interactive Demo** (Recommended First Time)
```bash
python3 quick_start.py
```N
**What it does:**
- Shows complete match analysis with explanations
- Demonstrates betting value calculations
- Explains confidence scoring and Kelly Criterion
- Perfect for understanding how everything works

---

#### **Option B: Test Everything Works**
```bash
python3 test_betting_model.py
```
**What it does:**
- Runs 6 automated tests
- Validates all features work correctly
- Takes ~30 seconds
- Should end with "✅ ALL TESTS PASSED!"

---

#### **Option C: Make Real Predictions**
```bash
python3 my_predictions.py
```
**What it does:**
- Analyzes today's matches
- Gives betting recommendations
- Shows stake sizes and expected value
- **Edit the file to add your matches and odds!**

---

### Step 3: Customize for Your Needs

Edit `my_predictions.py` to add your matches:

```python
matches = [
    {
        'team1': 'Juventus',      # Home team
        'team2': 'Milan',         # Away team
        'venue': 'Home',          # 'Home' or 'Away'
        'odds': {
            'win': 2.10,          # Odds from your bookmaker
            'draw': 3.40,
            'loss': 3.50
        }
    },
    # Add more matches...
]
```

Then run:
```bash
python3 my_predictions.py
```

---

## 📚 Available Commands

### See Available Teams
```bash
python3 -c "from model import FootballPredictor; p = FootballPredictor('data20202025.csv'); p.load_model('best_model.pth'); print('\\n'.join(p.get_all_teams()))"
```

### Analyze Specific Match
```bash
python3 -c "
from betting_strategy import analyze_betting_conditions
from model import FootballPredictor

p = FootballPredictor('data20202025.csv')
p.load_model('best_model.pth')
analyze_betting_conditions(p, 'Juventus', 'Milan', 'Home')
"
```

### Quick Prediction
```bash
python3 -c "
from model import FootballPredictor

p = FootballPredictor('data20202025.csv')
p.load_model('best_model.pth')
pred = p.predict('Juventus', 'Milan', 'Home', use_neural_network=True)

print(f'Win: {pred[\"win\"]*100:.1f}%')
print(f'Draw: {pred[\"draw\"]*100:.1f}%')
print(f'Loss: {pred[\"loss\"]*100:.1f}%')
print(f'Confidence: {pred[\"confidence\"]*100:.1f}%')
"
```

---

## 🔄 If You Need to Retrain the Model

The model is already trained (`best_model.pth` exists), but if you want to retrain:

```bash
# Delete old model
rm best_model.pth

# Train new model (takes ~2-3 minutes)
python3 train_model.py
```

**When to retrain:**
- New season starts
- You have updated data
- Every 2-3 months for best performance

---

## 📁 Project Files Overview

```
SerieA/
├── 🎯 ENTRY POINTS (Start here):
│   ├── quick_start.py           # Interactive demo
│   ├── test_betting_model.py    # Validation tests
│   └── my_predictions.py        # Your custom predictions (EDIT THIS)
│
├── 📚 DOCUMENTATION:
│   ├── README.md                # Project overview
│   ├── BETTING_GUIDE.md         # Complete betting guide
│   ├── MODEL_IMPROVEMENTS_SUMMARY.md  # What was improved
│   └── START_HERE.md            # This file
│
├── 🔧 CORE CODE:
│   ├── model.py                 # Prediction model
│   ├── betting_strategy.py     # Betting logic
│   └── train_model.py          # Training script
│
└── 📊 DATA:
    ├── data20202025.csv         # Training data
    └── best_model.pth           # Trained model
```

---

## 🎯 Common Use Cases

### Use Case 1: Daily Betting Routine
```bash
# Morning: Get today's predictions
python3 my_predictions.py > today_bets.txt
cat today_bets.txt

# Place recommended bets at your bookmaker

# Evening: Track results (manually for now)
```

### Use Case 2: Deep Analysis of Specific Match
```bash
python3 << EOF
from betting_strategy import analyze_betting_conditions
from model import FootballPredictor

p = FootballPredictor('data20202025.csv')
p.load_model('best_model.pth')

# Change teams here
analyze_betting_conditions(p, 'Inter', 'Napoli', 'Home')
EOF
```

### Use Case 3: Compare Multiple Bookmakers
Edit `my_predictions.py` with odds from different bookmakers and run separately to find best value.

---

## 💡 Tips for Best Results

### 1. **Start with Paper Trading**
- Track predictions without betting real money
- Need 50-100 bets to evaluate strategy
- Adjust thresholds based on results

### 2. **Key Parameters to Adjust**
In `my_predictions.py`:
```python
recommendation = strategy.evaluate_match(
    team1, team2, venue, odds,
    min_confidence=0.65,  # Lower = more bets (60-75% range)
    min_edge=0.08         # Lower = more bets (5-12% range)
)
```

**Conservative:** confidence=0.75, edge=0.12  
**Balanced:** confidence=0.65, edge=0.08 (default)  
**Aggressive:** confidence=0.60, edge=0.05

### 3. **Bankroll Management**
In `my_predictions.py`:
```python
strategy = BettingStrategy(predictor, initial_bankroll=1000)
```
**Change 1000 to your actual bankroll amount**

### 4. **Shop for Best Odds**
- Compare odds across multiple bookmakers
- Even 0.1 difference in odds matters long-term
- Use odds comparison sites

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'torch'"
```bash
source .venv/bin/activate  # Forgot to activate
pip install torch pandas numpy scikit-learn
```

### "FileNotFoundError: best_model.pth"
```bash
python3 train_model.py  # Train the model first
```

### "Team not found"
```bash
# See available teams
python3 -c "from model import FootballPredictor; p = FootballPredictor('data20202025.csv'); p.load_model('best_model.pth'); print('\\n'.join(sorted(p.get_all_teams())))"
```

### Model gives weird predictions
- Check if team names match exactly (case-sensitive)
- Ensure you have enough historical data
- Consider retraining with more recent data

---

## 📞 Need Help?

1. **Read the guides:**
   - `BETTING_GUIDE.md` - Complete betting strategy guide
   - `MODEL_IMPROVEMENTS_SUMMARY.md` - Technical details

2. **Test functionality:**
   ```bash
   python3 test_betting_model.py
   ```

3. **Try the examples:**
   ```bash
   python3 quick_start.py
   ```

---

## ⚠️ Important Reminders

- ✅ Always activate virtual environment first: `source .venv/bin/activate`
- ✅ Start with paper trading before real money
- ✅ Never bet more than 5% of bankroll on single bet
- ✅ Track at least 100 bets before judging strategy
- ✅ Update model every 2-3 months
- ✅ **Bet responsibly - only bet what you can afford to lose**

---

## 🎓 Next Steps

1. ✅ Run `python3 quick_start.py` to see how it works
2. ✅ Run `python3 test_betting_model.py` to validate
3. ✅ Edit `my_predictions.py` with your matches
4. ✅ Paper trade for 50+ matches
5. ✅ Read `BETTING_GUIDE.md` for advanced strategies
6. ✅ Start with small stakes when ready

**Good luck! 🍀⚽**
