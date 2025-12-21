import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    max_iterations = 20
    current_iteration = 0
    while current_iteration < max_iterations:
        try:
            finished = generate_content(client, messages, args.verbose)
            if finished:
                break
        except Exception as e:
            print(f"Error in iteration {current_iteration}: {e}")
            break
        current_iteration += 1


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    for candidate in response.candidates:
        messages.append(candidate.content)

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return

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

    print("Function call result list:")
    print(function_call_result_list)
    messages.append(types.Content(role="user", parts=function_call_result_list))

    print("Messages after function calls:")
    print(messages)

    if (
        function_call_result_list[-1].function_call == None
        and function_call_result_list[-1].text != None
    ):
        print("Final response:")
        print(function_call_result_list[-1].function_response.response)
        return True


if __name__ == "__main__":
    main()
