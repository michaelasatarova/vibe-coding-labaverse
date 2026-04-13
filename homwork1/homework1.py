import os
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv() 

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# 1. Define a tool (function)
def calculate(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


# 2. Describe the tool for the LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression like '2 + 2 * 3'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 3. Send a user query
messages = [
    {"role": "user", "content": "What is (5 + 3) * 2?"}
]

# 4. First call to LLM
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

# 5. Check if LLM wants to call a tool
if message.tool_calls:
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    # 6. Execute the tool
    if function_name == "calculate":
        result = calculate(arguments["expression"])

    # 7. Send result back to LLM
    messages.append(message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })

    # 8. Final LLM response
    final_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )

    print(final_response.choices[0].message.content)

else:
    print(message.content)

