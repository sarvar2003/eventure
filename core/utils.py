import io
import qrcode
import base64

from xhtml2pdf import pisa

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives


class SendEmailUtil:

    @staticmethod
    def send_mail(data):

        if "html_message" in data:
            email_subject = data["email_subject"]
            html_message = data["html_message"]
            text_content = data["email_body"]
            from_email = "noreply@eventures.world"
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


def generate_pdf(reservation):
    """Generate a PDF ticket for the reservation."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"Reservation ID: {reservation.id}")
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    context = {
        "reservation": reservation,
        "qr_code": img_str,
    }
    html = render_to_string("ticket_template.html", context)
    pdf_buffer = io.BytesIO()
    pisa.CreatePDF(io.StringIO(html), dest=pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer