from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import LoginSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # use email as username
            username = serializer.data.pop('email', None)
            user = authenticate(request, username=username, **serializer.data)
            if user is not None:
                # make user loggedin
                login(request=request, user=user)
            else:
                return Response(
                    {'message': _("Email or password incorrect.")},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response({'message': _("Login success!")})
