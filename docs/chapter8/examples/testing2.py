def myabs(a):
    """
    绝对值函数
    
    Example:
    
    >>> myabs(1)
    1
    
    >>> myabs(-1)
    1
    
    >>> myabs(0)
    0
    
    >>> myabs('1')
    TypeError Traceback (most recent call last)
        ...
    TypeError: bad operand type for abs(): 'str'
    """
    res = a if a >= 0 else -a
    return res




if __name__ == "__main__":
    import doctest
    doctest.testmod()