from django.contrib.auth import get_user_model
from rest_framework import serializers
import re
from accounts.password.new_passwords import NewCreatePassword

from accounts.password.caches import clear_code, verify_code

class SignUpSerializers(serializers.ModelSerializer):
    """
    회원가입 시리얼 라이저
    이메일, 비밀번호, 닉네임 입력
    """
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "nickname"]

    def validate_password(self, value):
        pattern = r'[!@#$%^&*(),.?":{}|<>]'

        if len(value) < 8:
            raise serializers.ValidationError("password가 8자 미만입니다.")
        
        if not re.search(pattern, value):
            raise serializers.ValidationError("특수문자를 포함시켜 주십시오. ex) abcd123@")
        
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

class ResetVerifySerializer(serializers.Serializer):
    """
    비밀번호 리셋 시리얼라이저
    아메일, 인증코드, 새로운 비밀번호 동시 입력
    """
    email = serializers.EmailField()
    code = serializers.CharField()
    new_password = serializers.CharField()

    # 이메일 검사하는 함수
    def validate_email(self, value):
        User = get_user_model()
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("가입된 email이 아닙니다.")
        return value
    
    # 이메일과 코드 캐시에 저장된 코드와 일치한지 확인하는 함수
    def validate(self, attrs):
        email = attrs["email"]
        code = attrs["code"]

        if not verify_code(email, code):
            raise serializers.ValidationError("인증번호가 틀렸거나 만료되었습니다.")
        return attrs
    
    # 새 비밀번호 생성 함수
    # NewCreatePassword.create_new_password 로 넘어가서 진행
    # clear_code(email) === 캐시에 있는 인증코드 삭제
    def create(self, validated_data):
        email = validated_data["email"]
        new_password=validated_data['new_password']
        user = NewCreatePassword.create_new_password(email, new_password)
        clear_code(email)
        return user
