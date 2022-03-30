from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (RegistrationAPIView, TokenAPIView, UserMeAPIView,
                    UserViewSet)

router = SimpleRouter()
router.register("users", UserViewSet)
urlpatterns = [
    path("v1/users/me/", UserMeAPIView.as_view()),
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", RegistrationAPIView.as_view()),
    path("v1/auth/token/", TokenAPIView.as_view()),
]
