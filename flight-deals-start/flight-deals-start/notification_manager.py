import smtplib
import time

class NotificationManager:
    """Handles email notifications for flight deals."""

    def __init__(self, email_sender, email_password):
        self.email_sender = email_sender
        self.email_password = email_password

    def send_email(self, to_email, subject, message):
        """Sends an email with flight details, with retries on failure."""
        email_message = f"Subject: {subject}\n\n{message}".encode("utf-8")

        for attempt in range(3):  # Retry up to 3 times
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                    connection.starttls()
                    connection.login(user=self.email_sender, password=self.email_password)
                    connection.sendmail(from_addr=self.email_sender, to_addrs=to_email, msg=email_message)

                print(f"✅ Email sent successfully to {to_email}")
                return

            except Exception as e:
                print(f"⚠️ Email send failed (Attempt {attempt + 1}/3): {e}")
                time.sleep(2)

        print("❌ Email send failed after 3 attempts.")
