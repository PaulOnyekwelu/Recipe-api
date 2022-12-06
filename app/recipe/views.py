from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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

    def params_to_ids(self, param):
        '''convert a comma-sep strings of ids to list of int ids'''
        return [int(id) for id in param.split(',')]

    def get_serializer_class(self):
        '''return serializer class'''
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        if self.action == 'upload_image':
            return serializers.RecipeUploadSerializer
        return self.serializer_class

    def get_queryset(self):
        '''return queryset for auth user'''
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset

        if tags:
            tags_ids = self.params_to_ids(tags)
            queryset = queryset.filter(tags__id__in=tags_ids)
        if ingredients:
            ingredients_ids = self.params_to_ids(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredients_ids)

        return queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        '''create a new recipe'''
        serializer.save(user=self.request.user)

    @action(
        methods=['POST'],
        detail=True,
        url_path='upload',
    )
    def upload_image(self, request, pk=None):
        '''handle uploading of recipe image'''
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
