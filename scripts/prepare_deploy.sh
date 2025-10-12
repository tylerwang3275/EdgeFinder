#!/bin/bash
set -euo pipefail

# EdgeFinder Deployment Preparation Script
echo "🚀 Preparing EdgeFinder for deployment..."

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial EdgeFinder commit"
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Creating .env file from template..."
    cp env.example .env
    echo "📝 Please edit .env file with your ODDS_API_KEY before deploying!"
    echo "   Get your free API key at: https://theoddsapi.com"
    read -p "Press Enter after editing .env file..."
fi

# Check if ODDS_API_KEY is set
if ! grep -q "ODDS_API_KEY=.*[^=]$" .env; then
    echo "❌ ODDS_API_KEY not set in .env file!"
    echo "   Please add your API key to .env file"
    exit 1
fi

# Test the application locally
echo "🧪 Testing application locally..."
if USE_FIXTURES=true python -m src.main run; then
    echo "✅ Local test passed!"
else
    echo "❌ Local test failed! Please fix issues before deploying."
    exit 1
fi

# Create deployment files if they don't exist
echo "📄 Ensuring deployment files exist..."

# Railway deployment
if [ ! -f railway.json ]; then
    echo "Creating railway.json..."
    cat > railway.json << EOF
{
  "\$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python -m src.main serve --host 0.0.0.0 --port \$PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF
fi

# Heroku deployment
if [ ! -f Procfile ]; then
    echo "Creating Procfile..."
    echo "web: python -m src.main serve --host 0.0.0.0 --port \$PORT" > Procfile
fi

# Commit deployment files
echo "📝 Committing deployment files..."
git add railway.json Procfile
git commit -m "Add deployment configuration" || echo "No changes to commit"

# Check if remote exists
if ! git remote | grep -q origin; then
    echo "🌐 No remote repository found."
    echo "   Please create a GitHub repository and add it as origin:"
    echo "   git remote add origin https://github.com/yourusername/EdgeFinder.git"
    echo "   git push -u origin main"
else
    echo "🔄 Pushing to remote repository..."
    git push origin main
fi

echo ""
echo "🎉 EdgeFinder is ready for deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://railway.app"
echo "2. Sign up with GitHub"
echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
echo "4. Select your EdgeFinder repository"
echo "5. Set environment variable: ODDS_API_KEY=your_key_here"
echo "6. Click 'Deploy'"
echo ""
echo "🌐 Your app will be live in 2-3 minutes!"
echo "📖 See QUICK_DEPLOY.md for other deployment options"
