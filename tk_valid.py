"""
To use these validate functions, create vcmd to register validation:
    Entry(master, validate="key", vcmd=(self.master.register(validate_###), "%P"))
"""


def validate_alpha(text):
    if not text:
        return True
    elif text.isalpha():
        return True
    else:
        return False


def validate_alphanum(text):
    if not text:
        return True
    elif text.isalnum():
        if ' ' in text:
            return False
        else:
            return True
    else:
        return False


def validate_int(text):
    if not text:
        return True
    try:
        int(text)
        if ' ' in text:
            return False
        else:
            return True
    except ValueError:
        return False


def validate_float(text):
    if not text:
        return True
    try:
        float(text)
        if ' ' in text:
            return False
        else:
            return True
    except ValueError:
        return False
