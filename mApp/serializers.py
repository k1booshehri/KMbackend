from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number',
                  'profile_image', 'university', 'field_of_study', 'entry_year')


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number',
                  'profile_image', 'university', 'field_of_study', 'entry_year')

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)
        obj.save()
        return obj


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username','password' ,'email', 'first_name', 'last_name', 'phone_number',
                  'profile_image', 'university', 'field_of_study', 'entry_year')
        extra_kwargs = {'paswword': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")