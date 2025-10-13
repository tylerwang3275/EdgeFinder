"""
Test script for the newsletter system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.newsletter import NewsletterData
from src.services.newsletter_generator import NewsletterGenerator
from src.services.email_service import EmailService


def test_newsletter_subscription():
    """Test newsletter subscription functionality."""
    print("🧪 Testing Newsletter Subscription System...")
    
    # Test newsletter data storage
    newsletter_data = NewsletterData()
    
    # Add test subscription
    success = newsletter_data.add_subscription("test@example.com", "Seattle, WA")
    print(f"✅ Added subscription: {success}")
    
    # Get active subscriptions
    subscribers = newsletter_data.get_active_subscriptions()
    print(f"✅ Active subscribers: {len(subscribers)}")
    
    for sub in subscribers:
        print(f"   - {sub.email} from {sub.location}")
    
    return True


def test_newsletter_generation():
    """Test newsletter report generation."""
    print("\n🧪 Testing Newsletter Report Generation...")
    
    generator = NewsletterGenerator()
    report_data = generator.generate_weekly_report()
    
    print(f"✅ Generated report with {report_data.get('total_games', 0)} games")
    print(f"✅ Best opportunities: {len(report_data.get('best_opportunities', []))}")
    print(f"✅ Most popular: {len(report_data.get('most_popular', []))}")
    print(f"✅ Hometown pick: {report_data.get('hometown_pick', {}).get('game', 'None')}")
    
    return report_data


def test_email_service():
    """Test email service (without actually sending)."""
    print("\n🧪 Testing Email Service...")
    
    email_service = EmailService()
    
    # Test HTML generation
    test_report = {
        'total_games': 5,
        'total_markets': 5,
        'total_books': 5,
        'best_opportunities': [
            {
                'game': 'Seattle Seahawks @ San Francisco 49ers',
                'time': '10/15 1:00 PM',
                'sport': 'NFL',
                'robinhoodAway': '42.0%',
                'robinhoodHome': '58.0%',
                'sportsbookAway': '+115',
                'sportsbookHome': '-135',
                'awayPayout': '2.4x',
                'homePayout': '1.7x',
                'discrepancy': '5.2%',
                'volume': '2,500'
            }
        ],
        'most_popular': [
            {
                'game': 'Dallas Cowboys @ Philadelphia Eagles',
                'time': '10/15 4:25 PM',
                'sport': 'NFL',
                'robinhoodAway': '48.0%',
                'robinhoodHome': '52.0%',
                'sportsbookAway': '+120',
                'sportsbookHome': '-140',
                'awayPayout': '2.1x',
                'homePayout': '1.9x',
                'discrepancy': '3.8%',
                'volume': '3,200'
            }
        ],
        'hometown_pick': {
            'game': 'Seattle Seahawks @ San Francisco 49ers',
            'time': '10/15 1:00 PM',
            'sport': 'NFL',
            'robinhoodAway': '42.0%',
            'robinhoodHome': '58.0%',
            'sportsbookAway': '+115',
            'sportsbookHome': '-135',
            'awayPayout': '2.4x',
            'homePayout': '1.7x',
            'discrepancy': '5.2%',
            'volume': '2,500'
        }
    }
    
    # Generate HTML content
    html_content = email_service._create_html_newsletter(
        "test@example.com", 
        "Seattle, WA", 
        test_report
    )
    
    print(f"✅ Generated HTML content: {len(html_content)} characters")
    
    # Generate text content
    text_content = email_service._create_text_newsletter(
        "test@example.com", 
        "Seattle, WA", 
        test_report
    )
    
    print(f"✅ Generated text content: {len(text_content)} characters")
    
    return True


def test_complete_newsletter_flow():
    """Test the complete newsletter flow."""
    print("\n🧪 Testing Complete Newsletter Flow...")
    
    # Add test subscription
    newsletter_data = NewsletterData()
    newsletter_data.add_subscription("test@example.com", "Seattle, WA")
    
    # Generate newsletter
    generator = NewsletterGenerator()
    result = generator.send_weekly_newsletters()
    
    print(f"✅ Newsletter send result: {result['status']}")
    print(f"✅ Emails sent: {result.get('emails_sent', 0)}")
    print(f"✅ Total subscribers: {result.get('total_subscribers', 0)}")
    
    return True


def main():
    """Run all newsletter tests."""
    print("🚀 EdgeFinder Newsletter System Test")
    print("=" * 50)
    
    try:
        # Test subscription system
        test_newsletter_subscription()
        
        # Test report generation
        test_newsletter_generation()
        
        # Test email service
        test_email_service()
        
        # Test complete flow
        test_complete_newsletter_flow()
        
        print("\n🎉 All newsletter tests passed!")
        print("\n📧 Newsletter system is ready!")
        print("\nTo set up email sending, configure these environment variables:")
        print("   - SMTP_SERVER (e.g., smtp.gmail.com)")
        print("   - SMTP_PORT (e.g., 587)")
        print("   - SENDER_EMAIL (your email address)")
        print("   - SENDER_PASSWORD (your email password or app password)")
        print("   - SENDER_NAME (e.g., EdgeFinder)")
        
    except Exception as e:
        print(f"\n❌ Newsletter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    main()
