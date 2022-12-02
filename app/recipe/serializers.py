from rest_framework import serializers

from core import models


class TagSerializer(serializers.ModelSerializer):
    '''serializes the Tag Model'''
    class Meta:
        model = models.Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    '''serializer for Ingredient model'''
    class Meta:
        model = models.Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)
