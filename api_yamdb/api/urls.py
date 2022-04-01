from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    RegistrationAPIView, ReviewViewSet, TitleViewsSet,
                    TokenAPIView, UserViewSet)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'titles', TitleViewsSet, basename='title')
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
    path('v1/auth/signup/', RegistrationAPIView.as_view(), name='signup'),
    path('v1/auth/token/', TokenAPIView.as_view(), name='token'),
]
