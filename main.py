import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("The GEMINI_API_KEY environment variable is not set. Make sure it is defined in your .env file.")

    print("API Key loaded successfully!")

    parser = argparse.ArgumentParser(description="Gemini Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)

    # Initialize conversation with user prompt
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    # Max iterations to prevent infinite loops
    MAX_ITERATIONS = 20

    for iteration in range(MAX_ITERATIONS):
        # Generate model response
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0
            ),
        )

        # Add model candidates to conversation history
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # Handle function calls
        function_calls = response.function_calls
        function_responses = []  # Collect results to feed back to model

        if function_calls:
            for function_call in function_calls:
                function_call_result = call_function(
                    function_call, 
                    verbose=args.verbose,
                    working_directory="./calculator"
                )
                
                # Validate result structure
                if not function_call_result.parts:
                    raise RuntimeError("Function call result has no parts")
                if function_call_result.parts[0].function_response is None:
                    raise RuntimeError("Function call result has no function_response")
                if function_call_result.parts[0].function_response.response is None:
                    raise RuntimeError("Function call result has no response")
                
                # Store response for model
                function_responses.append(function_call_result.parts[0])
                
                # Print result if verbose
                if args.verbose:
                    result_str = function_call_result.parts[0].function_response.response.get('result', 'No result')
                    print(f"-> {result_str}")

            # Feed function results back to model (as "user" messages)
            messages.append(types.Content(role="user", parts=function_responses))

        else:
            # No more function calls = final response
            if args.verbose:
                print("Final response:")
            
            response_text = response.text or "No response text"
            print(response_text)
            break

    else:
        # Max iterations reached without final response
        print(f"Error: Reached maximum {MAX_ITERATIONS} iterations without final response")
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main()