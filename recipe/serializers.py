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
    
    class Meta:
        """Meta Class"""
        model = Recipe
        fields = ["id","title","time_minute","price","link","tags"]
        read_only_fields = ("id",)

    def get_or_create_tags(self,recipe,tags):
        """Get Or Create Tag"""
        user = self.context['request'].user
        for tag in tags:
            tag_obj , created = Tag.objects.get_or_create(user=user,**tag)
            recipe.tags.add(tag_obj)

    def create(self,validated_data):
        """Customize Creation Recipe"""
        tags = validated_data.pop("tags", [])
        recipe = Recipe.objects.create(**validated_data)
        self.get_or_create_tags(recipe,tags)

        return recipe

    def update(self, instance, validated_data):
        """Customize Update Recipe"""
        tags = validated_data.pop('tags',None)

        if not tags is None :
            instance.tags.clear()
            self.get_or_create_tags(instance,tags)

        super().update(instance, validated_data)
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    """Recipe Detail Serializer"""
    class Meta(RecipeSerializer.Meta):
        """Recipe Detail Meta Class"""
        fields = RecipeSerializer.Meta.fields + ["desc"]