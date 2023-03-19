from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core import mail


def generate_mail(user):
    confirmation_code = default_token_generator.make_token(user)
    mail.send_mail(
        "Код для получения токена",
        f"Ваш код для получения токена {confirmation_code}",
        {settings.NOREPLY_YAMDB_EMAIL},
        [user.email],
        fail_silently=False,
    )
