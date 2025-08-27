import schedule
import time
import os
import logging
from dotenv import load_dotenv
from scraper import PMSVScraper
from email_notifier import EmailNotifier

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pmsv_monitor.log'),
        logging.StreamHandler()
    ]
)

class PMSVMonitor:
    def __init__(self):
        self.scraper = PMSVScraper()
        self.email_notifier = EmailNotifier()
        self.check_interval_hours = int(os.getenv('CHECK_INTERVAL_HOURS', '24'))

    def run_check(self):
        """Run a single check for SB number updates."""
        try:
            logging.info("Starting PMSV SB number check...")
            
            updated, current, previous = self.scraper.check_for_updates()
            
            if updated and previous is not None:
                logging.info(f"SB number updated! Previous: {previous}, Current: {current}")
                
                # Send email notification
                if self.email_notifier.send_notification(previous, current):
                    logging.info("Email notification sent successfully")
                else:
                    logging.warning("Failed to send email notification")
            elif current is not None:
                logging.info(f"SB number unchanged: {current}")
            else:
                logging.error("Could not retrieve current SB number")
                self.email_notifier.send_error_notification("Failed to retrieve current SB number from webpage")
                
        except Exception as e:
            error_msg = f"Error during PMSV check: {str(e)}"
            logging.error(error_msg)
            self.email_notifier.send_error_notification(error_msg)

    def start_monitoring(self):
        """Start the scheduled monitoring."""
        logging.info(f"Starting PMSV monitoring service. Check interval: {self.check_interval_hours} hours")
        
        # Schedule the check to run every specified hours
        schedule.every(self.check_interval_hours).hours.do(self.run_check)
        
        # Run initial check
        self.run_check()
        
        # Keep the service running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute for scheduled tasks

def main():
    """Main entry point for the application."""
    try:
        monitor = PMSVMonitor()
        monitor.start_monitoring()
    except KeyboardInterrupt:
        logging.info("PMSV monitoring service stopped by user")
    except Exception as e:
        logging.error(f"Fatal error in PMSV monitoring service: {e}")
        raise

if __name__ == "__main__":
    main()
