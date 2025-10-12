#!/bin/bash
set -euo pipefail

# EdgeFinder Render Setup Script
echo "🚀 Setting up EdgeFinder on Render (FREE!)..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Please run this script from the EdgeFinder root directory"
    exit 1
fi

# Check if git remote is set up
if ! git remote | grep -q origin; then
    echo "❌ Git remote not set up. Please run:"
    echo "   git remote add origin https://github.com/tylerwang3275/EdgeFinder.git"
    exit 1
fi

# Check if code is pushed to GitHub
echo "📤 Checking GitHub repository..."
if ! git ls-remote origin main > /dev/null 2>&1; then
    echo "❌ Code not pushed to GitHub. Please run:"
    echo "   git push -u origin main"
    exit 1
fi

echo "✅ Code is ready on GitHub!"

# Open Render in browser
echo "🌐 Opening Render in your browser..."
if command -v open > /dev/null; then
    open "https://render.com"
elif command -v xdg-open > /dev/null; then
    xdg-open "https://render.com"
else
    echo "Please open https://render.com in your browser"
fi

echo ""
echo "🎯 Next steps:"
echo "1. Sign up/Login to Render with GitHub (FREE!)"
echo "2. Click 'New +' → 'Web Service'"
echo "3. Connect 'tylerwang3275/EdgeFinder' repository"
echo "4. Configure service:"
echo "   - Name: edgefinder"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -e ."
echo "   - Start Command: python -m src.main serve --host 0.0.0.0 --port \$PORT"
echo "   - Plan: Free"
echo "5. Set environment variables:"
echo "   - ODDS_API_KEY = d98557c1e7c0485b02c4a0389890d6db"
echo "   - USE_FIXTURES = false"
echo "6. Deploy!"
echo ""
echo "📖 See render-deploy.md for detailed instructions"
echo ""
echo "🎉 Your EdgeFinder will be FREE and live in minutes!"
echo "💰 No credit card required - completely free!"
