A brief description of what your project does and its purpose.
python basic arthimetic operators

def add(a, b):
    """
    Add two numbers.

    Parameters:
    a (int or float): The first number.
    b (int or float): The second number.

    Returns:
    int or float: The sum of a and b.
    """
    return a + b

def sub(a, b):
    """
    Subtract one number from another.

    Parameters:
    a (int or float): The number to be subtracted from.
    b (int or float): The number to subtract.

    Returns:
    int or float: The difference of a and b.
    """
    return a - b

def mul(a, b):
    """
    Multiply two numbers.

    Parameters:
    a (int or float): The first number.
    b (int or float): The second number.

    Returns:
    int or float: The product of a and b.
    """
    return a * b

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

