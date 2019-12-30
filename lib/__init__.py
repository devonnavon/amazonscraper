import re


def text(soup):
    if soup is None:
        return soup
    else:
        return soup.text

def parent(soup):
    if soup is None:
        return soup
    else:
        return soup.parent

def like(string):
    """
    Return a compiled regular expression that matches the given
    string with any prefix and postfix, e.g. if string = "hello",
    the returned regex matches r".*hello.*"
    """
    string_ = string
    if not isinstance(string_, str):
        string_ = str(string_)
    regex = r'.*' + re.escape(string_) + r'.*'
    return re.compile(regex, flags=re.DOTALL)
