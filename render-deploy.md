# 🚀 Free Deployment on Render - EdgeFinder

## Why Render?
- ✅ **Completely FREE** (750 hours/month)
- ✅ **No credit card required**
- ✅ **Automatic deployments** from GitHub
- ✅ **Custom domains** on free tier
- ✅ **Perfect for FastAPI apps**

## Quick Setup (5 minutes)

### Step 1: Go to Render
1. Open [render.com](https://render.com) in your browser
2. Click **"Get Started for Free"**
3. Sign up with your **GitHub account**

### Step 2: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your **GitHub repository**
3. Select **"tylerwang3275/EdgeFinder"**
4. Click **"Connect"**

### Step 3: Configure Service
Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `edgefinder` (or any name you like) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -e .` |
| **Start Command** | `python -m src.main serve --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` |

### Step 4: Set Environment Variables
Click **"Advanced"** and add these environment variables:

| Key | Value |
|-----|-------|
| `ODDS_API_KEY` | `d98557c1e7c0485b02c4a0389890d6db` |
| `USE_FIXTURES` | `false` |
| `DEBUG` | `false` |
| `LOG_LEVEL` | `INFO` |

### Step 5: Deploy!
1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Your app will be live at: `https://edgefinder.onrender.com` (or similar)

## 🎯 Test Your Live App

Your EdgeFinder will be live with:
- **📱 Web Interface**: `https://your-app-name.onrender.com`
- **🔍 API Endpoint**: `https://your-app-name.onrender.com/api/latest`
- **💚 Health Check**: `https://your-app-name.onrender.com/health`
- **📊 CSV Download**: `https://your-app-name.onrender.com/api/csv`

## 🎉 What You'll Get

- ✅ **Real-time sports data** from TheOddsAPI
- ✅ **Live betting edges** analysis
- ✅ **Seattle team focus**
- ✅ **Auto-refreshing dashboard**
- ✅ **CSV export functionality**
- ✅ **Professional web interface**
- ✅ **Mobile-responsive design**

## 🔧 Troubleshooting

### If deployment fails:
1. Check the **"Logs"** tab for error messages
2. Verify environment variables are set correctly
3. Make sure build command is: `pip install -e .`

### If app won't start:
1. Check that start command is: `python -m src.main serve --host 0.0.0.0 --port $PORT`
2. Verify all environment variables are present
3. Check the build logs for Python errors

### If no data appears:
1. Verify your API key is working
2. Check if there are active games in the next 48 hours
3. Try setting `USE_FIXTURES=true` temporarily to test

## 📈 Free Tier Limits

- **750 hours/month** (enough for 24/7 operation)
- **512 MB RAM**
- **Automatic sleep** after 15 minutes of inactivity (wakes up on first request)
- **Custom domains** supported
- **No credit card required**

## 🆘 Need Help?

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **GitHub Issues**: [github.com/tylerwang3275/EdgeFinder/issues](https://github.com/tylerwang3275/EdgeFinder/issues)

---

**Your EdgeFinder will be completely FREE on Render! 🚀📈**
