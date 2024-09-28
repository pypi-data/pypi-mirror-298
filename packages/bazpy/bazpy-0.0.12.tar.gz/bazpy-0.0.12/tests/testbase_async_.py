from src.bazpy.testing.testbase_async import TestBaseAsync


class Test_TestBaseAsync(TestBaseAsync):
    def test_inherits_basic_stuff(self):
        self.assertIsInstance(self.few, int)
        self.assertIsInstance(self.some, int)
        self.assertIsInstance(self.many, int)

    make_awaitable_cases = [1, False, "dasoo", 3.2]

    async def test_make_awaitable_result(self):
        for expected in self.make_awaitable_cases:
            with self.subTest():
                sut = self.make_awaitable(expected)
                actual = await sut
                self.assertEqual(actual, expected)
