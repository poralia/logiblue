from django.urls import path

from .authorization.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
