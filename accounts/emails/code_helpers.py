import string
import secrets

class EmailHelper:
    def random_email_code(self):
        "문자 + 숫자 랜덤으로 섞이게"
        send_email_code = string.ascii_letters + string.digits
        return "".join(secrets.choice(send_email_code) for _ in range(6))

email_helper = EmailHelper()