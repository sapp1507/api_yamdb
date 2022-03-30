
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, TokenSerializer, UserMeSerializer, UserSerializer
from .permissions import AdminPermission
from django.contrib.auth import get_user_model

from .utils import send_confirmation_code

User = get_user_model()


class RegistrationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        username = data.get('username')
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=username)
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=request.data.get('username'))
        token = str(RefreshToken.for_user(user).access_token)
        data = {'acces': token}
        return Response(data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    lookup_field = 'username'


class UserMeAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserMeSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
