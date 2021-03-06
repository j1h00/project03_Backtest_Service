from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name', 'profile_img', 'profile_img_url', 'is_admin', 'is_google')

# 패스워드가 필요없는 다른 테이블에서 사용할 용도
class UserInfoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'profile_img', 'profile_img_url', 'is_admin', 'is_google')