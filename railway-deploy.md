# 🚀 Railway Deployment Guide for EdgeFinder

## Quick Setup (5 minutes)

### Step 1: Go to Railway
1. Open [railway.app](https://railway.app) in your browser
2. Click **"Sign up"** or **"Log in"**
3. Choose **"Continue with GitHub"** to connect your account

### Step 2: Create New Project
1. Click **"New Project"** button
2. Select **"Deploy from GitHub repo"**
3. Find and select **"tylerwang3275/EdgeFinder"**
4. Click **"Deploy Now"**

### Step 3: Set Environment Variables
Once the project is created:
1. Click on your project name
2. Go to the **"Variables"** tab
3. Add these environment variables:

| Key | Value |
|-----|-------|
| `ODDS_API_KEY` | `d98557c1e7c0485b02c4a0389890d6db` |
| `USE_FIXTURES` | `false` |
| `DEBUG` | `false` |
| `LOG_LEVEL` | `INFO` |

### Step 4: Wait for Deployment
- Railway will automatically build and deploy your app
- This takes about 2-3 minutes
- You'll see build logs in real-time
- Watch for "Deployment successful" message

### Step 5: Get Your Live URL
Once deployed:
1. Go to the **"Deployments"** tab
2. Click on your latest deployment
3. Copy the **"Domain"** URL (e.g., `https://edgefinder-production-xxxx.up.railway.app`)

## 🎯 Test Your Live App

Your EdgeFinder will be live at your Railway URL with:

- **📱 Web Interface**: `https://your-app-name.railway.app`
- **🔍 API Endpoint**: `https://your-app-name.railway.app/api/latest`
- **💚 Health Check**: `https://your-app-name.railway.app/health`
- **📊 CSV Download**: `https://your-app-name.railway.app/api/csv`

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
3. Make sure `ODDS_API_KEY` is valid

### If app won't start:
1. Check that `USE_FIXTURES=false` is set
2. Verify all environment variables are present
3. Check the build logs for Python errors

### If no data appears:
1. Verify your API key is working
2. Check if there are active games in the next 48 hours
3. Try setting `USE_FIXTURES=true` temporarily to test

## 📈 Next Steps

Once your app is live:
1. **Share the URL** with friends
2. **Bookmark it** for daily use
3. **Set up monitoring** (Railway provides basic monitoring)
4. **Consider upgrading** to Railway Pro for more resources

## 🆘 Need Help?

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **GitHub Issues**: [github.com/tylerwang3275/EdgeFinder/issues](https://github.com/tylerwang3275/EdgeFinder/issues)
- **TheOddsAPI**: [theoddsapi.com](https://theoddsapi.com)

---

**Your EdgeFinder is ready to go live! 🚀📈**
