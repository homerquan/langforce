from controller import Robot
import math

# Create the Robot instance.
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# ---------------------------
# Initialize Base (4 wheels)
# ---------------------------
wheelNames = ["wheel1", "wheel2", "wheel3", "wheel4"]
wheels = []
for name in wheelNames:
    motor = robot.getDevice(name)
    motor.setPosition(float('inf'))
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

# Set fixed positions for the non-waving joints (adjust these as needed)
armMotors[0].setPosition(0.0)
armMotors[1].setPosition(-0.55)
armMotors[3].setPosition(-1.5)
armMotors[4].setPosition(0.0)

# ---------------------------
# Main control loop
# ---------------------------
while robot.step(timestep) != -1:
    current_time = robot.getTime()
    
    # Drive in a curve:
    # (Assuming wheels[0] & wheels[1] are on the left and wheels[2] & wheels[3] are on the right.)
    left_speed = 5.0    # Left wheels slower.
    right_speed = 7.0   # Right wheels faster.
    wheels[0].setVelocity(left_speed)
    wheels[1].setVelocity(left_speed)
    wheels[2].setVelocity(right_speed)
    wheels[3].setVelocity(right_speed)
    
    # Wave the arm slower but with a bigger range:
    amplitude = 0.8     # Increased amplitude (radians)
    offset = -0.75      # Center position (adjust as needed)
    frequency = 0.25    # Slower frequency (0.25 Hz => one oscillation every 4 seconds)
    wave_position = offset + amplitude * math.sin(2 * math.pi * frequency * current_time)
    armMotors[2].setPosition(wave_position)
