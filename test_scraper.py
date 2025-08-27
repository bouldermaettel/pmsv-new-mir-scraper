#!/usr/bin/env python3
"""
Test script for the PMSV scraper functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper import PMSVScraper
from email_notifier import EmailNotifier

def test_scraper():
    """Test the web scraper functionality."""
    print("Testing PMSV Scraper...")
    
    scraper = PMSVScraper()
    
    # Test web scraping
    print("1. Testing web scraping...")
    sb_number = scraper.scrape_webpage()
    
    if sb_number:
        print(f"   ✓ Successfully extracted SB number: {sb_number}")
    else:
        print("   ✗ Failed to extract SB number")
        return False
    
    # Test data persistence
    print("2. Testing data persistence...")
    scraper.save_sb_number(sb_number)
    
    loaded_sb = scraper.load_previous_sb_number()
    if loaded_sb == sb_number:
        print(f"   ✓ Data persistence working correctly")
    else:
        print(f"   ✗ Data persistence failed. Expected: {sb_number}, Got: {loaded_sb}")
        return False
    
    # Test change detection
    print("3. Testing change detection...")
    updated, current, previous = scraper.check_for_updates()
    
    if not updated:
        print(f"   ✓ No changes detected (expected for first run)")
    else:
        print(f"   ✓ Change detected: {previous} -> {current}")
    
    print("\nAll tests passed! ✓")
    return True

def test_email_notifier():
    """Test the email notifier functionality."""
    print("\nTesting Email Notifier...")
    
    notifier = EmailNotifier()
    
    if notifier.enabled:
        print("   ✓ Email notifier is properly configured")
    else:
        print("   ⚠ Email notifier is disabled (missing environment variables)")
        print("   This is expected if you haven't set up email credentials yet.")
    
    return True

def main():
    """Run all tests."""
    print("=" * 50)
    print("PMSV Monitor - Test Suite")
    print("=" * 50)
    
    success = True
    
    # Test scraper
    if not test_scraper():
        success = False
    
    # Test email notifier
    if not test_email_notifier():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed!")
        print("\nThe application is ready to use.")
        print("Next steps:")
        print("1. Set up email credentials in .env file")
        print("2. Run 'python main.py' to start monitoring")
        print("3. Or use 'docker-compose up -d' for containerized deployment")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
