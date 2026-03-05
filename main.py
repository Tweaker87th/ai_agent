import os
from dotenv import load_dotenv
from google import genai

def main():
    # 1. Load configuration from .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("The GEMINI_API_KEY environment variable is not set. Make sure it is defined in your .env file.")

    print("API Key loaded successfully!")

    # 2. Initialize the Gemini client
    client = genai.Client(api_key=api_key)

    # 3. Interact with the model
    # Note: Check model name if you get an error (e.g., gemini-1.5-flash)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )

    print(response.text)

if __name__ == "__main__":
    main()