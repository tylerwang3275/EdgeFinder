"""
Email service for sending newsletter reports.
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from pathlib import Path


class EmailService:
    """Service for sending email newsletters."""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "")
        self.sender_password = os.getenv("SENDER_PASSWORD", "")
        self.sender_name = os.getenv("SENDER_NAME", "EdgeFinder")
    
    def send_newsletter(self, recipient_email: str, recipient_location: str, report_data: Dict[str, Any]) -> bool:
        """Send newsletter email to a recipient."""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"EdgeFinder Weekly Report - {datetime.now().strftime('%B %d, %Y')}"
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = recipient_email
            
            # Create HTML content
            html_content = self._create_html_newsletter(recipient_email, recipient_location, report_data)
            text_content = self._create_text_newsletter(recipient_email, recipient_location, report_data)
            
            # Attach parts
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            if not self.sender_email or not self.sender_password:
                print("⚠️ Email credentials not configured. Skipping email send.")
                return False
            
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Newsletter sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send newsletter to {recipient_email}: {e}")
            return False
    
    def _create_html_newsletter(self, recipient_email: str, recipient_location: str, report_data: Dict[str, Any]) -> str:
        """Create HTML newsletter content."""
        current_date = datetime.now().strftime('%B %d, %Y')
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>EdgeFinder Weekly Report</title>
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
                .header p {{
                    margin: 10px 0 0 0;
                    font-size: 1.2em;
                    opacity: 0.9;
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
                .game-row {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 15px;
                    margin: 10px 0;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .game-info {{
                    flex: 1;
                }}
                .game-title {{
                    font-weight: bold;
                    font-size: 1.1em;
                    color: #333;
                }}
                .game-time {{
                    color: #666;
                    font-size: 0.9em;
                }}
                .odds-info {{
                    text-align: right;
                    min-width: 200px;
                }}
                .robinhood-odds {{
                    color: #00d4aa;
                    font-weight: bold;
                }}
                .sportsbook-odds {{
                    color: #ff6b6b;
                    font-weight: bold;
                }}
                .payout {{
                    color: #4ecdc4;
                    font-weight: bold;
                }}
                .discrepancy {{
                    color: #ffa726;
                    font-weight: bold;
                }}
                .volume {{
                    color: #9c27b0;
                    font-weight: bold;
                }}
                .hometown-section {{
                    background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%);
                    color: white;
                    border-left: none;
                }}
                .hometown-section h2 {{
                    color: white;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border-radius: 10px;
                    color: #666;
                }}
                .disclaimer {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    color: #856404;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .stats {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .stat-card {{
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .stat-number {{
                    font-size: 2em;
                    font-weight: bold;
                    color: #667eea;
                }}
                .stat-label {{
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 EdgeFinder</h1>
                    <p>Weekly Robinhood vs Sportsbooks Report</p>
                    <p>{current_date}</p>
                </div>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{report_data.get('total_games', 0)}</div>
                        <div class="stat-label">Total Games</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{report_data.get('total_markets', 0)}</div>
                        <div class="stat-label">Robinhood Markets</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{report_data.get('total_books', 0)}</div>
                        <div class="stat-label">Sportsbooks</div>
                    </div>
                </div>
        """
        
        # Add Best Robinhood Opportunities section
        if report_data.get('best_opportunities'):
            html += """
                <div class="section">
                    <h2>🏆 Best Robinhood Opportunities</h2>
                    <p>Games with the largest differences between Robinhood prediction markets and sportsbooks</p>
            """
            
            for game in report_data['best_opportunities'][:5]:  # Top 5
                html += f"""
                    <div class="game-row">
                        <div class="game-info">
                            <div class="game-title">{game.get('game', 'N/A')}</div>
                            <div class="game-time">{game.get('time', 'N/A')} • {game.get('sport', 'N/A')}</div>
                        </div>
                        <div class="odds-info">
                            <div>Robinhood: <span class="robinhood-odds">{game.get('robinhoodAway', 'N/A')} / {game.get('robinhoodHome', 'N/A')}</span></div>
                            <div>Sportsbook: <span class="sportsbook-odds">{game.get('sportsbookAway', 'N/A')} / {game.get('sportsbookHome', 'N/A')}</span></div>
                            <div>Payout: <span class="payout">{game.get('awayPayout', 'N/A')}x / {game.get('homePayout', 'N/A')}x</span></div>
                            <div>Discrepancy: <span class="discrepancy">{game.get('discrepancy', 'N/A')}</span></div>
                        </div>
                    </div>
                """
            
            html += "</div>"
        
        # Add Most Popular section
        if report_data.get('most_popular'):
            html += """
                <div class="section">
                    <h2>🔥 Most Popular on Robinhood</h2>
                    <p>Games with the highest Robinhood prediction market volume</p>
            """
            
            for game in report_data['most_popular'][:5]:  # Top 5
                html += f"""
                    <div class="game-row">
                        <div class="game-info">
                            <div class="game-title">{game.get('game', 'N/A')}</div>
                            <div class="game-time">{game.get('time', 'N/A')} • {game.get('sport', 'N/A')}</div>
                        </div>
                        <div class="odds-info">
                            <div>Volume: <span class="volume">{game.get('volume', 'N/A')}</span></div>
                            <div>Robinhood: <span class="robinhood-odds">{game.get('robinhoodAway', 'N/A')} / {game.get('robinhoodHome', 'N/A')}</span></div>
                            <div>Payout: <span class="payout">{game.get('awayPayout', 'N/A')}x / {game.get('homePayout', 'N/A')}x</span></div>
                        </div>
                    </div>
                """
            
            html += "</div>"
        
        # Add Hometown Favorite section
        if report_data.get('hometown_pick'):
            html += f"""
                <div class="section hometown-section">
                    <h2>🏠 Hometown Favorite: {recipient_location}</h2>
                    <p>Your local team's best opportunity this week</p>
            """
            
            hometown = report_data['hometown_pick']
            html += f"""
                    <div class="game-row" style="background-color: rgba(255,255,255,0.1); color: white;">
                        <div class="game-info">
                            <div class="game-title" style="color: white;">{hometown.get('game', 'N/A')}</div>
                            <div class="game-time" style="color: rgba(255,255,255,0.8);">{hometown.get('time', 'N/A')}</div>
                        </div>
                        <div class="odds-info">
                            <div>Robinhood: <span style="color: #00d4aa;">{hometown.get('robinhoodAway', 'N/A')} / {hometown.get('robinhoodHome', 'N/A')}</span></div>
                            <div>Sportsbook: <span style="color: #ff6b6b;">{hometown.get('sportsbookAway', 'N/A')} / {hometown.get('sportsbookHome', 'N/A')}</span></div>
                            <div>Payout: <span style="color: #4ecdc4;">{hometown.get('awayPayout', 'N/A')}x / {hometown.get('homePayout', 'N/A')}x</span></div>
                            <div>Volume: <span style="color: #9c27b0;">{hometown.get('volume', 'N/A')}</span></div>
                        </div>
                    </div>
            """
            
            html += "</div>"
        
        # Add disclaimer and footer
        html += f"""
                <div class="disclaimer">
                    <strong>⚠️ Disclaimer:</strong> This newsletter is for informational purposes only. 
                    Sports betting involves risk and may not be legal in all jurisdictions. 
                    Please gamble responsibly and within your means.
                </div>
                
                <div class="footer">
                    <p><strong>EdgeFinder Newsletter</strong></p>
                    <p>Delivered to: {recipient_email}</p>
                    <p>Your location: {recipient_location}</p>
                    <p>Generated on {current_date}</p>
                    <p>
                        <a href="#" style="color: #667eea;">Unsubscribe</a> | 
                        <a href="https://edgefinder-czi3.onrender.com/" style="color: #667eea;">Visit EdgeFinder</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _create_text_newsletter(self, recipient_email: str, recipient_location: str, report_data: Dict[str, Any]) -> str:
        """Create plain text newsletter content."""
        current_date = datetime.now().strftime('%B %d, %Y')
        
        text = f"""
