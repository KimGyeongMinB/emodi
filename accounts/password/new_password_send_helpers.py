from django.core.mail import EmailMessage
from accounts.password.caches import save_code

def send_email(email: str, code: str, subject: str = "비밀번호 리셋 이메일 인증"):
    """
    password_email_service 에서 넘겨받은 값
    비밀번호 리셋 관련 메일 발송 함수
    발송 후 리셋 코드 캐시에 저장
    """
    mail = EmailMessage(subject=subject, body=code, to=[email])
    mail.content_subtype = "html" # html형태로 템플릿을 만들었을 때 필요함
    mail.send()
    save_code(email, code)