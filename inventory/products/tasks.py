from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from inventory import  settings

@shared_task(bind=True)
def test_func(self):
    users = get_user_model().objects.filter(email='XXX')
    for user in users:
        mail_subject = "Hi this is a subject"
        message = "helo this mail is from celery app"
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message= message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True
        )
    print("hello1")
    print(users)
    print("ddd")
    return "Done"
