"""Dieses Module enthält einige einfache Funktionen die als Gegenstück 
für UnitTests verwendet werden.
"""

def add(x, y):
    """Add Function
    
    Args:
        x: First argument
        y: Second argument
    
    Returns:
        This function returns the result of x + y 
        
    """
    return x + y


def subtract(x, y):
    """Subtract Function
    
    Args:
        x: First argument
        y: Second argument
    
    Returns:
        This function returns the result of x - y 

    """
    return x - y


def multiply(x, y):
    """Multiply Function
    
    Args:
        x: First argument
        y: Second argument
    
    Returns:
        This function returns the result of x * y 

    """

    return x * y


def divide(x, y):
    """Divide Function
    
    Args:
        x: First argument
        y: Second argument
    
    Raises:
        ValueError: Is raised when y = 0
    
    Returns:
        This function returns the result of x / y

    """


    if y == 0:
        raise ValueError('Can not divide by zero!')
    return x / y
