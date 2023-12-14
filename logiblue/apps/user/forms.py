from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms

from .models import User


class UserCreationFormExtend(UserCreationForm):
    email = forms.EmailField(help_text=_("Enter valid email address."))

    def clean_email(self):
        """Reject emails that differ only in case."""
        email = self.cleaned_data.get("email")
        if (
            email
            and self._meta.model.objects.filter(email__iexact=email).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return email

    def save(self, commit=True):
        user = super().save(commit)
        username = self.cleaned_data.get('username', None)
        email = self.cleaned_data.get('email', None)

        if username is None and email is not None:
            username = User.objects.generate_username_from_email(email)
            user.username = username

        return user
