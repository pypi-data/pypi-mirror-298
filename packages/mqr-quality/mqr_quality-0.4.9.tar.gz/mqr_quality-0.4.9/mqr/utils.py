import numpy as np

def make_ordinal(n):
    '''
    Convert an integer into its ordinal representation

    Thanks to: https://stackoverflow.com/a/50992575

    Arguments
    ---------
    n -- the number to express in ordinal representation
    '''
    if not np.isclose(n, int(n)):
        number = str(n)
        suffix = 'th'
    elif (11 <= (n % 100) <= 13) or ():
        number = str(int(n))
        suffix = 'th'
    else:
        number = str(int(n))
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(int(n) % 10, 4)]
    return number + suffix

def clip_where(a, a_min, a_max, where):
    '''
    Clamp `a` so that `a_min <= a <= a_max` is true or all true, masked by `where`.

    Arguments
    ---------
    a (number or array) -- value or values to clip.
    a_min (number) -- minimum value.
    a_max (number) -- maximum value.
    where (bool or array[bool]) -- clip when this value or corresponding element
        evaluates to `True`.
    '''
    aa = np.atleast_1d(a).copy()
    aa[where] = np.clip(np.atleast_1d(a)[where], a_min, a_max)
    try:
        iter(a)
    except TypeError:
        return aa[0]
    else:
        return aa
