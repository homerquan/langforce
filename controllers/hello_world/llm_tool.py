import requests
import base64
import json
import litellm
import os


def call_llm_tool(image, prompt):
    """
    Uses liteLLM to call the model "gpt-4o-mini-2024-07-18" with the provided image and prompt.
    The image (encoded in base64) is sent as an image block in the first user message, and the prompt
    is sent as the second. The output is expected to be a JSON object following a specified schema,
    which includes a "command" field with one of the following values:
    "forward", "backward", "stop", "turn_left", or "turn_right".
    """
    # Convert the image to base64.
    image_base64 = base64.b64encode(image).decode("utf-8")
    # Create a Data URI for the image.
    data_uri = "data:image/png;base64," + image_base64

    # Define the output JSON schema.
    json_schema = {
        "name": "action_demo",
        "schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "enum": ["forward", "backward", "stop", "turn_left", "turn_right"],
                    "description": "The navigation command for the robot.",
                }
            },
            "required": ["command"],
        },
    }

    try:
        response = litellm.completion(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                # System message with high-level instructions.
                {
                    "role": "system",
                    "content": (
                        "User will tell where to go. You first need to scan your surroundings (if the objective is not in the viewport), "
                        "turn around, locate the objective, and then move to it. Avoid obstacles. If you reach the destination, stop."
                    ),
                },
                # The first user message sends the image using an image block.
                {
                    "role": "user",
                    "content": [{"type": "image_url", "image_url": {"url": data_uri}}],
                },
                # The second user message sends the prompt.
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_schema", "json_schema": json_schema},
            temperature=0.7,
            max_tokens=15,
            # Uncomment and set api_base if needed.
            # api_base=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")
        )
        # The response should be a JSON object following the json_schema.
        result = response["choices"][0]["message"]["content"]
        if isinstance(result, str):
            result = json.loads(result)
        command = result.get("command", "stop")
        print("LLM command:", command)
    except Exception as e:
        print("Error calling LLM tool:", e)
        command = "stop"

    print(command)
    return command


def command_to_wheel_speeds(command):
    """
    Maps a textual navigation command to left and right wheel speeds.
    If the command is None or not a string, returns (0.0, 0.0).
    """
    if not isinstance(command, str):
        return (0.0, 0.0)

    cmd = command.lower()

    if cmd == "forward":
        return (5.0, 5.0)
    elif cmd == "backward":
        return (-3.0, -3.0)
    elif cmd in ["turn left", "turn_left"]:
        return (-5.0, 5.0)
    elif cmd in ["turn right", "turn_right"]:
        return (5.0, -5.0)
    elif cmd == "stop":
        return (0.0, 0.0)
    else:
        return (0.0, 0.0)
