from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from user import serializers


class CreateUserView(generics.CreateAPIView):
    '''create a new user'''
    serializer_class = serializers.UserSerializer


class CreateTokenView(ObtainAuthToken):
    '''handles user login token generation'''
    serializer_class = serializers.UserLoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    '''api for authenticated user profile'''
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        return self.request.user
