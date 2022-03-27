import unittest
from ex5 import common_prefix


class Test(unittest.TestCase):
    def test0(self):
        assert (common_prefix(["Cyprian", "cyberotoman",
                "cynik", "ceniąc", "czule"]) == "cy")

    def test1(self):
        assert (common_prefix(["Cyprian", "bankomant",
                "cynik", "bank", "bicz", "bańki"]) == "ba")

    def test2(self):
        assert common_prefix(
            ["kaczuszki", "kaczki", "Kacze opowieści", "Kacper"]) == "kacz"


if __name__ == "__main__":
    unittest.main()
