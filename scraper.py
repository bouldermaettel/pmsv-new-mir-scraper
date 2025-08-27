import requests
from bs4 import BeautifulSoup
import re
import json
import os
from datetime import datetime
import logging
from typing import Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class PMSVScraper:
    def __init__(self, data_file: str = 'sb_number_data.json'):
        self.url = "https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance/pmsv-reporting-forms_en"
        self.data_file = data_file
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def scrape_webpage(self) -> Optional[str]:
        """
        Scrape the webpage and extract the SB number from the MIR form line.
        
        Returns:
            Optional[str]: The extracted SB number or None if not found
        """
        try:
            logging.info(f"Scraping webpage: {self.url}")
            response = self.session.get(self.url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the specific line containing "New manufacturer incident report (MIR 7.3.1. PDF form - SB 10573)"
            # We'll search for text containing "MIR 7.3.1" and "SB"
            mir_pattern = re.compile(r'MIR 7\.3\.1.*?SB (\d+)', re.IGNORECASE)
            
            # Search in all text content
            page_text = soup.get_text()
            match = mir_pattern.search(page_text)
            
            if match:
                sb_number = match.group(1)
                logging.info(f"Found SB number: {sb_number}")
                return sb_number
            else:
                logging.warning("SB number not found in the webpage")
                return None
                
        except requests.RequestException as e:
            logging.error(f"Error scraping webpage: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during scraping: {e}")
            return None

    def load_previous_sb_number(self) -> Optional[str]:
        """
        Load the previously saved SB number from the data file.
        
        Returns:
            Optional[str]: The previously saved SB number or None if not found
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    return data.get('sb_number')
            return None
        except Exception as e:
            logging.error(f"Error loading previous SB number: {e}")
            return None

    def save_sb_number(self, sb_number: str) -> None:
        """
        Save the current SB number to the data file.
        
        Args:
            sb_number (str): The SB number to save
        """
        try:
            data = {
                'sb_number': sb_number,
                'last_updated': datetime.now().isoformat(),
                'timestamp': datetime.now().timestamp()
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logging.info(f"Saved SB number: {sb_number}")
        except Exception as e:
            logging.error(f"Error saving SB number: {e}")

    def check_for_updates(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check if the SB number has been updated.
        
        Returns:
            Tuple[bool, Optional[str], Optional[str]]: 
                - True if updated, False otherwise
                - Current SB number
                - Previous SB number
        """
        current_sb = self.scrape_webpage()
        previous_sb = self.load_previous_sb_number()
        
        if current_sb is None:
            logging.error("Could not retrieve current SB number")
            return False, None, previous_sb
        
        if previous_sb is None:
            logging.info(f"First run - saving initial SB number: {current_sb}")
            self.save_sb_number(current_sb)
            return False, current_sb, None
        
        if current_sb != previous_sb:
            logging.info(f"SB number updated! Previous: {previous_sb}, Current: {current_sb}")
            self.save_sb_number(current_sb)
            return True, current_sb, previous_sb
        else:
            logging.info(f"SB number unchanged: {current_sb}")
            return False, current_sb, previous_sb

def main():
    """Main function for testing the scraper."""
    scraper = PMSVScraper()
    updated, current, previous = scraper.check_for_updates()
    
    if updated:
        print(f"UPDATE DETECTED! Previous: {previous}, Current: {current}")
    else:
        print(f"No update. Current SB number: {current}")

if __name__ == "__main__":
    main()
