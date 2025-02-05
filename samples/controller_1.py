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
# Assume 5 arm motors with names "arm1" to "arm5"
armMotorNames = ["arm1", "arm2", "arm3", "arm4", "arm5"]
armMotors = []
for name in armMotorNames:
    motor = robot.getDevice(name)
    armMotors.append(motor)

# Set maximum velocities for the arm motors (example values)
armMotors[0].setVelocity(0.2)
armMotors[1].setVelocity(0.5)
armMotors[2].setVelocity(0.5)  # This joint will wave.
armMotors[3].setVelocity(0.3)
armMotors[4].setVelocity(0.3)

# Set fixed positions for the non-waving joints (modify as needed)
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
    # Example: set the left wheels slower than the right wheels.
    # (Assuming wheels[0] & wheels[1] are on the left side and wheels[2] & wheels[3] on the right.)
    left_speed = 5.0    # slower speed for left wheels
    right_speed = 7.0   # faster speed for right wheels
    wheels[0].setVelocity(left_speed)
    wheels[1].setVelocity(left_speed)
    wheels[2].setVelocity(right_speed)
    wheels[3].setVelocity(right_speed)
    
    # Wave the arm harder:
    # Increase the amplitude and frequency of the oscillation for a more vigorous waving motion.
    amplitude = 0.5     # Increased amplitude (radians)
    offset = -0.75      # Adjust this offset to match your arm's neutral position.
    frequency = 1.0     # Increased frequency in Hz (1 oscillation per second)
    wave_position = offset + amplitude * math.sin(2 * math.pi * frequency * current_time)
    armMotors[2].setPosition(wave_position)
