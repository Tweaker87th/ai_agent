import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    # 1. Load configuration from .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("The GEMINI_API_KEY environment variable is not set. Make sure it is defined in your .env file.")

    print("API Key loaded successfully!")

    # 2: Parse command line arguments
    parser = argparse.ArgumentParser(description="Gemini Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
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

    # 5. Interact with the model using messages
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=args.user_prompt,
    )

    # 6: Check usage_metadata and print token counts
    usage_metadata = response.usage_metadata
    if usage_metadata is None:
        raise RuntimeError("No usage_metadata returned. This likely indicates a failed API request. Check your API key, quota, or try again later.")
    
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    print(f"Response tokens: {usage_metadata.candidates_token_count}")

    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()