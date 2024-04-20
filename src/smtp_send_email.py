import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SMTPSendEmail:
    """
    A class to send emails using SMTP.
    """

    def __init__(self):
        """
        Initializes SMTPSendEmail with sender and receiver email addresses.

        Args:
            sender_email (str): Sender's email address.
            sender_app_password (str): Sender's application-specific password.
            receiver_email (str): Receiver's email address.
        """
        self.sender_email = os.environ.get("SENDER_EMAIL")
        self.sender_app_password = os.environ.get("SENDER_APP_PASSWORD") # NOTE:make your own app password from sender google account
        self.receiver_email = os.environ.get("RECEIVER_EMAIL")

    def smtp_config(self):
        """
        Configures the SMTP server with provided sender credentials.
        """
        self.smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.smtp_server.login(self.sender_email, self.sender_app_password)

    def send_email(self):
        """
        Sends an email with provided content.
        """
        self.smtp_config()
        
        subject = "New York Times News Data Report"
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = subject

        message = f'''Dear Recipient,

        I hope this email finds you well.

        Please find attached google sheet the latest report containing data from the New York Times News. 
        https://docs.google.com/spreadsheets/d/12Bb_UE2nzr3dT4MlnjahcpDC9v8hXud1VxlcRg_mZIA/edit?pli=1#gid=0

        Best regards,
        {self.sender_email}
        '''
        msg.attach(MIMEText(message, 'plain'))
        
        self.smtp_server.send_message(msg)
        self.smtp_server.quit()

# Example usage:
if __name__ == "__main__":
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_app_password = os.environ.get("SENDER_APP_PASSWORD")
    receiver_email = os.environ.get("RECEIVER_EMAIL")

    if sender_email and sender_app_password and receiver_email:
        email_sender = SMTPSendEmail(sender_email, sender_app_password, receiver_email)
        email_sender.send_email()
    else:
        print("Sender email, sender app password, or receiver email not found in environment variables.")



