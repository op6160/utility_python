import re

def re_form(startswith = "", endswith = ""):
    return re.compile(r'^'+startswith+r'.*'+endswith)

def compile_anchored_regex(startswith: str = "", endswith: str = "", *, ignore_case: bool = False) -> re.Pattern:
    """
    startswith로 시작하고 endswith로 끝나는 문자열을 매칭하는 정규식을 컴파일
    """
    prefix = re.escape(startswith)
    suffix = re.escape(endswith)
    flags = re.IGNORECASE if ignore_case else 0
    pattern = rf"^{prefix}.*{suffix}$"
    return re.compile(pattern, flags)