EDGEFINDER WEEKLY REPORT
{current_date}

Hello from EdgeFinder!

This week's analysis of Robinhood prediction markets vs sportsbooks:

SUMMARY:
- Total Games: {report_data.get('total_games', 0)}
- Robinhood Markets: {report_data.get('total_markets', 0)}
- Sportsbooks: {report_data.get('total_books', 0)}

🏆 BEST ROBINHOOD OPPORTUNITIES
Games with the largest differences between Robinhood and sportsbooks:

"""
        
        # Add best opportunities
        if report_data.get('best_opportunities'):
            for i, game in enumerate(report_data['best_opportunities'][:5], 1):
                text += f"""
{i}. {game.get('game', 'N/A')} ({game.get('time', 'N/A')})
   Robinhood: {game.get('robinhoodAway', 'N/A')} / {game.get('robinhoodHome', 'N/A')}
   Sportsbook: {game.get('sportsbookAway', 'N/A')} / {game.get('sportsbookHome', 'N/A')}
   Payout: {game.get('awayPayout', 'N/A')}x / {game.get('homePayout', 'N/A')}x
   Discrepancy: {game.get('discrepancy', 'N/A')}
"""
        
        text += "\n🔥 MOST POPULAR ON ROBINHOOD\nGames with highest volume:\n"
        
        # Add most popular
        if report_data.get('most_popular'):
            for i, game in enumerate(report_data['most_popular'][:5], 1):
                text += f"""
{i}. {game.get('game', 'N/A')} ({game.get('time', 'N/A')})
   Volume: {game.get('volume', 'N/A')}
   Robinhood: {game.get('robinhoodAway', 'N/A')} / {game.get('robinhoodHome', 'N/A')}
   Payout: {game.get('awayPayout', 'N/A')}x / {game.get('homePayout', 'N/A')}x
"""
        
        # Add hometown pick
        if report_data.get('hometown_pick'):
            hometown = report_data['hometown_pick']
            text += f"""
🏠 HOMETOWN FAVORITE: {recipient_location}
Your local team's best opportunity:

{hometown.get('game', 'N/A')} ({hometown.get('time', 'N/A')})
Robinhood: {hometown.get('robinhoodAway', 'N/A')} / {hometown.get('robinhoodHome', 'N/A')}
Sportsbook: {hometown.get('sportsbookAway', 'N/A')} / {hometown.get('sportsbookHome', 'N/A')}
Payout: {hometown.get('awayPayout', 'N/A')}x / {hometown.get('homePayout', 'N/A')}x
Volume: {hometown.get('volume', 'N/A')}
"""
        
        text += f"""
⚠️ DISCLAIMER:
This newsletter is for informational purposes only. Sports betting involves risk 
and may not be legal in all jurisdictions. Please gamble responsibly and within your means.

---
EdgeFinder Newsletter
Delivered to: {recipient_email}
Your location: {recipient_location}
Generated on {current_date}

Visit EdgeFinder: https://edgefinder-czi3.onrender.com/
"""
        
        return text
