
import unittest

from udemycalculator.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def test_calculate_square_area(self):
        self.assertEqual(Calculator.calculate_square_area(5), 25)
        
    def test_triangle_square_area(self):
        self.assertEqual(Calculator.calculate_triangle_area(base=10, height=5), 25)
        
    def test_calculate_trapezoid_area(self):
        self.assertEqual(Calculator.calculate_trapezoid_area(base1=10,
                                                             base2=5,
                                                             height=5), 37.5)
        
    def test_squares(self):
        self.assertTrue(Calculator.compare_squares(5, 5))
        self.assertFalse(Calculator.compare_squares(5, 6))
        
if __name__ == '__main__':
    unittest.main()