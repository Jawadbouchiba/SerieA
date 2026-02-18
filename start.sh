#!/bin/bash
# Quick start script for Sports Betting Model

echo "⚽ Football Betting Model - Quick Start"
echo "======================================"
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "🔧 Activating virtual environment..."
    source .venv/bin/activate
fi

echo "Choose an option:"
echo ""
echo "1) 🎯 Run Interactive Demo (Recommended first time)"
echo "2) 🧪 Run Tests (Validate everything works)"
echo "3) 💰 Make Predictions for Today's Matches"
echo "4) 📊 See Available Teams"
echo "5) 📚 Read Documentation"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "🎯 Running Interactive Demo..."
        python3 quick_start.py
        ;;
    2)
        echo ""
        echo "🧪 Running Tests..."
        python3 test_betting_model.py
        ;;
    3)
        echo ""
        echo "💰 Running Predictions..."
        echo "💡 Edit my_predictions.py to customize matches and odds"
        python3 my_predictions.py
        ;;
    4)
        echo ""
        echo "📊 Available Teams:"
        python3 -c "from model import FootballPredictor; p = FootballPredictor('data20202025.csv'); p.load_model('best_model.pth'); print('\n'.join(sorted(p.get_all_teams())))"
        ;;
    5)
        echo ""
        echo "📚 Documentation Files:"
        echo "  - START_HERE.md (Complete startup guide)"
        echo "  - BETTING_GUIDE.md (Betting strategies)"
        echo "  - MODEL_IMPROVEMENTS_SUMMARY.md (Technical details)"
        echo "  - README.md (Project overview)"
        echo ""
        echo "Opening START_HERE.md..."
        if command -v open &> /dev/null; then
            open START_HERE.md
        else
            cat START_HERE.md
        fi
        ;;
    *)
        echo "Invalid choice. Please run again and choose 1-5."
        exit 1
        ;;
esac

echo ""
echo "✅ Done!"
