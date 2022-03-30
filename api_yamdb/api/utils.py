from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_confirmation_code(user):
    email = user.email
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        "Код подтверждения",
        f"Ваш код подтверждения {confirmation_code}",
        "admin@yandb.com",
        [f"{email}"],
        fail_silently=False,
    )
