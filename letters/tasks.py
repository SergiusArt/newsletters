import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from letters.models import Newsletter, MailLog

# Получаем данные для smtp-сервера из переменных окружения
SMTP_HOST = os.environ.get('smtp_ya_host')
SMTP_MAIL = os.environ.get('smtp_ya_mail')
SMTP_PASSWORD = os.environ.get('smtp_ya_password')
SMTP_PORT = int(os.environ.get('smtp_ya_port'))


@shared_task
def send_newsletter():
    # Получаем все объекты рассылок
    newsletters = Newsletter.objects.all()

    for newsletter in newsletters:
        # Проверяем, что статус рассылки "создана" и время рассылки меньше текущего времени
        if newsletter.status == 'created' and newsletter.send_time < timezone.now():
            # Получаем последний лог для текущей рассылки
            last_log = MailLog.objects.filter(newsletter=newsletter).order_by('-last_sent').first()

            if last_log is None or (last_log.last_sent is not None and last_log.last_sent + get_timedelta(
                    newsletter.frequency) <= timezone.now()):

                # Меняем статус на "запущена"
                newsletter.status = 'started'
                # newsletter.save()

                # Получаем список email-адресов подписчиков рассылки
                recipients = [subscriber.email for subscriber in newsletter.emails.all()]

                # Отправляем рассылку с помощью функции send_mail Django
                server_response = send_email(newsletter.message.subject, newsletter.message.body, recipients)

                # Меняем статус на "завершена"
                newsletter.status = 'completed'
                newsletter.save()

                # Записываем информацию о рассылке в лог
                log = MailLog(
                    newsletter=newsletter,
                    status=newsletter.status,
                    last_sent=timezone.now(),
                    server_response=server_response)
                log.save()

                # Меняем статус на "создана"
                newsletter.status = 'created'
                newsletter.save()


def send_email(subject, text, to_addr):
    for i in range(len(to_addr)):
        msg = MIMEMultipart()
        msg['From'] = SMTP_MAIL
        msg['To'] = ", ".join(to_addr[i])
        msg['Subject'] = subject
        msg.attach(MIMEText(text, 'plain'))

        # Устанавливаем соединение с SMTP-сервером и отправляем сообщение
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            # server.starttls()
            server.login(SMTP_MAIL, SMTP_PASSWORD)
            response = server.sendmail(SMTP_MAIL, to_addr, msg.as_string())

    return response


def get_timedelta(frequency):
    if frequency == 'daily':
        return timedelta(days=1)
    elif frequency == 'weekly':
        return timedelta(weeks=1)
    elif frequency == 'monthly':
        return timedelta(days=30)
    else:
        return timedelta(days=1)  # По умолчанию, если значение частоты неизвестно
