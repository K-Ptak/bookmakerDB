import re


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def validate_phone_number(phone_number):
    pattern = r'^\d{9}$'
    return re.match(pattern, phone_number) is not None


def validate_password(password):
    pattern = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$'
    return re.match(pattern, password) is not None
