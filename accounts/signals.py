from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    reset_url = "{}?token={}".format(
        instance.request.build_absolute_uri(
            reverse('password_reset:reset-password-confirm')
        ),
        reset_password_token.key
    )

    email_message = f"""
Hello,

You requested a password reset.

Use the link below to reset your password:
{reset_url}

If you didn't request this, ignore this email.
"""

    msg = EmailMultiAlternatives(
        subject="Password Reset",
        body=email_message,
        from_email="noreply@test.com",
        to=[reset_password_token.user.email]
    )

    msg.send()