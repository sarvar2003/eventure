from django.core.mail import EmailMessage, EmailMultiAlternatives


class Mail:
    @staticmethod
    def send_mail(data):
        subject = data.get('subject')
        body = data.get('body')
        to = [data.get('to')]
        html_message = data.get('html_message')
        
        if html_message:
            # Create a multipart email with both plain text and HTML content
            email = EmailMultiAlternatives(subject=subject, body=body, to=to)
            email.attach_alternative(html_message, "text/html")
        else:
            # Create a plain text email
            email = EmailMessage(subject=subject, body=body, to=to)
        
        email.send()