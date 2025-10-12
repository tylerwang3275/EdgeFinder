# 🔧 Environment Variable Fix for Render

## 🎯 **The Problem**

The `SPORTS_FILTER` environment variable on Render is being set incorrectly, causing the app to not load real data.

## 🚀 **The Solution**

You need to update the environment variable on Render with the correct format:

### Step 1: Go to Render Dashboard
1. Open [render.com](https://render.com) and sign in
2. Find your **"edgefinder"** service and click on it
3. Go to the **"Environment"** tab

### Step 2: Fix the SPORTS_FILTER Variable

**Current (incorrect):**
```
SPORTS_FILTER = SPORTS_FILTER = baseball_mlb,americanfootball_nfl,basketball_nba,icehockey_nhl,soccer_epl
```

**Should be (correct):**
```
SPORTS_FILTER = baseball_mlb,americanfootball_nfl,basketball_nba,icehockey_nhl,soccer_epl
```

### Step 3: Verify All Environment Variables

Make sure these are set correctly:

| Variable | Value |
|----------|-------|
| `ODDS_API_KEY` | `d98557c1e7c0485b02c4a0389890d6db` |
| `USE_FIXTURES` | `false` |
| `SPORTS_FILTER` | `baseball_mlb,americanfootball_nfl,basketball_nba,icehockey_nhl,soccer_epl` |

### Step 4: Save and Wait

1. **Save** the environment variables
2. **Wait 2-3 minutes** for the deployment to complete
3. **Test** your site

## 🧪 **Test After Fix**

Once you've fixed the environment variable:

```bash
# Check debug endpoint (should show correct sport keys)
curl https://edgefinder-czi3.onrender.com/debug

# Check if data is loading
curl https://edgefinder-czi3.onrender.com/api/latest

# Web interface
# Open: https://edgefinder-czi3.onrender.com
```

## 🎉 **Expected Results**

After the fix, your EdgeFinder will show:

- ✅ **Real MLB games** (Seattle Mariners vs Toronto Blue Jays!)
- ✅ **Seattle Seahawks** analysis
- ✅ **Live betting odds** from multiple sportsbooks
- ✅ **Discrepancy analysis** between prediction markets and sportsbooks
- ✅ **Professional betting edge analysis**

---

**The key is to remove the duplicate "SPORTS_FILTER =" prefix from the environment variable value!**
