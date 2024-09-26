# Langval

Langval is a language model evaluation tool for evaluating the toxicity, accuracy, hallucination, and bias of language
models.

## Installation

```bash
pip install langval
```

## Usage

```python
from langchain_openai import ChatOpenAI

import langval
from langval import TestCase
from langval.eval import BaseEval
from langval.eval.langchain import LangchainEval
from langval.model import Validation

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
_eval = LangchainEval(
    llm, validation=Validation(toxicity=0.2, accuracy=0.9, hallucination=0.2, bias=0.1)
)


class TestEval(TestCase):
    @property
    def eval(self) -> BaseEval:
        return _eval

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = llm

    @langval.assess(model=llm, question="What is the capital of France?")
    def test_eval(self):
        return "paris"

    @langval.assess("What is the capital of India?")
    def test_001(self):
        return "New delhi"

    @classmethod
    def tearDownClass(cls):
        del cls.model

```

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more information.

## License

langval is licensed under the [MIT License](LICENSE).   
