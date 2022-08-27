"""
Recipe Serializer
"""

from rest_framework import serializers

from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """Recipe Serializer"""
    class Meta:
        """Meta Class"""
        model = Recipe
        fields = ["id","title","time_minute","price","link"]
        read_only_fields = ("id",)

class RecipeDetailSerializer(RecipeSerializer):
    """Recipe Detail Serializer"""
    class Meta(RecipeSerializer.Meta):
        """Recipe Detail Meta Class"""
        fields = RecipeSerializer.Meta.fields + ["desc"]