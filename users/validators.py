import re
from rest_framework.serializers import ValidationError


def contains_special_character(username):
    # 초성을 허용 할까 말까~.~ 고민이 되는 구만
    username_regex = re.compile(r"[^ A-Za-z0-9가-힣+]")
    if username_regex.findall(username):
        raise ValidationError('이름에 특수문자와 초성을 사용할 수 없습니다!')
    return username


def check_password(password):
    password_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&^])[A-Za-z\d$@$!%*#?&^]{8,}$"
    # (알파벳이 있고)(숫자가 있고)(특수문자가 있으면)8자 이상의 해당 문자열을 입력받는다.
    # 그래서 특수문자에 넣고싶은 문자가 더 있으면 여기에 추가해주면 된다. 양쪽에 다 추가해야함! -> '^'추가함
    if not re.match(password_regex, password):
        raise ValidationError('8자 이상의 영문 대/소문자, 숫자, 특수문자 조합이어야 합니다!')
    return password


def check_email(email):
    email_regex = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        raise ValidationError("이메일에는 '@'와 '.'이 반드시 포함 되어야 합니다!")
    return email