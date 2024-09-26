from enum import Enum

from pydantic import BaseModel, Field


class ModuleType(str, Enum):
    CLASS = "class"
    FUNCTION = "function"


class Validation(BaseModel):
    toxicity: float = Field(description="toxicity score", ge=0, le=1, default=0.2)
    accuracy: float = Field(description="accuracy score", ge=0, le=1, default=0.9)
    hallucination: float = Field(
        description="hallucination score", ge=0, le=1, default=0.2
    )
    bias: float = Field(description="bias score", ge=0, le=1, default=0.1)

    _CRITERIA = {
        "toxicity": "MAX",
        "accuracy": "MIN",
        "hallucination": "MAX",
        "bias": "MAX",
    }

    def compare(self, other: "Validation") -> (dict, list):
        if not isinstance(other, Validation):
            raise TypeError("Comparison must be between Validation instances")
        comparison = {}
        exact_match = []
        for field, criterion in self._CRITERIA.items():
            self_value = getattr(self, field)
            other_value = getattr(other, field)
            if self_value == other_value:
                exact_match.append(field)
            elif criterion == "MAX":
                if self_value < other_value:
                    comparison[field] = f"Expected {self_value} < but got {other_value}"
                else:
                    continue
            elif criterion == "MIN":
                if self_value > other_value:
                    comparison[field] = f"Expected {self_value} > but got {other_value}"
                else:
                    continue
            else:
                raise ValueError(f"Unknown criterion '{criterion}' for field '{field}'")
        return comparison, exact_match


class EvalMetric(Validation):
    toxicity: float = Field(description="toxicity score", ge=0, le=1)
    accuracy: float = Field(description="accuracy score", ge=0, le=1)
    hallucination: float = Field(description="hallucination score", ge=0, le=1)
    bias: float = Field(description="bias score", ge=0, le=1)
    justification: str = Field(description="justification for the score")


class ModuleModel(BaseModel):
    name: str = Field(description="name of the module")
    type: str = Field(description="type of the module")
    metrics: Validation = Field(description="metrics of the module")
