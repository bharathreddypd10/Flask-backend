from flask_mail import Message
from app.app_main import mail

def send_email(to, subject, template):
    """
    Sends an email using Flask-Mail with HTML content.
    
    Args:
    - to: The recipient's email.
    - subject: The subject of the email.
    - template: HTML template content.
    """
    msg = Message(
        subject,
        recipients=[to],  # List of recipients (can extend it)
        html=template,    # HTML content
    )
    
    try:
        mail.send(msg)
        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Error sending email: {e}")