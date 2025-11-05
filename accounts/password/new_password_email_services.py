from accounts.password.new_password_code_helpers import reset_password
from accounts.password.new_password_send_helpers import send_email
from accounts.password.caches import get_code

class PasswordVerificationService:
    """
    비밀번호 리셋 이메일 보내기
    받는 값은 email
    code 변수에 랜덤으로 생성한 코드 받아온 후
    send_email 함수에 인자 값 전달
    """


    @staticmethod
    def password_email_service(email: str):
        code = reset_password.reset_password_code()
        send_email(email, code, subject="패스워드 찾기 이메일 인증 코드")
        return get_code(email)