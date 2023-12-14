from django.urls import path, include

from apps.authbase.api import routers as authbase_routers
from apps.tracking.api import routers as tracking_routers

urlpatterns = [
     path("authbase/",
          include((authbase_routers, "authbase"), namespace="authbase_api")),
     path("tracking/",
          include((tracking_routers, "tracking"), namespace="tracking_api")),
]
