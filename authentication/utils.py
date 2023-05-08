from django.core.mail import EmailMessage,send_mail
from django.conf import settings

class Util:
    @staticmethod
    def send_email(data):
        # email = EmailMessage(
        #     subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        # email.send()
        subject = data['email_subject']
        message = data['email_body']
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [data['to_email']]
        send_mail( subject, message, email_from, recipient_list )