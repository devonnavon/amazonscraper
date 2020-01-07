import re

#soupshit
def text(soup):
    if soup is None:
        return soup
    else:
        return soup.text

def parent(soup, level=1):
    if soup is None:
        return soup
    elif level==1:
        return soup.parent
    elif level>1:
        return parent(soup.parent,level-1)
    else:
        pass

def nc(soup):
    '''
    None check
    '''
    try:
        soup_ = soup
    except:
        soup_ = None
    return soup_

#regex
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

def elike(string):
    """
    end like 'string%'
    """
    string_ = string
    if not isinstance(string_, str):
        string_ = str(string_)
    regex = e.escape(string_) + r'.*'
    return re.compile(regex, flags=re.DOTALL)

def blike(string):
    """
    begin like '%string'
    """
    string_ = string
    if not isinstance(string_, str):
        string_ = str(string_)
    regex = r'.*' + e.escape(string_)
    return re.compile(regex, flags=re.DOTALL)
