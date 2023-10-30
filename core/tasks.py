from celery import shared_task
from django.core.mail import send_mail
from core.models import Order
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
@shared_task
def order_email(order_firstname,order_id,order_mail):
	order = Order.objects.get(id=order_id)
	subject = 'Demo market: Order number {}'.format(order_id)
	message = 'Good day, {}! You have successfully ordered from Oloja market.\nYour Order number is {} .'.format(order_firstname,order_id)
	mailer = send_mail(subject, message, 'thkyanhlxag@gmail.com', [order_mail])
	logger.info("Task executed.")
	
@shared_task
def delete_mail(order_id):
    return 1
