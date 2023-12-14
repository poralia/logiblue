from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager

UserModel = get_user_model()


class UserManager(UserManager):
    def generate_username_from_email(self, email):
        username = email.split('@')[0]
        counter = 1
        while UserModel.objects.filter(username=username):
            username = username + str(counter)
            counter += 1

        return username

    def create_user(self, email, username=None, password=None, **kwargs):
        email = self.check_email_unique(email)
        if username is None:
            username = self.generate_username_from_email(email)
        return super().create_user(username, email, password, **kwargs)

    def check_email_unique(self, email):
        if UserModel.objects.filter(email=email).exists():
            raise ValidationError(_("Email already used."))
        return email


class User(UserModel):
    objects = UserManager()

    class Meta:
        proxy = True
        ordering = ('id', )
