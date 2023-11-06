import json
import logging

import openai
from tenacity import (before_sleep_log, retry, stop_after_attempt,
                      wait_random_exponential)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Chat:
    def __init__(
        self,
        agent: dict,
        model: str = "gpt-3.5-turbo-0613",
        verbose: bool = True,  # TODO: implement verbose
    ) -> None:
        self.messages = agent["messages"]
        self.functions = agent["functions"]
        self.model = model

    @retry(
        before_sleep=before_sleep_log(logger, logging.INFO),
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(6),
    )
    def predict(self, input: str):
        # Append the user prompt to the messages
        self.messages.append({"role": "user", "content": input})

        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=0.0,
            messages=self.messages,
            functions=[function_meta[0] for function_meta in self.functions],
        )
        message = response["choices"][0]["message"]  # type: ignore
        self.messages.append(message)
        
        # call functions if any
        if "function_call" in message:
            function_name = message["function_call"]["name"]
            kwargs = json.loads(message["function_call"]["arguments"])

            # Log the function name and arguments
            logger.info("=== Calling function ===")
            logger.info(f"{function_name} with args: {kwargs}")

            # Call the function
            for function in self.functions:
                if function_name == function[0]["name"] and function[1] is not None:
                    output = function[1](**kwargs)
                    logger.info(f"Got output: {output}\n")
                    break
            # return function output
            return output, kwargs
        else:
            return self.messages[-1]
