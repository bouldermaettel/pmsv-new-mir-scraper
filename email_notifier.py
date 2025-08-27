import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
from typing import Optional

class EmailNotifier:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')
        
        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            logging.warning("Email configuration incomplete. Email notifications will be disabled.")
            self.enabled = False
        else:
            self.enabled = True

    def send_notification(self, previous_sb: str, current_sb: str) -> bool:
        """
        Send email notification about SB number change.
        
        Args:
            previous_sb (str): Previous SB number
            current_sb (str): Current SB number
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.enabled:
            logging.warning("Email notifications are disabled due to incomplete configuration")
            return False
            
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"PMSV SB Number Update Alert - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Email body
            body = f"""
            PMSV SB Number Update Detected!
            
            The SB number on the PMSV reporting forms page has been updated.
            
            Previous SB Number: {previous_sb}
            Current SB Number: {current_sb}
            
            Check the page at: https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance/pmsv-reporting-forms_en
            
            This notification was sent automatically by the PMSV monitoring system.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logging.info(f"Email notification sent successfully to {self.recipient_email}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email notification: {e}")
            return False

    def send_error_notification(self, error_message: str) -> bool:
        """
        Send email notification about system errors.
        
        Args:
            error_message (str): Error message to send
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.enabled:
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"PMSV Monitor Error Alert - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            body = f"""
            PMSV Monitoring System Error
            
            An error occurred while monitoring the PMSV reporting forms page:
            
            {error_message}
            
            Please check the system logs for more details.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logging.info(f"Error notification sent successfully to {self.recipient_email}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send error notification: {e}")
            return False
