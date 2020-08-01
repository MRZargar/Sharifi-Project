from django.core.mail import EmailMultiAlternatives
from main.settings import EMAIL_HOST_USER
from users.models import CustomUser
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email():
	subject = 'Your geolab account has been verified'
	from_email = EMAIL_HOST_USER
	users = CustomUser.objects.all()
	for user in users:
		if user.email_confirmed == True and user.admin_confirmed == True and user.active_email_send == False and user.userType != "is_admin":
			message = render_to_string('account_acitvated.html', {'user': user,})
			text_message = strip_tags(message)
			msg = EmailMultiAlternatives(subject, text_message, from_email, [str(user.email)])
			msg.attach_alternative(message, "text/html")
			msg.send()
			user.active_email_send = True 
			user.save()