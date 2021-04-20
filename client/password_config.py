from check_length import check_length
from repair_text import change_sign


def password_config(field1, password, msg):
    field1 = change_sign(field1)
    field1 = check_length(field1, 255)

    password = change_sign(password)
    password = check_length(password, 255)

    message = f'{msg} {field1} {password}'

    return message


def clear_text(field1, password1, password2):
    field1.delete(0, 'end')
    password1.delete(0, 'end')
    password2.delete(0, 'end')
