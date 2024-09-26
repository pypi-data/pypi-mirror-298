import unittest
from abc import abstractmethod

from .eval import BaseEval


class TestCase(unittest.TestCase):
    model = None

    @property
    @abstractmethod
    def evaluator(self) -> BaseEval: ...

    @classmethod
    def setUpClass(cls) -> None:
        cls.result = {}
