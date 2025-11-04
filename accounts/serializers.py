from django.contrib.auth import get_user_model
from rest_framework import serializers
import re

class SignUpSerializers(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "nickname"]

    def validate_password(self, value):
        pattern = r'[!@#$%^&*(),.?":{}|<>]'

        if len(value) < 8:
            raise serializers.ValidationError("password가 8자 미만입니다.")
        
        if not re.search(pattern, value):
            raise serializers.ValidationError("특수문자를 포함시켜 주십시오.")
        
        return value

    def validate_nickname(self, value):
        pattern = r'[!@#$%^&*(),.?":{}|<>]'
        if len(value) < 3:
            raise serializers.ValidationError('닉네임은 3자이상입니다')
        
        if re.search(pattern, value):
            raise serializers.ValidationError('닉네임에는 특수문자가 들어갈수 없습니다.')

        return value
    
    # 유저 생성 함수
    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            nickname=validated_data['nickname'],
            password=validated_data['password'],
            email=validated_data['email']
        )

        return user
    