LANGCHAIN_SYSTEM_PROMPT = """
Evaluate the following generated text based on two key criteria, by comparing it against a actual text:

Please provide a score for each of these categories on a scale of 0 to 1. 
Make sure to list all the justification for your score.
{question}

Generated Text -->
{answer}

{expected_answer}
"""
