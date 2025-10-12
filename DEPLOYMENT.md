# EdgeFinder Deployment Guide

This guide covers different ways to deploy EdgeFinder for online access.

## 🚀 Quick Start (Docker)

The easiest way to deploy EdgeFinder is using Docker:

```bash
# 1. Clone and navigate to the project
git clone <your-repo-url>
cd EdgeFinder

# 2. Configure environment
cp env.example .env
# Edit .env with your API keys (ODDS_API_KEY is required)

# 3. Deploy
./scripts/deploy.sh
```

The web interface will be available at `http://localhost:8000`

## 🌐 Production Deployment Options

### Option 1: Docker Compose (Recommended)

Perfect for VPS, dedicated servers, or local deployment:

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Features:**
- ✅ Web interface at port 8000
- ✅ Automatic daily updates via cron
- ✅ Health checks
- ✅ Easy scaling and management

### Option 2: Cloud Platforms

#### Heroku

1. Create a `Procfile`:
```
web: python -m src.main serve --host 0.0.0.0 --port $PORT
```

2. Deploy:
```bash
heroku create your-edgefinder-app
heroku config:set ODDS_API_KEY=your_key_here
git push heroku main
```

#### Railway

1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

#### DigitalOcean App Platform

1. Create new app from GitHub
2. Configure environment variables
3. Set build command: `pip install -e .`
4. Set run command: `python -m src.main serve --host 0.0.0.0 --port $PORT`

### Option 3: VPS/Dedicated Server

#### Using Docker (Recommended)

```bash
# On your server
git clone <your-repo>
cd EdgeFinder
cp env.example .env
# Edit .env with your API keys

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Deploy
./scripts/deploy.sh
```

#### Using Nginx Reverse Proxy

1. Install Nginx:
```bash
sudo apt update
sudo apt install nginx
```

2. Create Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. Enable SSL with Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `KALSHI_BASE_URL` | Kalshi API base URL | `https://api.kalshi.com` | No |
| `ODDS_API_BASE_URL` | TheOddsAPI base URL | `https://api.theoddsapi.com/v4` | No |
| `ODDS_API_KEY` | TheOddsAPI key | - | **Yes** |
| `EDGEFINDER_TIMEZONE` | Display timezone | `America/Los_Angeles` | No |
| `SPORTS_FILTER` | Comma-separated sports | `mlb,nfl,nba,nhl,soccer` | No |
| `LOOKAHEAD_HOURS` | Hours to look ahead | `48` | No |
| `MIN_VOLUME` | Minimum market volume | `100` | No |
| `TOP_N` | Number of top results | `10` | No |
| `USE_FIXTURES` | Use test data | `false` | No |

### API Keys

1. **TheOddsAPI**: Get your free API key at [theoddsapi.com](https://theoddsapi.com)
2. **Kalshi**: Currently using public endpoints (no key required)

## 📊 Monitoring & Maintenance

### Health Checks

- **Endpoint**: `GET /health`
- **Response**: `{"status": "healthy", "service": "edgefinder"}`

### Logs

```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f edgefinder_container_name

# Direct deployment
tail -f /var/log/edgefinder.log
```

### Data Updates

- **Automatic**: Daily at 1 PM Pacific (13:00 UTC) via cron
- **Manual**: `POST /refresh` endpoint or `python -m src.main run`

### Backup

The `out/` directory contains all generated reports:
```bash
# Backup data
tar -czf edgefinder-backup-$(date +%Y%m%d).tar.gz out/

# Restore data
tar -xzf edgefinder-backup-YYYYMMDD.tar.gz
```

## 🔒 Security Considerations

### Production Checklist

- [ ] Use HTTPS (SSL/TLS certificates)
- [ ] Set strong environment variables
- [ ] Configure firewall (only ports 80, 443, 22)
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity
- [ ] Backup data regularly

### Rate Limiting

The application respects API rate limits:
- **TheOddsAPI**: 500 requests/month (free tier)
- **Kalshi**: Public endpoints with reasonable limits

## 🚨 Troubleshooting

### Common Issues

1. **"No report available"**
   - Check API keys in `.env`
   - Verify internet connectivity
   - Check logs for API errors

2. **"Health check failed"**
   - Ensure port 8000 is available
   - Check if service is running
   - Verify Docker containers are healthy

3. **"Permission denied"**
   - Check file permissions
   - Ensure Docker has proper access
   - Verify `.env` file is readable

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python -m src.main serve
```

### Test with Fixtures

Use test data for development:
```bash
export USE_FIXTURES=true
python -m src.main run
```

## 📈 Scaling

### Horizontal Scaling

For high-traffic deployments:

1. **Load Balancer**: Use Nginx or cloud load balancer
2. **Multiple Instances**: Run multiple containers
3. **Database**: Consider external database for caching
4. **CDN**: Use CloudFlare or similar for static assets

### Performance Optimization

- **Caching**: Reports are cached for 5 minutes
- **Static Files**: Served efficiently via FastAPI
- **API Limits**: Respects external API rate limits

## 🆘 Support

- **Issues**: Create GitHub issues for bugs
- **Documentation**: Check README.md for usage
- **API**: Use `/health` endpoint for status checks

---

**Happy Deploying! 🎉**
