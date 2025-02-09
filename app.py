import os
import openai
from flask import Flask, request, jsonify

# Create a Flask app that serves static files from the "www" folder.
app = Flask(__name__, static_folder="www", static_url_path="")

# Optionally, define a route for the root URL ("/") to serve index.html.
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Set up the OpenAI client with your API key.
client = openai.Client(api_key=os.environ.get("OPENAI_API_KEY", "<your own key>"))

def generate_behavior_code(user_instruction: str) -> str:
    """
    Uses the updated OpenAI Python SDK to generate a Python code snippet that
    implements a robot behavior based on the provided natural language instruction.
    The code snippet must define a function `get_control_values(current_time)` that returns:
    left_speed, right_speed, and wave_position.
    """
    system_prompt = (
        "You are an expert robotic behavior programmer. Given a natural language instruction "
        "that describes the behavior the robot should perform, generate a Python code snippet "
        "that implements this behavior. The code should define a function called `get_control_values(current_time)` "
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
        "Now, generate the code based on the following instruction:\n"
        f"\"{user_instruction}\"\n"
    )

    # Use the updated client method to get a chat completion.
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_instruction},
        ],
        model="gpt-4o-mini-2024-07-18",
        temperature=0.7,
    )

    # Extract the generated code from the response.
    code = chat_completion.choices[0].message.content

    # Remove markdown code fence markers if present.
    lines = code.splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    code = "\n".join(lines)
    return code

@app.route('/api/sendCommand', methods=['POST'])
def send_command():
    """
    Expects a JSON payload with an 'instruction' field (e.g., { "instruction": "moving forward" }).
    It generates the corresponding Python code, writes it to './controller/hello_world/behavor.py',
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
    # Run the server on port 8080.
    app.run(port=8080)
