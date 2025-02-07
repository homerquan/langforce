import math

def get_control_values(current_time):
    left_speed = 3.0
    right_speed = 3.0
    amplitude = 0.2
    offset = -0.75
    frequency = 0.5
    wave_position = offset + amplitude * math.sin(2 * math.pi * frequency * current_time)
    return left_speed, right_speed, wave_position