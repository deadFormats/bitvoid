from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from order.models import Order


@shared_task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'BitVoid Shop - Invoice no. {order.id}'
    message = "Please, find attached the invoice for your recent purchase."
    email = EmailMessage(
        subject,
        message,
        'admin@bitvoid.com',
        [order.email]
    )

    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylsheets)

    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    email.send()
