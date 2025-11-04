# 캐시 관련
from django.core.cache import cache

# 캐시 접두어
_KEY_PREFIX = "verify_code:"

# 유효시간
_TTL = 5 * 60

def save_code(email: str, code: str):
    """회원가입 코드 캐시 저장"""
    key = _KEY_PREFIX + email
    cache.set(key, code, timeout=_TTL)

def get_code(email: str):
    """저장된 코드 불러오기"""
    key = _KEY_PREFIX + email
    return cache.get(key)

def verify_code(email: str, code: str):
    """입력된 코드가 캐시에 저장된 코드와 일치하는지 검사"""
    saved = get_code(email)
    return saved is not None and saved == code

def clear_code(email: str):
    """검증 완료 후 캐시 삭제"""
    key = _KEY_PREFIX + email
    cache.delete(key)