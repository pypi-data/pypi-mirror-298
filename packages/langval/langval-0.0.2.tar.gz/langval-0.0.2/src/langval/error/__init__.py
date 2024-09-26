class BaseLangvalError(Exception):
    """
    Base class for all langval errors.
    """

    pass


class EvalThreshold(BaseLangvalError):
    def __init__(
        self,
        breached_value: dict,
        question: str = None,
        answer: str = None,
        expected_answer: str = None,
    ):
        self.breached_value = breached_value
        self.question = question
        self.answer = answer
        self.expected_answer = expected_answer

    def __str__(self):
        return (
            f"\n Error Message: Validation failed for "
            f"\n \t Question :- {self.question},"
            f"\n \t Answer :- {self.answer}"
            f"\n \t Expected Answer :- {self.expected_answer}. "
            f"\n \t Validation score :- {self.breached_value}"
        )

    def __dict__(self):
        return {
            "failed_validation_score": self.breached_value,
            "question": self.question,
            "answer": self.answer,
            "expected_answer": self.expected_answer,
        }
