"""
Newsletter scheduler for sending weekly reports.
"""

import schedule
import time
from datetime import datetime
from src.services.newsletter_generator import NewsletterGenerator
from src.util.log import get_logger


class NewsletterScheduler:
    """Scheduler for weekly newsletter emails."""
    
    def __init__(self):
        self.logger = get_logger()
        self.generator = NewsletterGenerator()
    
    def send_weekly_newsletter(self):
        """Send weekly newsletter to all subscribers."""
        try:
            self.logger.info("Starting weekly newsletter send...")
            
            result = self.generator.send_weekly_newsletters()
            
            if result['status'] == 'success':
                self.logger.info(f"Weekly newsletter sent successfully: {result['message']}")
                self.logger.info(f"Emails sent: {result['emails_sent']}, Failed: {result['emails_failed']}")
            else:
                self.logger.error(f"Weekly newsletter failed: {result['message']}")
                
        except Exception as e:
            self.logger.error(f"Error in weekly newsletter send: {e}")
    
    def start_scheduler(self):
        """Start the newsletter scheduler."""
        # Schedule newsletter for Monday, Thursday, and Saturday at 9:00 AM
        schedule.every().monday.at("09:00").do(self.send_weekly_newsletter)
        schedule.every().thursday.at("09:00").do(self.send_weekly_newsletter)
        schedule.every().saturday.at("09:00").do(self.send_weekly_newsletter)
        
        # Also schedule for testing - every day at 2:00 PM (remove this in production)
        schedule.every().day.at("14:00").do(self.send_weekly_newsletter)
        
        self.logger.info("Newsletter scheduler started")
        self.logger.info("Newsletter scheduled for Monday, Thursday, and Saturday at 9:00 AM")
        self.logger.info("Test newsletter scheduled for daily at 2:00 PM")
        
        # Run scheduler
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


def main():
    """Main function to run the newsletter scheduler."""
    scheduler = NewsletterScheduler()
    scheduler.start_scheduler()


if __name__ == "__main__":
    main()
