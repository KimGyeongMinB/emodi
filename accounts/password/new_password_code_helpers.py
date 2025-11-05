import string
import secrets

class ResetPasswordCode:

    def reset_password_code(self):
        "문자 + 숫자 랜덤으로 섞이게"
        reset_password_code = string.ascii_letters + string.digits
        return "".join(secrets.choice(reset_password_code) for _ in range(6))

reset_password = ResetPasswordCode()