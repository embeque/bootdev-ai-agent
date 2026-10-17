import os
import sys
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI

from prompt import system_prompt
from call_function import *
def generate_content(client, messages):
    # print(messages)
    return client.chat.completions.create(
        # model="openrouter/free",
        # model="xingchen-agi/xing4.0-29b-a4b:free",
        model="dots-studio/dots-3-note-preview:free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError('API Key not Found!')

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]


    for _ in range(20):
        response = generate_content(client, messages)
        print(f'got response: {response}')
        message = response.choices[0].message
        messages.append(message)

        if response.usage is  None:
            raise RuntimeError('Failed API Request!')    

        if args.verbose:
            print('User prompt: ', args.user_prompt)
            print('Prompt tokens: ', response.usage.prompt_tokens)
            print('Response tokens: ', response.usage.completion_tokens)
        

        if message.tool_calls:
            for tool_call in message.tool_calls:
                # func_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, True)
                messages.append(result_message)

                if not result_message['content']:
                    raise Exception('Called Function Returned Nothing!')

                if args.verbose:
                    print(f"-> {result_message['content']}")
        
        else:    
            # original response content
            print(message.content)
            return

    print('Final Response not generated, out of tries, try increasing the number of tries per request')
    sys.exit(1)

    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        with open('error.txt', 'w') as f:
            f.write(f'{e}')