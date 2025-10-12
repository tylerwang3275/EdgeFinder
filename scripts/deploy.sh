#!/bin/bash
set -euo pipefail

# EdgeFinder Deployment Script
echo "🚀 Deploying EdgeFinder..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env.example .env
    echo "📝 Please edit .env file with your API keys before continuing."
    echo "   Required: ODDS_API_KEY"
    read -p "Press Enter to continue after editing .env..."
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ EdgeFinder is running successfully!"
    echo "🌐 Web interface: http://localhost:8000"
    echo "📊 API endpoint: http://localhost:8000/api/latest"
    echo "💾 CSV download: http://localhost:8000/api/csv"
    echo ""
    echo "📋 Useful commands:"
    echo "   View logs: docker-compose logs -f"
    echo "   Stop services: docker-compose down"
    echo "   Restart: docker-compose restart"
    echo "   Update: docker-compose pull && docker-compose up -d"
else
    echo "❌ Health check failed. Check logs with: docker-compose logs"
    exit 1
fi
