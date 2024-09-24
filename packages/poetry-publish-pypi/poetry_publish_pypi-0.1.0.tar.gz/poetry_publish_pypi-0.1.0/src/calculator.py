def addition(a: int | float, b: int | float) -> int | float:  
    return a + b  
  
def subtraction(a: int | float, b: int | float) -> int | float:  
    return a - b  
  
def multiplication(a: int | float, b: int | float) -> int | float:  
    return a * b  
  
def division(a: int | float, b: int | float) -> int | float:  
    if b == 0:  
        raise ZeroDivisionError("Cannot divide by zero!")  
    return a / b