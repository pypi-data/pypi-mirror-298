__all__ = ['testClass']


class TestClass:
    def __init__(self):
        pass

    def test_method1(self, number1, number2):
        return number1 + number2 + 10

    def test_method2(self, number1, number2):
        return number1 * number2 + 10


testClass = TestClass()
