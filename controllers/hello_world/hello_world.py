from controller import Robot
import os
import importlib
import behavior  # Import our behavior module
from llm_tool import call_llm_tool, command_to_wheel_speeds
from PIL import Image
import io
import numpy as np
import base64

# Create the Robot instance.
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Write "stop" to prompt.txt upon initialization.
with open("prompt.txt", "w") as f:
    f.write("stop")

# ---------------------------
# Initialize Base (4 wheels)
# ---------------------------
wheelNames = ["wheel1", "wheel2", "wheel3", "wheel4"]
wheels = []
for name in wheelNames:
    motor = robot.getDevice(name)
    motor.setPosition(float('inf'))  # set wheel motors in velocity mode
    wheels.append(motor)

# ---------------------------
# Initialize Arm Motors
# ---------------------------
armMotorNames = ["arm1", "arm2", "arm3", "arm4", "arm5"]
armMotors = []
for name in armMotorNames:
    motor = robot.getDevice(name)
    armMotors.append(motor)

# Set maximum velocities for the arm motors (example values)
armMotors[0].setVelocity(0.2)
armMotors[1].setVelocity(0.5)
armMotors[2].setVelocity(0.5)  # This joint will perform the waving motion.
armMotors[3].setVelocity(0.3)
armMotors[4].setVelocity(0.3)

# Set fixed positions for the non-waving joints (adjust as needed)
armMotors[0].setPosition(0.0)
armMotors[1].setPosition(-0.55)
armMotors[3].setPosition(-1.5)
armMotors[4].setPosition(0.0)

# Retrieve the camera device by its name defined in the PROTO ("camera")
camera = robot.getDevice('camera')
camera.enable(timestep)

def get_png_image_from_camera(camera):
    """
    Converts the raw image from the Webots camera to PNG bytes.
    The raw image is assumed to be in BGRA format.
    """
    raw_image = camera.getImage()
    if raw_image is None:
        return None
    width = camera.getWidth()
    height = camera.getHeight()
    
    # Convert the raw image to a numpy array.
    image_array = np.frombuffer(raw_image, dtype=np.uint8).reshape((height, width, 4))
    
    # Convert from BGRA to RGB.
    # Take the first three channels and reverse their order.
    image_rgb = image_array[:, :, :3][:, :, ::-1]
    
    # Create an image from the numpy array.
    im = Image.fromarray(image_rgb)
    
    # Save the image to a bytes buffer in PNG format.
    buffer = io.BytesIO()
    im.save(buffer, format="PNG")
    png_data = buffer.getvalue()
    return png_data

# ---------------------------
# Main control loop with hot reload
# ---------------------------
# Initialize variables.
last_prompt_mod_time = None
last_llm_call = 0  # Time of the last LLM call.
current_command = None
prompt = ""  # Initialize with a default prompt if desired.

while robot.step(timestep) != -1:
    current_time = robot.getTime()
    
    # Get the PNG formatted image from the camera.
    png_image = get_png_image_from_camera(camera)
    
    # Always check for prompt.txt updates.
    try:
        mod_time = os.path.getmtime("prompt.txt")
    except OSError:
        mod_time = None  # File not found or inaccessible.
    
    # If prompt.txt has changed, reload it and call the LLM immediately.
    if mod_time is not None and mod_time != last_prompt_mod_time:
        last_prompt_mod_time = mod_time
        with open("prompt.txt", "r") as f:
            prompt = f.read()
        print("Prompt file updated. Reloading prompt.txt:", prompt)
        current_command = call_llm_tool(png_image, prompt)
        last_llm_call = current_time  # Reset the 10s timer.
    
    # Otherwise, if 10 seconds have elapsed since the last LLM call, call the LLM.
    elif current_time - last_llm_call >= 10:
        current_command = call_llm_tool(png_image, prompt)
        last_llm_call = current_time

    # Map the current command to wheel speeds.
    left_speed, right_speed = command_to_wheel_speeds(current_command)
    
    # Apply the wheel velocities.
    wheels[0].setVelocity(left_speed)
    wheels[1].setVelocity(right_speed)
    wheels[2].setVelocity(left_speed)
    wheels[3].setVelocity(right_speed)