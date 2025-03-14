#!/usr/bin/env python3
import argparse
import json
import os
from typing import override
from urllib.parse import urlparse

from openai import OpenAI, AssistantEventHandler
from selenium.webdriver.remote.webdriver import WebDriver

from webdriver_factory import get_driver

client = OpenAI()


class OpenAIEventHandler(AssistantEventHandler):
    def __init__(self, driver: WebDriver):
        super().__init__()
        self.driver = driver

    @override
    def on_event(self, event):
        # Retrieve events that are denoted with 'requires_action'
        # since these will have our tool_calls
        if event.event == "thread.run.requires_action":
            run_id = event.data.id  # Retrieve the run ID from the event data
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            args = json.loads(tool.function.arguments)

            if tool.function.name == "retrieve_page_source":
                print("Retrieving page source...")
                tool_outputs.append(
                    {"tool_call_id": tool.id, "output": self.driver.page_source}
                )

            elif tool.function.name == "open_web_page":
                print(f"Opening {args["url"]}...")
                self.driver.get(args["url"])
                tool_outputs.append({"tool_call_id": tool.id, "output": "success"})

            elif tool.function.name == "save_file":
                print(f"Saving local file {args["filename"]}...")
                with open(args["filename"], "w") as f:
                    f.write(args["content"])
                tool_outputs.append({"tool_call_id": tool.id, "output": "success"})

        # Submit all tool_outputs at the same time
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        # Use the submit_tool_outputs_stream helper
        with client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=OpenAIEventHandler(self.driver),
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()


def is_valid_url(url: str) -> bool:
    """Check if the provided string is a valid URL."""
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for processing a web page URL."
    )
    args = parser.parse_args()

    assistant = client.beta.assistants.retrieve(os.environ["OPENAI_ASSISTANT_ID"])
    thread = client.beta.threads.create()

    driver = get_driver()

    print("Ready to accept the command:")

    while True:
        command = input("? ")
        if command.strip().lower() == "exit":
            break

        message = client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=command
        )

        event_handler = OpenAIEventHandler(driver)
        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=event_handler,
        ) as stream:
            stream.until_done()


if __name__ == "__main__":
    main()
