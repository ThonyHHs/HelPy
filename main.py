import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    try:
        user_prompt = sys.argv[1]
        user_args = ""
        if "--verbose" in sys.argv:
            user_args = sys.argv[2]
        if user_prompt.strip() == "":
            raise Exception("Empty string")
    except Exception as e:
        print("ERROR:", e)
        print(f"No prompt has been provided. Please add an prompt to use the program.")
        exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    print(f"Response: {response.text}")
    if user_args == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()