# Importing the necessary modules 
import smtplib
from email.message import EmailMessage

# Creating a class for sending the email 
class SendEmail:
    def __init__(self, senderEmail, receiverEmail, appPassword): 
        # Getting the sender Email and the receiver email 
        self.senderEmail = senderEmail
        self.receiverEmail = receiverEmail
        self.appPassword = appPassword

    # Creating a function for sending the email 
    def sendMail(self): 
        # Build the email 
        msg = EmailMessage()
        msg["Subject"] = "Password Reset"
        msg["From"] = self.senderEmail 
        msg["To"] = self.receiverEmail

        # HTML Content 
        msg.add_alternative("""
            <!DOCTYPE html>
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: white; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); padding: 20px;">
                    <h2 style="color: #2b6cb0;">Hello from Python! 🐍</h2>
                    <p style="font-size: 16px;">This is an <strong>HTML-formatted email</strong> sent using Gmail's SMTP server.</p>
                    <p>You can include <a href="https://www.python.org" style="color: #3182ce;">links</a>, images, and even inline styles!</p>
                    <hr>
                    <footer style="font-size: 12px; color: #777;">
                        Sent with ❤️ using <b>Python</b> and <b>smtplib</b>.
                    </footer>
                    </div>
                </body>
            </html>
        """, subtype="html")

        # Send the email 
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp: 
            # login the user and send the message 
            smtp.login(self.senderEmail, self.appPassword)
            smtp.send_message(msg) 

        # Dispalyining the success 
        print("HTML email sent successfully")