A brief description of what your project does and its purpose.
Basic arithmatic operator modules

def add(a, b):
    """
    Add two numbers together.

    Parameters:
    a (int or float): The first number to add.
    b (int or float): The second number to add.

    Returns:
    int or float: The sum of a and b.
    """
    return a + b

def sub(a, b):
    """
    Subtract the second number from the first.

    Parameters:
    a (int or float): The number from which to subtract.
    b (int or float): The number to subtract.

    Returns:
    int or float: The difference between a and b.
    """
    return a - b

def mul(a, b):
    """
    Multiply two numbers together.

    Parameters:
    a (int or float): The first number to multiply.
    b (int or float): The second number to multiply.

    Returns:
    int or float: The product of a and b.
    """
    return a * b

def div(a, b):
    """
    Divide the first number by the second.

    Parameters:
    a (int or float): The numerator (the number to be divided).
    b (int or float): The denominator (the number to divide by).

    Returns:
    float: The quotient of a divided by b.

    Raises:
    ZeroDivisionError: If b is zero, division by zero is not allowed.
    """
    return a / b
