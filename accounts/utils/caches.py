# 캐시 관련
from django.core.cache import cache
import hashlib

# 캐시 접두어
_SIGNUP_PREFIX = "verify_code:signup:"
_PASSWORD_PREFIX = "verify_code:password_reset:"

# 유효시간
_TTL = 5 * 60

# (이메일 lower + 해시) + 캐시 접두어
def lowered_email(PREFIX: str, email: str) -> str:
    return PREFIX + hashlib.sha256(email.lower().encode()).hexdigest()

# ---------- 구분선 ---------- #

def signup_save_code(email: str, code: str):
    """회원가입 코드 캐시 저장"""
    key = lowered_email(_SIGNUP_PREFIX, email)
    cache.set(key, code, timeout=_TTL)

def signup_get_code(email: str):
    """저장된 코드 불러오기"""
    key = lowered_email(_SIGNUP_PREFIX, email)
    return cache.get(key)

def signup_verify_code(email: str, code: str):
    """입력된 코드가 캐시에 저장된 코드와 일치하는지 검사"""
    saved = signup_get_code(email)
    return saved is not None and str(saved) == str(code)

def signup_clear_code(email: str):
    """검증 완료 후 캐시 삭제"""
    key = lowered_email(_SIGNUP_PREFIX, email)
    cache.delete(key)

# ---------- 구분선 ---------- #

def password_save_code(email: str, code: str):
    """패스워드 리셋 코드 저장"""
    key = lowered_email(_PASSWORD_PREFIX, email)
    cache.set(key, code, timeout=_TTL)

def password_get_code(email: str):
    """패스워드 리셋 관련 저장된 코드 불러오기"""
    key = lowered_email(_PASSWORD_PREFIX, email)
    return cache.get(key)

def password_verify_code(email: str, code: str):
    """입력된 코드가 캐시에 저장된 코드와 일치하는지 검사"""
    saved = password_get_code(email)
    return saved is not None and str(saved) == str(code)

def password_clear_code(email: str):
    """검증 완료 후 캐시 삭제"""
    key = lowered_email(_PASSWORD_PREFIX, email)
    cache.delete(key)