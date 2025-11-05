from django.core.mail import EmailMessage
from accounts.utils.caches import signup_save_code

def send_email(email: str, code: str, subject: str = "이메일 인증"):
    mail = EmailMessage(subject=subject, body=code, to=[email])
    mail.content_subtype = "html" # html형태로 템플릿을 만들었을 때 필요함
    mail.send()
    signup_save_code(email, code)