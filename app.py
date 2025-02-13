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

@app.route('/api/sendCommand', methods=['POST'])
def send_command():
    """
    Expects a JSON payload with an 'instruction' field (e.g., { "instruction": "moving forward" }).
    It saves the instruction to "prompt.txt" at "./controllers/hello_world".
    """
    data = request.get_json()
    if not data or "instruction" not in data:
        return jsonify({"error": "Missing 'instruction' parameter in JSON payload."}), 400

    instruction = data["instruction"]

    try:
        # Ensure the target directory exists.
        target_dir = "./controllers/hello_world"
        os.makedirs(target_dir, exist_ok=True)

        # Write (or overwrite) the instruction to "prompt.txt".
        file_path = os.path.join(target_dir, "prompt.txt")
        with open(file_path, "w") as f:
            f.write(instruction)

        return jsonify({
            "message": "Instruction saved successfully.",
            "file": file_path,
            "instruction": instruction
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Run the server on port 8888.
    app.run(port=8888)
