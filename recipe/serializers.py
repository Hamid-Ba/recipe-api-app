"""
Recipe Module Serializer
"""
from rest_framework import serializers
from core.models import Ingredient, Recipe, Tag

class IngredientSerializer(serializers.ModelSerializer):
    """Ingredient Serializer"""
    class Meta:
        """Meta Class"""
        model = Ingredient
        fields = ['id','name']
        read_only_fields = ('id',)

class TagSerializer(serializers.ModelSerializer):
    """Serializer For Tag Model"""
    class Meta:
        """Meta Class"""
        model = Tag
        fields = ['id','name']
        read_only_fields = ("id",)

class RecipeSerializer(serializers.ModelSerializer):
    """Recipe Serializer"""
    tags = TagSerializer(many=True,required=False)
    ingredients = IngredientSerializer(many=True,required=False)
    
    class Meta:
        """Meta Class"""
        model = Recipe
        fields = ["id","title","time_minute","price","link","tags","ingredients"]
        read_only_fields = ("id",)

    def _get_or_create_tags(self,recipe,tags):
        """Get Or Create Tag"""
        user = self.context['request'].user
        for tag in tags:
            tag_obj , created = Tag.objects.get_or_create(user=user,**tag)
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self,recipe,ingredients):
        """Get Or Create Ingredient"""
        user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj , created = Ingredient.objects.get_or_create(user=user,**ingredient)
            recipe.ingredients.add(ingredient_obj)

    def create(self,validated_data):
        """Customize Creation Recipe"""
        tags = validated_data.pop("tags", [])
        ingredients = validated_data.pop("ingredients", [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(recipe,tags)
        self._get_or_create_ingredients(recipe,ingredients)

        return recipe

    def update(self, instance, validated_data):
        """Customize Update Recipe"""
        tags = validated_data.pop('tags',None)
        ingredients = validated_data.pop("ingredients", None)

        if not tags is None :
            instance.tags.clear()
            self._get_or_create_tags(instance,tags)

        if not ingredients is None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(instance,ingredients)

        super().update(instance, validated_data)
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    """Recipe Detail Serializer"""
    class Meta(RecipeSerializer.Meta):
        """Recipe Detail Meta Class"""
        fields = RecipeSerializer.Meta.fields + ["desc"]