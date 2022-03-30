from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (RegistrationAPIView, TokenAPIView, UserMeAPIView,
                    UserViewSet,CommentViewSet, ReviewViewSet, TitleViewsSet,
                    GenreViewSet, CategoryViewSet)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewsSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path("v1/users/me/", UserMeAPIView.as_view()),
    path("v1/auth/signup/", RegistrationAPIView.as_view()),
    path("v1/auth/token/", TokenAPIView.as_view()),
]
