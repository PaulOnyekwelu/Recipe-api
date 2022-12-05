from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
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


class TagViewSet(BaseRecipeAttr):
    '''list and create api endpoints for tag model'''
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttr):
    '''list and create api endpoints for ingredient model'''
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(ModelViewSet):
    '''list and create api endpoints for recipe model'''
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        '''return serializer class'''
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        '''return queryset for auth user'''
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        '''create a new recipe'''
        serializer.save(user=self.request.user)
