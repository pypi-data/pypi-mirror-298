
def Strip(text):
    """
    Removes everything after a semicolon and strips leading/trailing whitespace.
    """
    text = text.split(';')[0].strip()
    return text
