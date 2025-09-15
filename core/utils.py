from django.core.mail import EmailMessage, EmailMultiAlternatives
from dotenv import load_dotenv
import os

load_dotenv()
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")


class SendEmailUtil:

    @staticmethod
    def send_mail(data):

        if "html_message" in data:
            email_subject = data["email_subject"]
            html_message = data["html_message"]
            text_content = data["email_body"]
            from_email = "saravarjuraev@gmail.com"
            to_email = data["to_email"]

            email = EmailMultiAlternatives(
                email_subject, text_content, from_email, [to_email]
            )
            email.attach_alternative(html_message, "text/html")
            # email.content_subtype = 'html'
            email.send()
        else:
            email = EmailMessage(
                subject=data["email_subject"],
                body=data["email_body"],
                to=[data["to_email"]],
            )
            email.send()
