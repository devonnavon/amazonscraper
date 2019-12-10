

def none_check(soup):
    try:
        return soup
    except TypeError:
        return None
