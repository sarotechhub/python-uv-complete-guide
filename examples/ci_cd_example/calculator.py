"""Sample module for CI/CD testing."""


def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


class Calculator:
    """Simple calculator class."""
    
    def __init__(self):
        """Initialize calculator."""
        self.result = 0
    
    def clear(self) -> None:
        """Clear the result."""
        self.result = 0
    
    def add_operation(self, value: int) -> None:
        """Add operation."""
        self.result += value
    
    def get_result(self) -> int:
        """Get current result."""
        return self.result
