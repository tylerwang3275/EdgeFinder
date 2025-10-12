# 🚀 **Render Environment Variables Update Guide**

## 🎯 **Quick Fix to See Your EdgeFinder in Action**

### **Step 1: Go to Render Dashboard**
1. Open [render.com](https://render.com) and sign in
2. Find your **"edgefinder"** service and click on it
3. Go to the **"Environment"** tab

### **Step 2: Update Environment Variables**

Update these variables to the following values:

| Variable | Current Value | New Value |
|----------|---------------|-----------|
| `USE_FIXTURES` | `false` | `true` |
| `ODDS_API_KEY` | `d98557c1e7c0485b02c4a0389890d6db` | `d98557c1e7c0485b02c4a0389890d6db` |
| `SPORTS_FILTER` | `baseball_mlb,americanfootball_nfl,basketball_nba,icehockey_nhl,soccer_epl` | `baseball_mlb,americanfootball_nfl,basketball_nba,icehockey_nhl,soccer_epl` |

### **Step 3: Optional - Add Kalshi API Key (for real prediction market data)**

If you want to use real prediction market data instead of fixtures:

| Variable | Value |
|----------|-------|
| `KALSHI_API_KEY` | `your_kalshi_api_key_here` |

**Note:** Kalshi API requires registration at [kalshi.com](https://kalshi.com)

### **Step 4: Save and Wait**

1. **Save** all environment variables
2. **Wait 2-3 minutes** for the deployment to complete
3. **Test** your site

## 🧪 **Test After Update**

```bash
# Check debug endpoint
curl https://edgefinder-czi3.onrender.com/debug

# Check if data is loading
curl https://edgefinder-czi3.onrender.com/api/latest

# Web interface
# Open: https://edgefinder-czi3.onrender.com
```

## 🎉 **Expected Results**

After setting `USE_FIXTURES=true`, your EdgeFinder will show:

### **✅ Real Analysis with Demo Data:**
- **3 matched games** (Seattle Seahawks, Mariners, Lakers)
- **Discrepancy analysis** between prediction markets and sportsbooks
- **Seattle hometown picks** section
- **Professional betting edge analysis**
- **Volume and payout calculations**

### **📊 Sample Output:**
```
# EdgeFinder: Sports vs Prediction Markets

**Summary:** 3 matched games, 5 markets, 6 book odds

## Biggest Discrepancies

| Rank | Sport | Game | Pred Prob | Books | Discrepancy | Volume | Payout |
|------|-------|------|-----------|-------|-------------|--------|--------|
| 1 | BASEBALL_MLB | diamondbacks @ astros | 0.380 | 0.400/0.521/0.643 | 0.141 | 800 | 1.6x |
| 2 | BASKETBALL_NBA | lakers @ nuggets | 0.620 | 0.524/0.524/0.524 | 0.096 | 2,000 | 0.6x |
| 3 | AMERICANFOOTBALL_NFL | seahawks @ 49ers | 0.450 | 0.455/0.519/0.583 | 0.069 | 1,500 | 1.2x |

## Seattle Hometown Pick

🏈 **Seattle Seahawks vs San Francisco 49ers**
- **Prediction Market:** 45% (Seahawks win)
- **Sportsbook Average:** 51.9%
- **Edge:** 6.9% discrepancy
- **Volume:** $1,500
- **Payout:** 1.2x
```

## 🔄 **Switching Back to Real Data**

To use real data instead of fixtures:

1. Set `USE_FIXTURES=false`
2. Add `KALSHI_API_KEY=your_actual_key`
3. Save and wait for deployment

---

**The key change is setting `USE_FIXTURES=true` to see your EdgeFinder in action with demo data!**
