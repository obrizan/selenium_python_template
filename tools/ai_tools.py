import inspect
from dataclasses import dataclass
from typing import Tuple

from pydantic import BaseModel
from openai import OpenAI


client = OpenAI()


class Locator(BaseModel):
    strategy: str
    value: str


@dataclass
class StackInfo:
    filename: str
    line_number: int
    function_name: str
    code_line: str | None


SYSTEM_PROMPT = """
You are an experienced web developer.
You are helping to fix automatic tests written in Python and Selenium. 
Your will be given a LOCATOR, consisting of LOCATOR_STRATEGY and a VALUE.
LOCATOR_STRATEGY is one of: "id", "xpath", "link text", "partial link text", "name", "tag name", "class name", "css selector".
Also you will be given with a PAGE_SOURCE.
Your task to analyze given LOCATOR and provide actually existing one. 
"""


def lookup_better_selector(by: str, value: str, page_source: str) -> Tuple[str, str]:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"<LOCATOR><LOCATOR_STRATEGY>{by}<LOCATOR_STRATEGY><VALUE>{value}</VALUE><PAGE_SOURCE>{page_source}</PAGE_SOURCE>",
            },
        ],
        response_format=Locator,
        store=False,
        temperature=0.0,  # Lower temperature for deterministic output
        top_p=1.0,  # Use nucleus sampling
    )

    return completion.choices[0].message.parsed.strategy, completion.choices[
        0
    ].message.parsed.value


def find_nearest_find_element_call() -> StackInfo | None:
    """
    Traverses the call stack to find the nearest `find_element` call and extracts its details.

    Returns:
        dict: A dictionary containing filename, line number, function name, and the code line.
    """
    stack = inspect.stack()

    for frame_info in stack:
        code_context = frame_info.code_context
        if code_context and any(".find_element(" in line for line in code_context):
            return StackInfo(
                filename=frame_info.filename,
                line_number=frame_info.lineno,
                function_name=frame_info.function,
                code_line=code_context[0].strip() if code_context else "Unknown",
            )

    return None
