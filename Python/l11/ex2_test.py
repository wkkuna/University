import unittest
from ex2 import is_palindrom


class Test(unittest.TestCase):
    def test0(self):
        assert is_palindrom("")

    def test1(self):
        assert is_palindrom("Ala")

    def test2(self):
        assert is_palindrom("Kajak")

    def test3(self):
        assert not is_palindrom(
            "Małe kaczuszki są super! Niestety nie są palindromem")


if __name__ == "__main__":
    unittest.main()
