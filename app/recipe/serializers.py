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


class RecipeSerializer(serializers.ModelSerializer):
    '''serializes recipe model'''
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Tag.objects.all()
    )

    class Meta:
        model = models.Recipe
        fields = ('id', 'title', 'time_minutes',
                  'price', 'link', 'ingredients', 'tags', 'image')
        read_only_fields = ('id', 'image')


class RecipeDetailSerializer(RecipeSerializer):
    '''serializes recipe details'''
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeUploadSerializer(serializers.ModelSerializer):
    '''serializer for uploading recipe image'''
    class Meta:
        model = models.Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
