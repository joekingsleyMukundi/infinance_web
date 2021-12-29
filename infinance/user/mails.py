from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse


def otp_email(otp, username, reciver):
    subject = 'Email Verification'
    message = 'Welcome '+username + \
        ' We need to verify that your email.This is you Otp '+str(otp)
    from_email = 'info@goldlinebreeze.com'
    try:
        send_mail(subject, message, from_email, [reciver])
        print('sent')
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
