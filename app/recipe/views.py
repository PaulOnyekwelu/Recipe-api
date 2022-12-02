from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from core import models
from recipe import serializers


class TagViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    '''list and create api endpoints for tag model'''
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''return tag objects for current authuser'''
        return self.queryset\
            .filter(user=self.request.user)\
            .order_by('-name')

    def perform_create(self, serializer):
        '''modify data object before create'''
        serializer.save(user=self.request.user)


class IngredientViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    '''list and create api endpoints for ingredient model'''
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''return queryset for auth-user'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        '''modify data object before create'''
        serializer.save(user=self.request.user)
