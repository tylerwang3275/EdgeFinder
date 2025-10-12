# 🚀 **Add Kalshi API Credentials to Render**

## 🎯 **Step-by-Step Guide**

### **Step 1: Go to Render Dashboard**
1. **Open [render.com](https://render.com)** and sign in
2. **Find your "edgefinder" service** and click on it
3. **Go to the "Environment" tab**

### **Step 2: Add Kalshi API Credentials**

Add these **new environment variables**:

| Variable Name | Value |
|---------------|-------|
| `KALSHI_API_KEY_ID` | `f178b0a4-438a-47e2-b01b-25c357e48c5c` |
| `KALSHI_PRIVATE_KEY` | `-----BEGIN RSA PRIVATE KEY-----<br/>MIIEowIBAAKCAQEAuxEifsJZu8uTh4Rvj5ETl5pfj7dDhOwLZ55z4R3mWu6jI0UH<br/>RAgy26w/GMpyuG2T2MlMKeed+CGvHhYPadRUx1TmdHBIFEe7tyRDbTs/FTWvfHx/<br/>nVrpjLthfP/H+cuARvx7+DNqnFBw0KVbkKHsiu6FMWGzSWWPhYqEO6xAWBfEi55S<br/>NcEBX1dgS1Q6RTIjuu9a3guJ/T6cWVe9UcUVlq34srOKWkYdQndkhYLeXNdEX8O5<br/>370l/AcSRNoB92lo9avvq50B1gvc05M1A0yoBBbuh+y96z6EKtrKg8QlcgXiBLmB<br/>BdB4Ytge0ginhENcbinq5IAend5Vv/gq1r9eKwIDAQABAoIBAF9JmB+nkhvl0+1Y<br/>2Zbw2GEGAp1rRZpkvl52ySInn9o76p+hntTZtEZPlAhlv1AQiRoJV6GU2NO3HMOf<br/>ixRmUxUCOy2esCicbZMZhrsSTczY/t3TcRHPaF4GaN9KTyv/rAT8wY0pa6naE81E<br/>HcMrqBkQ7Im98Zx2fkgQydC3qkL0YGQJVXzLsOcYbW46/1EkbwWdN5cxcuN6vZbd<br/>19iXCnnjgYrlhPxM1Dkt6419FIxJaqYTzG06X631JQElC06WGmXE3OM1Vw38k+1O<br/>oLHwt8UsD3bLbopr1GWjZKHgQVzXGFFPi9VjDlghFwDW1lwAR42yfjYDxKDxAX0N<br/>sz3edvECgYEAxk5mvH/T4Q4o5Rx+gsRg3gwrwiZj/Tgth4EZMWbUbFNOZFTVePHl<br/>X8zXREw0pE4A6EKAqD/yCWcJche3HF3ze+cre+pHWMc21bxeZ+6wLs0ipRvlv+kw<br/>bnZYEDUfFdVgGyDm04Fdl/eqUplG7JK6ly2/QVDRnFjxLpViXq4tlRMCgYEA8X2k<br/>lu3QP6r6YHnWfquaM/Hklc7QM0sdwc4C2VIs39Nbz5xpcAQsjyA6JrdLnoNyKaiy<br/>PH3G8sU4QJHqlUQs4BMhr8LhxVhE66dDikKHCM1IWEbxYS3c3JIWiZYxhEncnxBc<br/>8uFQ5jT/QZMOMSvPflcrQG3eO66n4xt4DIBI7YkCgYA/QXkB/eBvNJ4U3y73tX6U<br/>tdsrdiWE+2uCgsqveHagCz7BQFJL3xVkpqmwDoLoOj2N2NDDWopxN13K+Aef09Q8<br/>HLRBNa0Gg51ZNloC2x91/ldjxW9W9SJOyg8zNE6zHzolzSv0IZriQ80fxebaxb8h<br/>RCVyxz3lmnVsf5g+TV8a4wKBgQCi+o7IJbu0HGpaDiBK4PlzMT96M1ekJn/wul6F<br/>2MXcUULXPNKT/N0twyw70NzCICg+IVIZLTHFyoCKY3AUSSyYFZFYk4fXrhjlib81<br/>YmzL7e9zVH23fkJewmFfffPxOgAhgeOZL6NvmjjjQqIDYXPp6l6QXxXq5Zb82R8O<br/>IM4XMQKBgB9LP14ukqB+LmKNJEqOks+0MJOITPf5swh/hZKKxPm6lpIyLbaYqnAb<br/>DV94L3EfcdMmDe0KEuGCdSo9+RNCeSAbhsQa8gjhS8ZV+8sYf2exnLTFNS9bgyWS<br/>Pn9qglHT+2QbE7uGWDZkf2acgvisdqwe/M21VmcK4W6cV0hum5b8<br/>-----END RSA PRIVATE KEY-----` |

### **Step 3: Update Existing Variables**

Make sure these are set correctly:

| Variable | Value |
|----------|-------|
| `USE_FIXTURES` | `false` |
| `ODDS_API_KEY` | `d98557c1e7c0485b02c4a0389890d6db` |
| `SPORTS_FILTER` | `baseball_mlb,americanfootball_nfl,basketball_nba,icehockey_nhl,soccer_epl` |

### **Step 4: Save and Wait**

1. **Save** all environment variables
2. **Wait 3-5 minutes** for the deployment to complete
3. **Test** your site

## 🧪 **Test Your Live Site**

After adding the credentials:

```bash
# Test Kalshi connection
curl https://edgefinder-czi3.onrender.com/debug/kalshi

# Check if real data is loading
curl https://edgefinder-czi3.onrender.com/api/latest

# Web interface
# Open: https://edgefinder-czi3.onrender.com
```

## 🎉 **Expected Results**

With real Kalshi data, your EdgeFinder will show:

- ✅ **Real prediction market prices** from Kalshi
- ✅ **Live sportsbook odds** from TheOddsAPI  
- ✅ **Actual discrepancy analysis** between markets
- ✅ **Real betting edges** and opportunities
- ✅ **Current market sentiment** and volume

## 🔧 **Important Notes**

### **Private Key Format:**
- **Copy the ENTIRE private key** including the `-----BEGIN` and `-----END` lines
- **Keep all line breaks** - don't compress it into one line
- **The key should be exactly as provided** above

### **Security:**
- These credentials are now stored securely on Render
- The private key is used to generate JWT tokens for API access
- Tokens expire after 1 hour and are automatically renewed

## 🚨 **Troubleshooting**

### **If you get authentication errors:**
1. **Check the private key format** - make sure it includes the BEGIN/END lines
2. **Verify the API key ID** is correct
3. **Wait a few minutes** for the deployment to complete

### **If you still see "0 matched games":**
1. **Check the debug endpoint** to see if Kalshi is connecting
2. **Verify USE_FIXTURES=false** is set
3. **The API might be slow** - try refreshing after a few minutes

---

**Once you've added these credentials, your EdgeFinder will have access to real prediction market data from Kalshi!**
