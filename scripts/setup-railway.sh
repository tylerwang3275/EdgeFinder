#!/bin/bash
set -euo pipefail

# EdgeFinder Railway Setup Script
echo "🚀 Setting up EdgeFinder on Railway..."

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

# Open Railway in browser
echo "🌐 Opening Railway in your browser..."
if command -v open > /dev/null; then
    open "https://railway.app"
elif command -v xdg-open > /dev/null; then
    xdg-open "https://railway.app"
else
    echo "Please open https://railway.app in your browser"
fi

echo ""
echo "🎯 Next steps:"
echo "1. Sign up/Login to Railway with GitHub"
echo "2. Click 'New Project' → 'Deploy from GitHub repo'"
echo "3. Select 'tylerwang3275/EdgeFinder'"
echo "4. Set environment variables:"
echo "   - ODDS_API_KEY = d98557c1e7c0485b02c4a0389890d6db"
echo "   - USE_FIXTURES = false"
echo "5. Deploy!"
echo ""
echo "📖 See railway-deploy.md for detailed instructions"
echo ""
echo "🎉 Your EdgeFinder will be live in minutes!"
