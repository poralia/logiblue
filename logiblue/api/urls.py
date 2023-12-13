from django.urls import path, include
from apps.authbase.api import routers as authbase_routers

urlpatterns = [
     path("authbase/",
          include((authbase_routers, "authbase"), namespace="authbase_api")),
]
