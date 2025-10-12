# 🚀 **Kalshi API Setup Guide**

## 🎯 **Getting Live Prediction Market Data**

### **Step 1: Sign Up for Kalshi**

1. **Go to [kalshi.com](https://kalshi.com)**
2. **Click "Sign Up"** and create an account
3. **Complete identity verification** (required for API access)
4. **Verify your email and phone number**

### **Step 2: Request API Access**

1. **Log into your Kalshi account**
2. **Go to Account Settings** or **Developer Section**
3. **Look for "API Access" or "Developer Tools"**
4. **Request API access** - you may need to:
   - Provide your use case (sports betting analysis)
   - Explain how you'll use the data
   - Wait for approval (can take 1-7 days)

### **Step 3: Get Your API Key**

Once approved:
1. **Navigate to API section** in your account
2. **Generate an API key** or **access token**
3. **Copy the key** (it might look like: `Bearer abc123...` or just `abc123...`)

### **Step 4: Add to Render**

1. **Go to [render.com](https://render.com)** and sign in
2. **Find your "edgefinder" service** and click on it
3. **Go to "Environment" tab**
4. **Add new environment variable:**
   - **Name:** `KALSHI_API_KEY`
   - **Value:** `your_actual_api_key_here`
5. **Set `USE_FIXTURES=false`** to use real data
6. **Save and wait 2-3 minutes**

## 🧪 **Test Your Setup**

After adding the API key, test the connection:

```bash
# Test Kalshi connection
curl https://edgefinder-czi3.onrender.com/debug/kalshi

# Check if real data is loading
curl https://edgefinder-czi3.onrender.com/api/latest
```

## 🔄 **Alternative: Use Public Kalshi Data**

If API access is taking too long, we can try to use public Kalshi data:

### **Option 1: Kalshi Public Markets**
- Some Kalshi markets are publicly accessible
- We can scrape or use public endpoints
- Limited data but still useful

### **Option 2: Other Prediction Markets**
- **Polymarket** - has public API
- **PredictIt** - has some public data
- **Manifold Markets** - open source

## 🎉 **Expected Results with Real Kalshi Data**

Once connected, your EdgeFinder will show:

- ✅ **Real prediction market prices** from Kalshi
- ✅ **Live sportsbook odds** from TheOddsAPI
- ✅ **Actual discrepancy analysis** between markets
- ✅ **Real betting edges** and opportunities
- ✅ **Current market sentiment** and volume

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **"API key not valid"**
   - Check if the key is correct
   - Make sure it includes "Bearer " prefix if needed
   - Verify the key hasn't expired

2. **"Access denied"**
   - API access might not be approved yet
   - Check your Kalshi account status
   - Contact Kalshi support

3. **"Rate limit exceeded"**
   - Kalshi has API rate limits
   - We'll implement caching to reduce calls

### **Fallback Options:**

If Kalshi API doesn't work:
1. **Keep `USE_FIXTURES=true`** for demo purposes
2. **Try other prediction market APIs**
3. **Use public market data sources**

## 📞 **Need Help?**

- **Kalshi Support:** Contact through their website
- **API Documentation:** Check Kalshi's developer docs
- **Community:** Join Kalshi Discord or forums

---

**The key is getting API access from Kalshi and adding the key to your Render environment variables!**
