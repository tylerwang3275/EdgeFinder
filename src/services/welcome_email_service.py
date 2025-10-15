"""
Welcome email service for new newsletter subscribers.
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os


class WelcomeEmailService:
    """Service for sending welcome emails to new subscribers."""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "")
        self.sender_password = os.getenv("SENDER_PASSWORD", "")
        self.sender_name = os.getenv("SENDER_NAME", "EdgeFinder")
    
    def send_welcome_email(self, recipient_email: str, recipient_location: str) -> bool:
        """Send welcome email to a new subscriber."""
        try:
            # Extract first name from email (everything before @)
            first_name = recipient_email.split('@')[0].title()
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "🎉 Welcome to EdgeFinder! Here's Your First Sneak Peek"
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = recipient_email
            
            # Create HTML content
            html_content = self._create_welcome_html(first_name, recipient_location)
            text_content = self._create_welcome_text(first_name, recipient_location)
            
            # Attach parts
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            if not self.sender_email or not self.sender_password:
                print("⚠️ Email credentials not configured. Skipping welcome email send.")
                return False
            
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Welcome email sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send welcome email to {recipient_email}: {e}")
            return False
    
    def _create_welcome_html(self, first_name: str, location: str) -> str:
        """Create HTML welcome email content."""
        # Determine hometown team based on location
        hometown_team = self._get_hometown_team(location)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to EdgeFinder</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 2.5em;
                    font-weight: bold;
                }}
                .section {{
                    margin: 30px 0;
                    padding: 20px;
                    border-left: 4px solid #667eea;
                    background-color: #f8f9fa;
                    border-radius: 5px;
                }}
                .section h2 {{
                    color: #667eea;
                    margin-top: 0;
                    font-size: 1.8em;
                }}
                .sample-box {{
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 15px 0;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .odds-comparison {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin: 10px 0;
                }}
                .robinhood-odds {{
                    color: #00d4aa;
                    font-weight: bold;
                }}
                .sportsbook-odds {{
                    color: #ff6b6b;
                    font-weight: bold;
                }}
                .discrepancy {{
                    color: #ffa726;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border-radius: 10px;
                    color: #666;
                }}
                .highlight {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    color: #856404;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 EdgeFinder</h1>
                    <p>Welcome to the Future of Sports Betting Intelligence</p>
                </div>
                
                <p>Hi <strong>{first_name}</strong>,</p>
                
                <p>Welcome to EdgeFinder! 🎉 We're thrilled to have you on board.</p>
                
                <p>Every <strong>Monday, Thursday, and Saturday</strong>, we send out insights to help you find the best betting edges in sports, using Robinhood's prediction markets and top sportsbooks like DraftKings and FanDuel. Think of us as your sports betting guide, highlighting opportunities you won't find anywhere else!</p>
                
                <div class="section">
                    <h2>📊 What You Can Expect From Us</h2>
                    <ul>
                        <li><strong>Best Odds:</strong> The biggest discrepancies between Robinhood's prediction markets and sportsbooks.</li>
                        <li><strong>Most Popular:</strong> The most bet-on games (you know where the crowd's money is).</li>
                        <li><strong>Long Shot:</strong> The highest potential returns on Robinhood.</li>
                        <li><strong>Hometown Fav:</strong> Personalized picks for your city (yes, we've got {location} covered! 😉).</li>
                    </ul>
                </div>
                
                <div class="section">
                    <h2>🔍 Your First Sneak Peek: A Sample of This Week's Newsletter</h2>
                    
                    <div class="sample-box">
                        <h3>🏆 Best Odds</h3>
                        <h4>Lakers vs Warriors</h4>
                        <div class="odds-comparison">
                            <span><strong>Robinhood:</strong> <span class="robinhood-odds">54% (Lakers win)</span></span>
                            <span><strong>DraftKings:</strong> <span class="sportsbook-odds">48%</span></span>
                            <span><strong>Discrepancy:</strong> <span class="discrepancy">6%</span></span>
                        </div>
                        <p><strong>📊 Why this matters:</strong> If you're betting on the Lakers, Robinhood is giving you an extra edge. This could be an opportunity to find value that sportsbooks aren't offering.</p>
                    </div>
                    
                    <div class="sample-box">
                        <h3>📈 Most Popular</h3>
                        <h4>Cowboys vs Eagles</h4>
                        <p><strong>DraftKings:</strong> -4.5 (Cowboys)</p>
                        <p><strong>Most bet on:</strong> 32% of total handle</p>
                        <p><strong>📊 Why this matters:</strong> When the crowd picks a side, it often moves the line. You'll want to track this game closely as it could move fast.</p>
                    </div>
                    
                    <div class="sample-box">
                        <h3>💸 Long Shot</h3>
                        <h4>Chicago Bulls +550</h4>
                        <p><strong>Robinhood Price:</strong> 0.15 (15%)</p>
                        <p><strong>Potential Return:</strong> 5x+</p>
                        <p><strong>📊 Why this matters:</strong> Big payout for a low-likelihood bet. If you think the Bulls can upset, now's your chance to place your bet before the odds change.</p>
                    </div>
                    
                    <div class="sample-box">
                        <h3>💚 Hometown Fav ({location} Edition)</h3>
                        <h4>{hometown_team} vs Los Angeles Angels</h4>
                        <p><strong>Betting Volume:</strong> 10% more bets on {hometown_team}</p>
                        <p><strong>Robinhood Odds:</strong> 55% {hometown_team} win</p>
                        <p><strong>📊 Why this matters:</strong> {hometown_team} fans are putting their money on the home team! Robinhood is offering a solid probability here, and the local sentiment could be something to take advantage of.</p>
                    </div>
                </div>
                
                <div class="highlight">
                    <p><strong>That's just a small sample of what you'll get in each edition.</strong> Every newsletter gives you a mix of betting insights, tips, and hometown favorites — so you can bet smarter, not harder.</p>
                </div>
                
                <div class="section">
                    <h2>🚀 What's Next?</h2>
                    <p>Keep an eye on your inbox for our first full issue, coming this <strong>Monday</strong>!</p>
                    <p>In the meantime, feel free to check out the <a href="https://edgefinder-czi3.onrender.com/" style="color: #667eea;">EdgeFinder Dashboard</a> for the latest odds, trends, and predictions.</p>
                </div>
                
                <p>We're excited to have you with us and can't wait to help you find the edge in your betting strategy.</p>
                
                <p>If you have any questions or just want to chat about sports, feel free to reply to this email — I'm always here to help!</p>
                
                <div class="footer">
                    <p><strong>Welcome aboard,</strong></p>
                    <p><strong>Tyler Wang</strong><br>Founder @ EdgeFinder</p>
                    <p><em>P.S. Have a friend who loves sports betting? Share EdgeFinder with them and let them experience the same sharp insights!</em></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _create_welcome_text(self, first_name: str, location: str) -> str:
        """Create plain text welcome email content."""
        hometown_team = self._get_hometown_team(location)
        
        text = f"""
