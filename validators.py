import re
from datetime import datetime


def validate_name(name):
    return bool(re.match("^[A-Za-zА-Яа-яЁё\s\-]+$", name))


def validate_birthdate(birthdate_str):
    try:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
        age = (datetime.now() - birthdate).days // 365
        return age <= 100
    except ValueError:
        return False
