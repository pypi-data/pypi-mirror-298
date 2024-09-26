from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field


class ArithemeticOperation(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"


class ComparisonEnum(str, Enum):
    greater_than = "greater_than"
    less_than = "less_than"
    equal_to = "equal_to"
    not_equal_to = "not_equal_to"


class Comparison(BaseModel):
    num1: Annotated[float | str, Field(description="first number or string")]
    num2: Annotated[float | str, Field(description="second number or string")]


class Arithemetic(BaseModel):
    num1: Annotated[float, Field(description="first number")]
    num2: Annotated[float, Field(description="second number")]
    operation: Annotated[
        ArithemeticOperation, Field(description="operation to be performed")
    ]


def arithemetic(arithmetic: Arithemetic) -> float:
    """
    Performs arithmetic operation on two numbers
    Args:
        arithmetic (Arithemetic): Input object containing two numbers and operation to be performed
    Returns:
        float: Result of the arithmetic operation
    """
    if arithmetic.operation == ArithemeticOperation.add:
        return arithmetic.num1 + arithmetic.num2
    elif arithmetic.operation == ArithemeticOperation.subtract:
        return arithmetic.num1 - arithmetic.num2
    elif arithmetic.operation == ArithemeticOperation.multiply:
        return arithmetic.num1 * arithmetic.num2
    elif arithmetic.operation == ArithemeticOperation.divide:
        return arithmetic.num1 / arithmetic.num2
    else:
        raise ValueError("Invalid operation")


def comparison(com: Comparison) -> str:
    """
    Compares two numbers
    Args:
        com (Comparison): Input object containing two numbers or strings to been compared
    Returns:
        float: Result of the comparison
    """
    if isinstance(com.num1, str) or isinstance(com.num2, str):
        if com.num1 == com.num2:
            return ComparisonEnum.equal_to
        elif com.num1 != com.num2:
            return ComparisonEnum.not_equal_to
    elif com.num1 > com.num2:
        return ComparisonEnum.greater_than
    elif com.num1 < com.num2:
        return ComparisonEnum.less_than
    elif com.num1 == com.num2:
        return ComparisonEnum.equal_to
