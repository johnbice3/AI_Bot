import os
from dotenv import load_dotenv
from google import genai

def main():
    

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key isn't working")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(model="gemini-2.5-flash",contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    
    if response.usage_metadata is None:
        raise RuntimeError ("API request failed - usage metadata is none")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)
    print("Hello from jb3-ai-agent!")


if __name__ == "__main__":
    main()
