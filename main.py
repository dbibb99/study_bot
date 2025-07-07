import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from config import MAX_ITERS



def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Coding Tudor")
        print("\nUsage: python main.py <your prompt here> [--verbose optional]")
        print("\nExample: python main.py 'Create a python file that includes three example recursive functions.'")
        sys.exit(1)

    user_prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.0-flash-001"

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # iters = 0
    # while True:
    #     iters +=1
    #     if iters > MAX_ITERS:
    #         print(f"Maximum iterations ({MAX_ITERS}) reached.")
    #         sys.exit(1)
        
    #     try:
    #         final_response =

    final_response = generate_content(client=client, model_name=model_name, messages=messages, verbose=verbose)
    print(final_response)

def generate_content(client, model_name, messages, verbose):
    response = client.models.generate_content(
        model = model_name,
        contents = messages,
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    return response.text


if __name__ == "__main__":
    main()
