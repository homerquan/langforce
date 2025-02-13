import os
from flask import Flask, request, jsonify
import litellm  # Use litellm to access Ollama

app = Flask(__name__, static_folder="www", static_url_path="")

def extract_plain_code(code):
    """
    Extracts the content between the first and last code fence (```).
    If both a starting and an ending fence are found, it removes everything
    before the end of the first fence line and everything after the beginning
    of the last fence. If no fences are found, returns the original code.
    """
    first_fence = code.find("```")
    last_fence = code.rfind("```")
    
    # If both fences exist and they are not the same fence:
    if first_fence != -1 and last_fence != -1 and first_fence != last_fence:
        # Remove everything before (and including) the first fence line.
        first_newline = code.find("\n", first_fence)
        if first_newline != -1:
            code = code[first_newline+1:]
        else:
            code = code[first_fence+3:]
        
        # Remove everything from the start of the last fence.
        code = code[:code.rfind("```")]
    
    # If only one fence is present and it's at the beginning, remove that line.
    elif first_fence == 0:
        first_newline = code.find("\n", first_fence)
        if first_newline != -1:
            code = code[first_newline+1:]
        else:
            code = ""
    
    # If no fences are found, or conditions don't match, leave the code unchanged.
    return code.strip()


@app.route('/')
def index():
    return app.send_static_file('index.html')

def generate_behavior_code(user_instruction: str) -> str:
    """
    Uses litellm (targeting Ollama) to generate a Python code snippet that
    implements a robot behavior based on the provided natural language instruction.
    The generated code defines a function `get_control_values(current_time)` that returns:
    left_speed, right_speed, and wave_position.
    """
    system_prompt = (
        "You are an expert robotic behavior programmer. Given a natural language instruction "
        "that describes the behavior the robot should perform, generate a Python code snippet "
        "that implements this behavior. The code snippet must define a function called `get_control_values(current_time)` "
        "which returns three values: left_speed, right_speed, and wave_position. "
        "The code should compute driving speeds and calculate an arm waving motion using math.sin. "
        "For example, if the instruction is 'moving forward', you might generate:\n\n"
        "```python\n"
        "import math\n\n"
        "def get_control_values(current_time):\n"
        "    left_speed = 3.0\n"
        "    right_speed = 3.0\n"
        "    amplitude = 0.2\n"
        "    offset = -0.75\n"
        "    frequency = 0.5\n"
        "    wave_position = offset + amplitude * math.sin(2 * math.pi * frequency * current_time)\n"
        "    return left_speed, right_speed, wave_position\n"
        "```\n\n"
        "Only the function body is needed; you don't need to include the import statement or the function signature.\n"
        "Now, generate the code based on the following instruction:\n"
        f"\"{user_instruction}\"\n"
    )

    # Call the litellm completion function targeting an Ollama model.
    response = litellm.completion(
        model="ollama/llava-llama3",  # adjust the model name as needed (or use an Ollama Chat model like "ollama_chat/llama3.1")
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_instruction},
        ],
        temperature=0.7,
        api_base=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")
    )

    # Extract the generated code from the response.
    code = response.choices[0].message.content

    # Remove markdown code fence markers if present.
    return extract_plain_code(code)

@app.route('/api/sendCommand', methods=['POST'])
def send_command():
    """
    Expects a JSON payload with an 'instruction' field (e.g., { "instruction": "moving forward" }).
    It generates the corresponding Python code, writes it to './controllers/hello_world/behavior.py',
    and returns a JSON response with the generated code.
    """
    data = request.get_json()
    if not data or "instruction" not in data:
        return jsonify({"error": "Missing 'instruction' parameter in JSON payload."}), 400

    instruction = data["instruction"]

    try:
        # Generate the Python code based on the user's instruction.
        code = generate_behavior_code(instruction)

        # Ensure the target directory exists.
        target_dir = "./controllers/hello_world"
        os.makedirs(target_dir, exist_ok=True)

        # Write (or overwrite) the generated code to the file.
        file_path = os.path.join(target_dir, "behavior.py")
        with open(file_path, "w") as f:
            f.write(code)

        return jsonify({
            "message": "Behavior code generated and written successfully.",
            "file": file_path,
            "code": code
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the server on port 8888.
    app.run(port=8888)
