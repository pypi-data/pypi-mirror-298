import sys
from typing import Any, Iterable
from unittest import TestCase
from ..random import Random
from os import path as Path
import uuid
from io import StringIO


class TestBase(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.few = 4
        self.some = 16
        self.many = 32
        self.id1 = "11111111-1111-1111-1111-111111111111"
        self.id2 = "22222222-2222-2222-2222-222222222222"
        self.id3 = "33333333-3333-3333-3333-333333333333"
        self.id4 = "44444444-4444-4444-4444-444444444444"
        self.id5 = "55555555-5555-5555-5555-555555555555"
        # sys.path.append("backend")

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    # ==========================  Helpers  ==========================

    def make_getter(self, x: Any) -> callable:
        return lambda *args, **kwargs: x

    def get_stdout(self, action: callable) -> str:
        recorder = StringIO()
        sys.stdout = recorder  # Redirect stdout
        action()  # Call function
        sys.stdout = sys.__stdout__  # Undo redirect
        return recorder.getvalue()

    # ==========================  Assertions  ==========================

    def assertFails(self, assertion: callable, *args, **kwargs):
        self.assertRaises(AssertionError, lambda: assertion(*args, **kwargs))

    def assertLen(self, things: Iterable, expected: int):
        self.assertEqual(len(things), expected)

    def assertBetween(self, value: float, lower: int, upper: int):
        self.assertGreater(value, lower)
        self.assertLess(value, upper)

    def assertAreInstances(self, things: Iterable, expected_class):
        self.assertIsInstance(things, Iterable)
        for x in things:
            self.assertIsInstance(x, expected_class)

    def assertAll(self, things: Iterable, validation: object):
        for x in things:
            self.assertTrue(validation(x))

    def assertAlmostEqualMany(
        self, values: Iterable, expectations: Iterable, precision: int = 7
    ):
        self.assertIsInstance(values, Iterable)
        self.assertIsInstance(expectations, Iterable)
        self.assertLen(values, len(expectations))
        for i, value in enumerate(values):
            self.assertAlmostEqual(value, expectations[i], precision)

    def assertIsFile(self, filepath: str):
        self.assertTrue(Path.isfile(filepath))

    def assertIsNotFile(self, filepath: str):
        self.assertFalse(Path.isfile(filepath))

    def assertIsDir(self, path: str):
        self.assertTrue(Path.isdir(path))

    def assertIsNotDir(self, path: str):
        self.assertFalse(Path.isdir(path))

    def assertUuid(self, value: str):
        try:
            uuid.UUID(str(value))
            return True
        except ValueError:
            return False
