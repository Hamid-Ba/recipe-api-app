"""
Recipe Module Serializer
"""
from rest_framework import serializers

from core.models import Recipe, Tag

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

    def create(self,validated_data):
        """Customize Creation Recipe"""
        tags = validated_data.pop("tags", [])
        user = self.context['request'].user
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            tag_obj , created = Tag.objects.get_or_create(user=user,**tag)
            recipe.tags.add(tag_obj)

        return recipe

    def update(self, instance, validated_data):
        """Customize Update Recipe"""
        tags = validated_data.pop('tags',None)
        user = self.context['request'].user

        if not tags is None :
            instance.tags.clear()
            for tag in tags:
                tag_obj , created = Tag.objects.get_or_create(user=user,**tag)
                instance.tags.add(tag_obj)

        super().update(instance, validated_data)
        
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    """Recipe Detail Serializer"""
    class Meta(RecipeSerializer.Meta):
        """Recipe Detail Meta Class"""
        fields = RecipeSerializer.Meta.fields + ["desc"]