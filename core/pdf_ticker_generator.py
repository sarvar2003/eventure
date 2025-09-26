import io
import qrcode
import base64
from django.template.loader import render_to_string
from xhtml2pdf import pisa

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
    if pisa.err:
        return None
    return pdf_buffer