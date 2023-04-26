import string, re


def contains_special_character(value):
    for char in value:
        if char in string.punctuation:
            return True
    return False


def check_password(password):
    password_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&^])[A-Za-z\d$@$!%*#?&^]{8,}$"
    # (알파벳이 있고)(숫자가 있고)(특수문자가 있으면)8자 이상의 해당 문자열을 입력받는다.
    # 그래서 특수문자에 넣고싶은 문자가 더 있으면 여기에 추가해주면 된다. 양쪽에 다 추가해야함! -> '^'추가함
    if len(password) < 8:
        return True
    if not re.match(password_regex, password):
        return True


def check_email(email):
    email_regex = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return True
