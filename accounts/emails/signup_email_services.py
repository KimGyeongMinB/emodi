from accounts.emails.signup_code_helpers import email_helper
from accounts.emails.signup_send_helpers import send_email
from accounts.utils.caches import signup_get_code

class EmailVerificationService:

    @staticmethod
    def email_service(email: str):
        code = email_helper.random_email_code()
        send_email(email, code, subject="회원가입 이메일 인증 코드")
        return signup_get_code(email)