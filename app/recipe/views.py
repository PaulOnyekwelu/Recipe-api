from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from core import models
from recipe import serializers


class BaseRecipeAttr(ListModelMixin, CreateModelMixin, GenericViewSet):
    '''Base class attributes for recipe viewsets'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''return objects for current logged user'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        '''create new object'''
        serializer.save(user=self.request.user)


class TagViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    '''list and create api endpoints for tag model'''
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    '''list and create api endpoints for ingredient model'''
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
