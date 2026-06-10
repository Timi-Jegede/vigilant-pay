import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings

class EmailService:
    def __init__(self):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 465
        self.email = settings.GMAIL_EMAIL
        self.password = settings.GMAIL_APP_PASSWORD

    def send_fraud_alert(self, to_email, transaction_data):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = 'Fraud Alert - Possible Fraud'

            html_body = f'''
                        <h2>Fraud Alert</h2>
                        <p>High risk transaction detected:</p>
                        <ul>
                            <li>Amount: ${transaction_data["amount"]}</li>
                            <li>Merchant: {transaction_data["merchant"]}</li>
                            <li>Risk Score: {transaction_data["risk_score"]}</li>
                        </ul>
                        <p>Note User: Vigilant Pay will never ask you for code over the phone.</p>
                        '''
            msg.attach(MIMEText(html_body, 'html'))

            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=30)
            server.set_debuglevel(1)

            server.login(self.email, self.password)

            server.send_message(msg)
            server.quit()

            print('Email sent successfully')
            return True
        except Exception as e:
            print(f'Email error: {e}')
            print(f'Error type: {type(e)}')
            return False