🎉 Welcome to EdgeFinder! Here's Your First Sneak Peek

Hi {first_name},

Welcome to EdgeFinder! 🎯 We're thrilled to have you on board.

Every Monday, Thursday, and Saturday, we send out insights to help you find the best betting edges in sports, using Robinhood's prediction markets and top sportsbooks like DraftKings and FanDuel. Think of us as your sports betting guide, highlighting opportunities you won't find anywhere else!

Here's what you can expect from us:

Best Odds: The biggest discrepancies between Robinhood's prediction markets and sportsbooks.

Most Popular: The most bet-on games (you know where the crowd's money is).

Long Shot: The highest potential returns on Robinhood.

Hometown Fav: Personalized picks for your city (yes, we've got {location} covered! 😉).

Your First Sneak Peek: A Sample of This Week's Newsletter

🏆 Best Odds
Lakers vs Warriors

Robinhood: 54% (Lakers win)
DraftKings: 48%
Discrepancy: 6%

📊 Why this matters: If you're betting on the Lakers, Robinhood is giving you an extra edge. This could be an opportunity to find value that sportsbooks aren't offering.

📈 Most Popular
Cowboys vs Eagles

DraftKings: -4.5 (Cowboys)
Most bet on: 32% of total handle

📊 Why this matters: When the crowd picks a side, it often moves the line. You'll want to track this game closely as it could move fast.

💸 Long Shot
Chicago Bulls +550

Robinhood Price: 0.15 (15%)
Potential Return: 5x+

📊 Why this matters: Big payout for a low-likelihood bet. If you think the Bulls can upset, now's your chance to place your bet before the odds change.

💚 Hometown Fav ({location} Edition)
{hometown_team} vs Los Angeles Angels

Betting Volume: 10% more bets on {hometown_team}
Robinhood Odds: 55% {hometown_team} win

📊 Why this matters: {hometown_team} fans are putting their money on the home team! Robinhood is offering a solid probability here, and the local sentiment could be something to take advantage of.

That's just a small sample of what you'll get in each edition. Every newsletter gives you a mix of betting insights, tips, and hometown favorites — so you can bet smarter, not harder.

What's Next?

Keep an eye on your inbox for our first full issue, coming this Monday!

In the meantime, feel free to check out the EdgeFinder Dashboard for the latest odds, trends, and predictions: https://edgefinder-czi3.onrender.com/

We're excited to have you with us and can't wait to help you find the edge in your betting strategy.

If you have any questions or just want to chat about sports, feel free to reply to this email — I'm always here to help!

Welcome aboard,
Tyler Wang
Founder @ EdgeFinder

P.S. Have a friend who loves sports betting? Share EdgeFinder with them and let them experience the same sharp insights!
        """
        
        return text
    
    def _get_hometown_team(self, location: str) -> str:
        """Get hometown team based on location."""
        location_lower = location.lower()
        
        if 'seattle' in location_lower:
            return 'Seattle Mariners'
        elif 'los angeles' in location_lower or 'la' in location_lower:
            return 'Los Angeles Lakers'
        elif 'new york' in location_lower or 'nyc' in location_lower:
            return 'New York Yankees'
        elif 'chicago' in location_lower:
            return 'Chicago Bulls'
        elif 'boston' in location_lower:
            return 'Boston Celtics'
        elif 'philadelphia' in location_lower or 'philly' in location_lower:
            return 'Philadelphia Eagles'
        elif 'dallas' in location_lower:
            return 'Dallas Cowboys'
        elif 'san francisco' in location_lower or 'sf' in location_lower:
            return 'San Francisco 49ers'
        elif 'miami' in location_lower:
            return 'Miami Heat'
        elif 'denver' in location_lower:
            return 'Denver Broncos'
        else:
            return 'Your Local Team'
