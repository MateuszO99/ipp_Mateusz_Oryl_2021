def check_length(text, length):
    if len(text) > length:
        text = text[:length]

    return text
