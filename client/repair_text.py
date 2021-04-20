import re


def change_sign(text, if_scrolled_text=False):
    regex = re.compile("'")
    if if_scrolled_text:
        result_text = text.get('1.0', 'end-1c')
    else:
        result_text = text.get()

    return regex.sub("''", result_text)
