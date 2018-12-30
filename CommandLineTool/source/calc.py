def add(x, y):
    """Add Function
    
    Arguments:
        x: First argument
        y: Second argument
    
    Returns:
        x + y 
    """
    return x + y


def subtract(x, y):
    """Subtract Function
    
    Arguments:
        x: First argument
        y: Second argument
    
    Returns:
        x - y 
    """
    return x - y


def multiply(x, y):
    """Multiply Function
    
    Arguments:
        x: First argument
        y: Second argument
    
    Returns:
        x * y 
    """

    return x * y


def divide(x, y):
    """Divide Function
    
    Arguments:
        x: First argument
        y: Second argument
    
    Raises:
        ValueError: Is raised when y = 0
    
    Returns:
        x / y
    """


    if y == 0:
        raise ValueError('Can not divide by zero!')
    return x / y
