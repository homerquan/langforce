from controller import Robot
import importlib
import behavior  # Import our behavior module

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

# ---------------------------
# Main control loop with hot reload
# ---------------------------
while robot.step(timestep) != -1:
    current_time = robot.getTime()
    
    # Reload the behavior module so that any changes on disk are applied.
    importlib.reload(behavior)
    
    # Get updated control values from the (possibly updated) behavior module.
    left_speed, right_speed, wave_position = behavior.get_control_values(current_time)
    
    # Apply the wheel velocities.
    wheels[0].setVelocity(left_speed)
    wheels[1].setVelocity(right_speed)
    wheels[2].setVelocity(left_speed)
    wheels[3].setVelocity(right_speed)
    
    # Update the waving joint.
    armMotors[2].setPosition(wave_position)
