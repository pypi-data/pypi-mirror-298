def div(a, b):
    """
    Divide one number by another.

    Parameters:
    a (int or float): The numerator.
    b (int or float): The denominator.

    Returns:
    float: The result of a divided by b.

    Raises:
    ZeroDivisionError: If b is zero.
    """
    return a / b

def mod(a, b):
    """
    Calculate the modulus of one number by another.

    Parameters:
    a (int or float): The dividend.
    b (int or float): The divisor.

    Returns:
    int or float: The remainder of a divided by b.
    """
    return a % b

def exp(a, b):
    """
    Raise one number to the power of another.

    Parameters:
    a (int or float): The base.
    b (int or float): The exponent.

    Returns:
    int or float: The result of a raised to the power of b.
    """
    return a ** b
