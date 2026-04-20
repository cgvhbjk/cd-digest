"""
LLM summarization — provider to be configured.

Swap in your chosen backend by implementing the _call_llm function below.
Currently raises NotImplementedError so the rest of the pipeline still runs
and you can see formatted output with placeholder summaries during setup.
"""

PROMPT_TEMPLATE = """Summarize this Chief Delphi robotics discussion.

Return:
1. A 2-3 sentence summary
2. Key technical takeaways (bullet points)
3. Any competing approaches or disagreements (if present)

Focus only on technical content. Ignore jokes or off-topic replies.

Thread:
{thread_text}"""


def summarize(thread_text: str) -> str:
    prompt = PROMPT_TEMPLATE.format(thread_text=thread_text)
    return _call_llm(prompt)


def _call_llm(prompt: str) -> str:
    # TODO: plug in your LLM here.
    # Example skeleton for Ollama (uncomment when ready):
    #
    # import requests
    # response = requests.post(
    #     "http://localhost:11434/api/generate",
    #     json={"model": "llama3.1:8b", "prompt": prompt, "stream": False},
    #     timeout=120,
    # )
    # return response.json()["response"].strip()

    raise NotImplementedError(
        "LLM backend not configured. See digest/summarizer.py to plug in your model."
    )
