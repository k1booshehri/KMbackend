from rest_framework import serializers
from .models import User, Post, Bid
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


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'phone_number',
                  'profile_image', 'university', 'field_of_study', 'entry_year')
        extra_kwargs = {'password': {'write_only': True}}

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


class AddPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        owner = User.objects.get(username=self.initial_data.get('owner'))
        post = Post.objects.create(**validated_data, owner=owner)
        return post

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)
        obj.save()
        return obj


class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'

