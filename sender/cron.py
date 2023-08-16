import datetime

from django.conf import settings
from django.core.mail import send_mail

from sender.models import Sender, SenderLog


def send_email(sender_client, sender_mailing):
    message = send_mail(
        subject=sender_mailing.subject,
        message=sender_mailing.message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[sender_client.email],
        fail_silently=False
    )

    SenderLog.objects.create(
        client=sender_client,
        sender=sender_mailing,
        status=SenderLog.Status.SUCCESS if message else SenderLog.Status.FAILED
    )


def my_scheduled_job():
    now = datetime.datetime.now()
    for mailing in Sender.objects.filter(status=Sender.Status.STARTED):
        for client in mailing.client.all():
            client_log = SenderLog.objects.filter(client=client.pk, sender=mailing.pk)
            if client_log.exists():
                date_try = client_log.order_by('-last_try').first()
                if mailing.period == mailing.Period.DAILY:
                    if (now.day - date_try.last_try.day) == 1 and (now.time().hour == mailing.time.hour):
                        send_email(date_try.client, date_try.sender)
                elif mailing.period == mailing.Period.WEEKLY:
                    if (now.day - date_try.last_try.day) == 7 and (now.time().hour == mailing.time.hour):
                        send_email(date_try.client, date_try.sender)
                elif mailing.period == mailing.Period.MONTHLY:
                    if (now.day - date_try.last_try.day) == 28 and (now.time().hour == mailing.time.hour):
                        send_email(date_try.client, date_try.sender)
            else:
                if now.time().hour >= mailing.time.hour:
                    send_email(client, mailing)
