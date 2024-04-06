# utils.py

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

def send_new_article_notification(article):
    subject = 'New Article Published!'
    message = (
        f"New Article Published!\n\n"
        f"Title: {article.title}\n"
        f"Department: {article.department}\n"
        f"Author: {article.author.username}\n"
        f"Log in to check it out!\n"
    )
    recipient_list = [user.email for user in User.objects.all()]  # Include all registered users
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
