import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions

def main():
    # 1. Load configuration from .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("The GEMINI_API_KEY environment variable is not set. Make sure it is defined in your .env file.")

    print("API Key loaded successfully!")

    # 2: Parse command line arguments
    # NEW: Added --verbose CLI argument
    parser = argparse.ArgumentParser(description="Gemini Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # 3. Initialize the Gemini client
    client = genai.Client(api_key=api_key)

    # 4. Build messages list (single user message for now)
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    # 5. Generate content
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0
        ),
    )

    # 6: Check usage_metadata and print token counts
        # Print prompt info and token counts (verbose only)
    usage_metadata = response.usage_metadata
    if usage_metadata is None:
        raise RuntimeError("No usage_metadata returned. This likely indicates a failed API request. Check your API key, quota, or try again later.")

    # 7: Handle response: function calls OR text
    function_calls = response.function_calls
    if function_calls:
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
            print(f"Response tokens: {usage_metadata.candidates_token_count}")
        print(response.text)

if __name__ == "__main__":
    main()