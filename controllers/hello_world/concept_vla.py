from transformers import AutoModelForVision2Seq, AutoProcessor
from PIL import Image
import torch

# Load the processor and model from Hugging Face.
# (Here we use "openvla/openvla-7b" as an example; adjust if you want another model.)
processor = AutoProcessor.from_pretrained("openvla/openvla-7b", trust_remote_code=True)
model = AutoModelForVision2Seq.from_pretrained(
    "openvla/openvla-7b",
    attn_implementation="flash_attention_2",  # Optional: improves efficiency if supported.
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    trust_remote_code=True
).to("cuda:0")

# Convert your Webots camera image into a PIL Image.
# For example, if you saved your camera output to disk:
image = Image.open("path_to_your_captured_image.png")

# Define a text prompt that tells the model what you want.
prompt = "In: What action should the robot take to pick up the red ball?\nOut:"

# Process the input (tokenizing both the image and the prompt).
inputs = processor(prompt, image, return_tensors="pt").to("cuda:0", dtype=torch.bfloat16)

# Generate action tokens without sampling (deterministic prediction).
with torch.no_grad():
    action_tokens = model.generate(**inputs, do_sample=False)

# Decode the action tokens into a human-readable command.
# (Decoding details may vary by model—check the model documentation for specifics.)
action_command = processor.decode(action_tokens[0], skip_special_tokens=True)
print("Predicted Action:", action_command)
