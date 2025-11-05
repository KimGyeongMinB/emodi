from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class NewCreatePassword:

    @staticmethod
    def create_new_password(email: str, new_password: str) -> bool:
        """
        유저 이메일 조회해서 있으면 모델 메서드 new_set_password 로 넘어감
        """
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("해당 이메일의 사용자가 존재하지 않습니다.")
        return user.new_set_password(new_password)