# 🚀 Quick Deploy Guide - EdgeFinder Live

Get EdgeFinder running live on the web in minutes! Choose your preferred platform:

## 🌟 Option 1: Railway (Recommended - Easiest)

**Deploy in 2 minutes:**

1. **Sign up**: Go to [railway.app](https://railway.app) and sign up with GitHub
2. **Connect repo**: Click "New Project" → "Deploy from GitHub repo"
3. **Select EdgeFinder**: Choose your EdgeFinder repository
4. **Set environment variables**:
   - `ODDS_API_KEY`: Your TheOddsAPI key (get free at [theoddsapi.com](https://theoddsapi.com))
   - `USE_FIXTURES`: Set to `true` for testing (optional)
5. **Deploy**: Click "Deploy" and wait 2-3 minutes
6. **Access**: Your app will be live at `https://your-app-name.railway.app`

**✅ Pros**: Free tier, automatic deployments, easy setup
**❌ Cons**: Limited free tier (500 hours/month)

---

## 🐳 Option 2: Docker + VPS

**Deploy on any VPS (DigitalOcean, Linode, etc.):**

```bash
# On your VPS
git clone <your-repo-url>
cd EdgeFinder
cp env.example .env
# Edit .env with your API key

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Deploy
./scripts/deploy.sh
```

**✅ Pros**: Full control, unlimited usage, custom domain
**❌ Cons**: Requires VPS management

---

## ☁️ Option 3: Heroku

**Deploy to Heroku:**

```bash
# Install Heroku CLI
# Create app
heroku create your-edgefinder-app

# Set environment variables
heroku config:set ODDS_API_KEY=your_key_here

# Deploy
git push heroku main
```

**✅ Pros**: Easy deployment, good free tier
**❌ Cons**: Free tier discontinued, paid plans only

---

## 🔥 Option 4: Render

**Deploy to Render:**

1. **Sign up**: Go to [render.com](https://render.com)
2. **New Web Service**: Connect your GitHub repo
3. **Configure**:
   - Build Command: `pip install -e .`
   - Start Command: `python -m src.main serve --host 0.0.0.0 --port $PORT`
4. **Set environment variables**: `ODDS_API_KEY`
5. **Deploy**: Click "Create Web Service"

**✅ Pros**: Free tier, automatic deployments
**❌ Cons**: Free tier has limitations

---

## 🎯 Option 5: DigitalOcean App Platform

**Deploy to DigitalOcean:**

1. **Create app**: Go to DigitalOcean App Platform
2. **Connect GitHub**: Select your EdgeFinder repo
3. **Configure**:
   - Build Command: `pip install -e .`
   - Run Command: `python -m src.main serve --host 0.0.0.0 --port $PORT`
4. **Environment variables**: Add `ODDS_API_KEY`
5. **Deploy**: Click "Create Resources"

**✅ Pros**: Reliable, good performance
**❌ Cons**: Paid service

---

## 🚀 Quick Start Commands

### For Railway (Recommended):
```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy EdgeFinder"
git push origin main

# 2. Go to railway.app and deploy from GitHub
# 3. Set ODDS_API_KEY environment variable
# 4. Deploy!
```

### For Docker:
```bash
# 1. Set up environment
cp env.example .env
# Edit .env with your API key

# 2. Deploy
./scripts/deploy.sh

# 3. Access at http://localhost:8000
```

---

## 🔑 Required API Key

**TheOddsAPI Key** (Free):
1. Go to [theoddsapi.com](https://theoddsapi.com)
2. Sign up for free account
3. Get your API key
4. Set as `ODDS_API_KEY` environment variable

**Free tier**: 500 requests/month (plenty for EdgeFinder)

---

## 📊 After Deployment

Your EdgeFinder will be live with:

- **📱 Web Interface**: Modern, responsive dashboard
- **🔄 Auto-refresh**: Updates every 5 minutes
- **📊 Live Data**: Real-time sports betting edges
- **🏠 Seattle Focus**: Hometown team analysis
- **💾 CSV Export**: Download data anytime

---

## 🆘 Troubleshooting

### Common Issues:

1. **"No report available"**
   - Check `ODDS_API_KEY` is set correctly
   - Verify API key is valid at theoddsapi.com

2. **Build fails**
   - Ensure all files are committed to GitHub
   - Check Python version compatibility

3. **App won't start**
   - Verify `PORT` environment variable is available
   - Check start command is correct

### Debug Mode:
```bash
# Test locally first
USE_FIXTURES=true python -m src.main serve
```

---

## 🎉 Success!

Once deployed, your EdgeFinder will be live and accessible worldwide! Share the URL with friends and start finding those betting edges! 

**Happy Trading! 📈⚡**
