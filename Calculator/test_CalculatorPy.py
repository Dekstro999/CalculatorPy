import unittest

from CalculatorPy02 import Calculator  # Assuming you have a Calculator class in CalculatorPy module

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_addition(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)

    def test_subtraction(self):
        result = self.calc.subtract(5, 3)
        self.assertEqual(result, 2)

    def test_multiplication(self):
        result = self.calc.multiply(2, 3)
        self.assertEqual(result, 6)

    def test_division(self):
        result = self.calc.divide(6, 3)
        self.assertEqual(result, 2)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(1, 0)

if __name__ == '__main__':
    unittest.main()