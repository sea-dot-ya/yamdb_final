import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers


def email_is_valid(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def username_validation(self, value):
    regex = re.compile(r"^[\w.@+-]+$")
    if not re.fullmatch(regex, value) or self.initial_data["username"] == "me":
        raise serializers.ValidationError("Проверьте username!!")
    return value
