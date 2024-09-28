import asyncio
from typing import Awaitable, TypeVar
from unittest import IsolatedAsyncioTestCase as AsyncCase
from .testbase import TestBase

T = TypeVar("T")


class TestBaseAsync(TestBase, AsyncCase):

    def make_awaitable(self, value: T) -> Awaitable[T]:
        promise: asyncio.Future[T] = asyncio.Future()
        promise.set_result(value)
        return promise
