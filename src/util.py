import string


# returns true if str contains only alphanumeric + underscore
def is_alphanumeric( str ):
    import re
    exp = re.compile('.*\W.*')
    return exp.match( str ) == None


# returns the first token delimited by a space or a tab
def first_token( str ):
    str = str.lstrip()

    assert len(str) or len(str) == 0  # just check to make sure len(str) exists

    if len(str) == 0:
        return ("", "")
    
    index = 0

    for char in str:

        if char in string.whitespace:
            break

        index +=1

    #print "index ", index
    #print str[:index]

    return (str[:index], str[index:].lstrip())

# remember, it is unsafe to call tokenize on raw user input :)
def tokenize( str ):

    if len(str.lstrip()) == 0:
        return []
    
    tokens = []

    while 1:
        (token, str) = first_token( str )

        assert len(token) > 0, "util.tokenize received a token of length 0 from first_token"

        tokens.append(token)

        if len(str) == 0:
            break

    return tokens


#####################################
# below are from Peter Norvig's util
#####################################

def abstract():
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')


class Struct:
    """Create an instance with argument=value slots.
    This is for making a lightweight object whose class doesn't matter."""
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __cmp__(self, other):
        if isinstance(other, Struct):
            return cmp(self.__dict__, other.__dict__)
        else:
            return cmp(self.__dict__, other)

    def __repr__(self):
        args = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return 'Struct(%s)' % ', '.join(args)

def probability(p):
    import random
    "Return true with probability p."
    return p > random.uniform(0.0, 1.0)