"""Tests for calculator module."""

import pytest
from calculator import add, subtract, multiply, divide, Calculator


class TestBasicOperations:
    """Test basic arithmetic operations."""
    
    def test_add(self):
        """Test addition."""
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0
    
    def test_subtract(self):
        """Test subtraction."""
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5
    
    def test_multiply(self):
        """Test multiplication."""
        assert multiply(3, 4) == 12
        assert multiply(-2, 3) == -6
        assert multiply(0, 100) == 0
    
    def test_divide(self):
        """Test division."""
        assert divide(10, 2) == pytest.approx(5.0)
        assert divide(1, 4) == pytest.approx(0.25)
    
    def test_divide_by_zero(self):
        """Test division by zero raises error."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)


class TestCalculator:
    """Test Calculator class."""
    
    def test_init(self):
        """Test initialization."""
        calc = Calculator()
        assert calc.get_result() == 0
    
    def test_add_operation(self):
        """Test add operation."""
        calc = Calculator()
        calc.add_operation(5)
        assert calc.get_result() == 5
        calc.add_operation(3)
        assert calc.get_result() == 8
    
    def test_clear(self):
        """Test clear operation."""
        calc = Calculator()
        calc.add_operation(10)
        assert calc.get_result() == 10
        calc.clear()
        assert calc.get_result() == 0
