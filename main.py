import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_ITERATIONS
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    current_iteration = 0
    while True:
        current_iteration += 1
        if current_iteration > MAX_ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached. Exiting.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content in iteration {current_iteration}: {e}")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_call_result_list = []

    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)

        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
            or not function_call_result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function call response for {function_call.name}")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        function_call_result_list.append(function_call_result.parts[0])

    messages.append(types.Content(role="user", parts=function_call_result_list))


if __name__ == "__main__":
    main()
