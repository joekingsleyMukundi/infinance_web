from django.contrib.auth.models import User
from django.db.models.signals import post_save
import random
from.models import Dashboard
from.mails import otp_email


def userRegistered(sender, instance, created, **kwargs):
    if created:
        user = instance
        userOtp = random.randint(1000, 9999)
        userDashboard = Dashboard.objects.create(
            user=user,
            balance='0',
            budget=0,
            monthly_capital='0',
            otp=userOtp,
        )
        otp_email(userOtp, user.username, 'joekingsleymukundi@gmail.com')


post_save.connect(userRegistered, sender=User)
