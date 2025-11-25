import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if len(sys.argv) < 2:
        print("Please provide a message as a command line argument.")
        return exit(1)

    verbose = False
    for argument in sys.argv:
        if argument == "--verbose":
            verbose = True

    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])])
    ]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    print(f"Response: {response.text}")

    if verbose:
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
