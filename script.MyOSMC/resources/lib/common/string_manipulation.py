

def sanitize_string(string):

    try:
        return str(string)
    except UnicodeEncodeError:
        return string.encode('utf-8', 'ignore')
