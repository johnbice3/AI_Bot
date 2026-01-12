import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function
import sys

def main():
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key isn't working")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [
        types.Content(
            role="user", 
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    for _ in range(20):

        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(
                tools = [available_functions],
                system_instruction = system_prompt, 
                temperature = 0
                ),
            )
        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.usage_metadata is None:
            raise RuntimeError ("API request failed - usage metadata is none")
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        if not response.function_calls:
            print("Response:")
            print(response.text)
            return

        else:
            function_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)     
                
                if not function_call_result.parts:
                    raise Exception("Function call returned no parts")

                first_part = function_call_result.parts[0]
                func_resp = first_part.function_response

                if func_resp is None:
                    raise Exception("Function response is missing")

                response_dict = func_resp.response
                if response_dict is None:
                    raise Exception("Function response has no data")
                
                function_results.append(first_part)

                if args.verbose:
                    print(f"-> {response_dict}")

            messages.append(
                    types.Content(
                        role="user",
                        parts=function_results,
                    )
                )

    print("Agent did not finish within 20 iterations.")
    sys.exit(1)

if __name__ == "__main__":
    main()
