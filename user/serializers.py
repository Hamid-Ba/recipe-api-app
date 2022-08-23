"""
User Serilizer
"""
from rest_framework import serializers
from django.contrib.auth import (
    get_user_model,
    authenticate
)

class UserSerializer(serializers.ModelSerializer):
    """ User Serilizer """
    class Meta:
        """User Meta Class"""
        model = get_user_model()
        fields = ["email","password","name"]
        extra_kwargs = {'password' : {"write_only": True , "min_length": 5}}

    def create(self , validated_data):
        return get_user_model().objects.create_user(**validated_data)

class AuthTokenSerializer(serializers.Serializer):
    """User Authorization Token Serializer """
    email = serializers.EmailField()
    password = serializers.CharField(
        style = {"input_type" : "password"},
        trim_whitespace = False ,
        )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = authenticate(
            request=self.context.get('request'),
            username= email,
            password=password
        )

        if not user:
            msg = 'please enter correct information'
            raise serializers.ValidationError(msg,code='authorization')

        attrs['user'] = user
        return attrs