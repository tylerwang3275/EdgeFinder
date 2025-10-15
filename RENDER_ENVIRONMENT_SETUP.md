# Render Environment Variables Setup

## 🚨 Issue Identified
The newsletter signup emails are not working because the email environment variables are not configured on your Render deployment.

## ✅ Solution
You need to add these environment variables to your Render deployment:

### Required Environment Variables:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=edgefindernews@gmail.com
SENDER_PASSWORD=ufzn fneg awxz jivh
SENDER_NAME=EdgeFinder
```

## 📋 How to Add Environment Variables on Render:

1. **Go to your Render Dashboard**
   - Visit: https://dashboard.render.com/
   - Find your EdgeFinder service

2. **Navigate to Environment Tab**
   - Click on your EdgeFinder service
   - Go to the "Environment" tab

3. **Add Each Variable**
   - Click "Add Environment Variable"
   - Add each variable one by one:
     - **Key**: `SMTP_SERVER` **Value**: `smtp.gmail.com`
     - **Key**: `SMTP_PORT` **Value**: `587`
     - **Key**: `SENDER_EMAIL` **Value**: `edgefindernews@gmail.com`
     - **Key**: `SENDER_PASSWORD` **Value**: `ufzn fneg awxz jivh`
     - **Key**: `SENDER_NAME` **Value**: `EdgeFinder`

4. **Save and Redeploy**
   - Click "Save Changes"
   - Render will automatically redeploy your service

## ✅ Verification
After adding the environment variables and redeploying:

1. **Test the newsletter signup** on your website
2. **Check your email** for the welcome message
3. **The email should arrive immediately** after signup

## 🔧 Local Testing
To test locally, run:
```bash
SMTP_SERVER=smtp.gmail.com SMTP_PORT=587 SENDER_EMAIL=edgefindernews@gmail.com SENDER_PASSWORD="ufzn fneg awxz jivh" SENDER_NAME=EdgeFinder python test_welcome_email_send.py
```

## 📧 What the Welcome Email Contains:
- **Personalized greeting** with the user's name
- **Live sports data** from your website
- **Sample newsletter preview** with real odds comparisons
- **Hometown team picks** based on user location
- **Professional HTML formatting** with styling

## 🎯 Expected Behavior:
1. User signs up for newsletter on website
2. **Immediate welcome email** is sent (within seconds)
3. **Weekly newsletters** sent on Monday, Thursday, Saturday
4. **All emails include live data** from your sports APIs

---

**The email system is working perfectly - it just needs the environment variables configured on Render!**
