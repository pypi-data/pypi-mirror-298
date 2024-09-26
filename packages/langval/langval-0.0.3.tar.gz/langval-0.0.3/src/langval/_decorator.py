from typing import Annotated

from langchain_core.runnables import Runnable


from .eval import BaseEval


def assess(
    question: Annotated[str, "Question to be asked to the model"],
    model: Annotated[Runnable, "Langchain Graph or Model to run the Invoke"] = None,
):
    def decorator(func):
        def wrapper_func(*args, **kwargs):
            expected_answer = func(*args, **kwargs)
            cls = args[0]
            if isinstance(cls, BaseEval):
                raise ValueError("model is required")
            _model = model
            if not _model:
                if cls.model:
                    _model = cls.model
                else:
                    raise ValueError("LLM Model is missing, and its required")
            response = _model.invoke(question)
            if "content" in response:
                response = response["content"]
            result = cls.evaluator.eval(
                question=question, expected_answer=expected_answer, answer=response
            )
            return result

        return wrapper_func

    return decorator
