from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.core.exceptions import ValidationError

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.user.models import User
from apps.user.api.serializers import UserSerializer
from .serializers import LoginSerializer, RegisterSerializer


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


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )
    queryset = User.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer is unmutable, so copied the data
            data = dict(serializer.data)
            # name is not django user fields: get value and remove key
            name = data.pop('name', None)

            try:
                user = User.objects.create_user(first_name=name, **data)
            except ValidationError as e:
                return Response(
                    {'message': e},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

            user_serializer = UserSerializer(user, context={'request': request})
            return Response(
                user_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': _("Invalid!")},
            status=status.HTTP_403_FORBIDDEN
        )
