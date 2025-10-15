# EdgeFinder Deployment Troubleshooting Guide

## 🚨 Current Issue: 502 Bad Gateway

Your website is showing a "502 Bad Gateway" error, which means Render can't start your application.

## 🔍 Possible Causes & Solutions

### 1. **Missing Environment Variables** (Most Likely)
The email system requires these environment variables to be set on Render:

**Go to Render Dashboard → Your Service → Environment Tab → Add these:**

```
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
SENDER_EMAIL = edgefindernews@gmail.com
SENDER_PASSWORD = ufzn fneg awxz jivh
SENDER_NAME = EdgeFinder
```

**Steps:**
1. Visit: https://dashboard.render.com/
2. Click on your EdgeFinder service
3. Go to "Environment" tab
4. Add each variable one by one
5. Click "Save Changes"
6. Wait for automatic redeploy

### 2. **Application Startup Issues**
If environment variables are set but still getting 502:

**Check Render Logs:**
1. Go to your service on Render Dashboard
2. Click "Logs" tab
3. Look for error messages during startup

**Common startup errors:**
- Import errors
- Missing dependencies
- Port binding issues

### 3. **Resource Constraints**
Render's free tier has limitations:
- **Memory**: 512MB RAM
- **CPU**: Limited processing power
- **Sleep**: Apps sleep after 15 minutes of inactivity

**Solutions:**
- Upgrade to paid plan for better performance
- Optimize your application for lower memory usage

### 4. **Build Issues**
Check if the build is completing successfully:

**In Render Dashboard:**
1. Go to "Deploys" tab
2. Check if latest deploy shows "Live" status
3. If "Failed", click on it to see build logs

## 🛠️ Quick Fixes to Try

### Fix 1: Add Environment Variables
This is the most likely solution. Add all 5 email environment variables listed above.

### Fix 2: Check Build Logs
1. Go to Render Dashboard
2. Click "Deploys" tab
3. Look for any failed builds
4. Check build logs for errors

### Fix 3: Manual Redeploy
1. Go to your service on Render Dashboard
2. Click "Manual Deploy" → "Deploy latest commit"
3. Wait for deployment to complete

### Fix 4: Check Application Logs
1. Go to your service on Render Dashboard
2. Click "Logs" tab
3. Look for runtime errors

## 📊 Expected Behavior After Fix

Once the environment variables are added and the app redeploys:

1. **Website loads successfully** (no more 502 error)
2. **Newsletter signup works** (no more timeouts)
3. **Welcome emails are sent** immediately after signup
4. **Weekly newsletters** sent on Monday, Thursday, Saturday

## 🧪 Testing the Fix

After adding environment variables and redeploying:

1. **Visit your website**: https://edgefinder-czi3.onrender.com/
2. **Test newsletter signup** using the form
3. **Check your email** for welcome message
4. **Verify no more 502 errors**

## 📞 If Still Not Working

If you're still getting 502 errors after adding environment variables:

1. **Check Render logs** for specific error messages
2. **Try manual redeploy** from Render dashboard
3. **Consider upgrading** to Render's paid plan for better reliability
4. **Contact Render support** if the issue persists

## 🎯 The Root Cause

The newsletter signup system tries to send welcome emails immediately, but without the SMTP environment variables configured, the email sending process hangs, causing the entire request to timeout and eventually crash the application.

**Adding the environment variables will fix this issue completely.**
