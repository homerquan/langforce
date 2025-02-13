import requests
import base64
import json
import litellm
import os

def call_llm_tool(image, prompt):
    """
    Uses liteLLM to call the Ollama model "llava-llama3" with the provided image and prompt.
    The image (encoded in base64) is sent as the first user message, and the prompt as the second.
    Returns the navigation command without the "using tools:" prefix.
    """
    # Convert the image to base64.
    image_base64 = base64.b64encode(image).decode('utf-8')
    
    try:
        response = litellm.completion(
            model="ollama/llava-llama3",
            messages=[
                {"role": "user", "content": "Image data (base64): " + image_base64},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            api_base=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")
        )
        # Assume the response is in OpenAI chat format.
        command = response["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error calling LLM tool:", e)
        command = "using tools: stop"
    
    # Remove the "using tools:" prefix if present.
    if command.lower().startswith("using tools:"):
        command = command[len("using tools:"):].strip()
    return command

def llm_navigation_tool(image):
    """
    Defines the navigation prompt using the "using tools" convention and calls the LLM tool.
    """
    prompt = (
        "front image, help robot to navigate, output: using tools: forward, "
        "using tools: backward, using tools: stop, using tools: turn left, "
        "using tools: turn right"
    )
    return call_llm_tool(image, prompt)

def command_to_wheel_speeds(command):
    """
    Maps a textual navigation command to left and right wheel speeds.
    """
    cmd = command.lower()
    if cmd == "forward":
         return (2.0, 2.0)
    elif cmd == "backward":
         return (-2.0, -2.0)
    elif cmd == "turn left":
         return (-1.0, 1.0)
    elif cmd == "turn right":
         return (1.0, -1.0)
    elif cmd == "stop":
         return (0.0, 0.0)
    else:
         return (0.0, 0.0)
