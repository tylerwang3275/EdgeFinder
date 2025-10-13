# EdgeFinder Newsletter System Setup Guide

## 🎉 Newsletter System Features

The EdgeFinder newsletter system is now fully implemented with the following features:

### ✅ **Completed Features:**
- **Newsletter Signup Modal** - Appears after 10 seconds on first visit
- **Location-Based Personalization** - Hometown picks based on user location
- **Comprehensive Email Templates** - Both HTML and text versions
- **Weekly Automation** - Scheduled to send every Monday at 9:00 AM
- **Admin Management** - Endpoints to view subscribers and send newsletters
- **Data Storage** - File-based subscription management

### 📧 **Email Content Sections:**
1. **Best Robinhood Opportunities** - Games with largest discrepancies
2. **Most Popular on Robinhood** - Highest volume games
3. **Biggest Payout** - Best payout ratios
4. **Hometown Favorite** - Personalized picks based on user location

## 🚀 **How to Use the Newsletter System**

### **For Users:**
1. Visit the EdgeFinder website
2. Newsletter signup modal appears automatically after 10 seconds
3. Enter email and hometown location
4. Agree to terms and subscribe
5. Receive weekly personalized reports

### **For Administrators:**

#### **View Subscribers:**
```bash
curl https://edgefinder-czi3.onrender.com/api/newsletter/subscribers
```

#### **Send Weekly Newsletter:**
```bash
curl -X POST https://edgefinder-czi3.onrender.com/api/newsletter/send
```

#### **Preview Newsletter Content:**
```bash
curl https://edgefinder-czi3.onrender.com/api/newsletter/preview
```

## ⚙️ **Email Configuration (Optional)**

To enable actual email sending, configure these environment variables on Render:

### **Gmail Setup:**
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SENDER_NAME=EdgeFinder
```

### **Other Email Providers:**
- **Outlook/Hotmail:** `smtp-mail.outlook.com:587`
- **Yahoo:** `smtp.mail.yahoo.com:587`
- **Custom SMTP:** Use your provider's settings

### **Gmail App Password Setup:**
1. Enable 2-factor authentication on Gmail
2. Go to Google Account settings
3. Security → App passwords
4. Generate app password for "Mail"
5. Use this password (not your regular password)

## 📊 **Newsletter Data Structure**

The newsletter includes:

```json
{
  "total_games": 15,
  "total_markets": 15,
  "total_books": 15,
  "best_opportunities": [
    {
      "game": "Seattle Seahawks @ San Francisco 49ers",
      "time": "10/15 1:00 PM",
      "sport": "NFL",
      "robinhoodAway": "42.0%",
      "robinhoodHome": "58.0%",
      "sportsbookAway": "+115",
      "sportsbookHome": "-135",
      "awayPayout": "2.4x",
      "homePayout": "1.7x",
      "discrepancy": "5.2%",
      "volume": "2,500"
    }
  ],
  "most_popular": [...],
  "hometown_pick": {...}
}
```

## 🔧 **Technical Implementation**

### **Files Created:**
- `src/models/newsletter.py` - Subscription data models
- `src/services/email_service.py` - Email sending service
- `src/services/newsletter_generator.py` - Report generation
- `src/scheduler/newsletter_scheduler.py` - Weekly automation
- `templates/index.html` - Updated with signup modal
- `static/js/app.js` - Newsletter signup functionality

### **API Endpoints:**
- `POST /api/newsletter/subscribe` - User subscription
- `GET /api/newsletter/subscribers` - View all subscribers
- `POST /api/newsletter/send` - Send weekly newsletter
- `GET /api/newsletter/preview` - Preview newsletter content

### **Data Storage:**
- Subscriptions stored in `data/newsletter_subscriptions.json`
- Includes email, location, subscription date, and last email sent

## 🎯 **Newsletter Automation**

### **Scheduling:**
- **Production:** Every Monday at 9:00 AM
- **Testing:** Daily at 2:00 PM (remove in production)

### **To Run Scheduler:**
```bash
python src/scheduler/newsletter_scheduler.py
```

### **Manual Newsletter Send:**
```bash
curl -X POST https://edgefinder-czi3.onrender.com/api/newsletter/send
```

## 🧪 **Testing**

Run the comprehensive test suite:
```bash
python test_newsletter_system.py
```

This tests:
- ✅ Subscription system
- ✅ Report generation
- ✅ Email templates
- ✅ Complete newsletter flow

## 📈 **Analytics & Monitoring**

### **Track Newsletter Performance:**
- Monitor subscriber count via `/api/newsletter/subscribers`
- Check email send success via `/api/newsletter/send` response
- Review logs for delivery issues

### **Subscriber Growth:**
- Newsletter modal appears on first visit
- Users can subscribe via navbar button
- Location-based personalization increases engagement

## 🚨 **Important Notes**

### **Email Limits:**
- Gmail: 500 emails/day (free), 2000/day (paid)
- Consider upgrading for large subscriber bases
- Monitor sending limits to avoid blocks

### **Compliance:**
- Newsletter includes unsubscribe option
- Terms agreement required for subscription
- Disclaimer included in all emails

### **Backup:**
- Subscriber data stored in JSON file
- Consider database migration for production scale
- Regular backups recommended

## 🎊 **Success!**

Your EdgeFinder newsletter system is now fully operational! Users can:
- ✅ Sign up for weekly reports
- ✅ Receive personalized hometown picks
- ✅ Get the best Robinhood opportunities
- ✅ See most popular games and biggest payouts

The system automatically generates fresh data each week and sends beautiful, personalized emails to all subscribers.

---

**Next Steps:**
1. Configure email credentials on Render (optional)
2. Monitor subscriber growth
3. Consider adding more sports or markets
4. Set up analytics tracking
5. Scale to database storage if needed
