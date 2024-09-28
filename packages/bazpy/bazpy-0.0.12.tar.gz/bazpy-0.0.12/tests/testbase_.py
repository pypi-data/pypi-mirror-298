from pathlib import Path
from src.bazpy.random import Random
from src.bazpy.testing.testbase import TestBase


class TestBase_(TestBase):
    def test_has_basic_stuff(self):
        self.assertIsInstance(self.few, int)
        self.assertIsInstance(self.some, int)
        self.assertIsInstance(self.many, int)

    assertLen_cases = [
        (False, [], -1),
        (True, [], 0),
        (False, [], 1),
    ]

    def test_assertLen(self):
        for should, input, expect in self.assertLen_cases:
            with self.subTest():
                if should:
                    self.assertLen(input, expect)
                else:
                    self.assertFails(self.assertLen, input, expect)

    assertBetween_cases = [
        (False, 0.3, 1, 2.5),
        (True, 1.3, 1, 2.5),
        (False, 2.51, 1, 2.5),
    ]

    def test_assertBetween(self):
        for should, value, lower, upper in self.assertBetween_cases:
            with self.subTest():
                if should:
                    self.assertBetween(value, lower, upper)
                else:
                    self.assertFails(self.assertBetween, value, lower, upper)

    def test_assertIsFile(self):
        path = "./tests/scratch/baz.txt"
        self.assertIsNotFile(path)
        handle = Path(path)
        handle.touch()
        self.assertIsFile(path)
        handle.unlink()
        self.assertIsNotFile(path)

    def test_assertIsFile(self):
        path = "./tests/scratch/bazdir"
        self.assertIsNotDir(path)
        handle = Path(path)
        handle.mkdir(parents=True, exist_ok=True)
        self.assertIsDir(path)
        handle.rmdir()
        self.assertIsNotDir(path)

    def test_get_stdout(self):
        expected = Random.String.make()
        action = lambda: print(expected, end="", flush=True)
        actual = self.get_stdout(action)
        self.assertEqual(actual, expected)
