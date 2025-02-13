import unittest
import os
from llm_tool import call_llm_tool, llm_navigation_tool, command_to_wheel_speeds

class TestLLMTool(unittest.TestCase):
    def setUp(self):
        # Ensure a valid test image file is present.
        image_path = "sample_images/test1.png"
        if not os.path.exists(image_path):
            self.skipTest("Test image file 'test_image.png' not found.")
        with open(image_path, "rb") as f:
            self.image = f.read()
        
        self.navigation_prompt = (
            "front image, help robot to navigate, output: using tools: forward, "
            "using tools: backward, using tools: stop, using tools: turn left, "
            "using tools: turn right"
        )

    def test_call_llm_tool(self):
        print("\n--- test_call_llm_tool ---")
        print("Navigation prompt:", self.navigation_prompt)
        command = call_llm_tool(self.image, self.navigation_prompt)
        print("Received command:", command)
        self.assertIn(
            command, 
            ["forward", "backward", "stop", "turn left", "turn right"],
            msg=f"Unexpected command received: {command}"
        )

    def test_llm_navigation_tool(self):
        print("\n--- test_llm_navigation_tool ---")
        command = llm_navigation_tool(self.image)
        print("Received command from llm_navigation_tool:", command)
        self.assertIn(
            command, 
            ["forward", "backward", "stop", "turn left", "turn right"],
            msg=f"Unexpected command received: {command}"
        )

    def test_command_to_wheel_speeds(self):
        print("\n--- test_command_to_wheel_speeds ---")
        commands = ["forward", "backward", "turn left", "turn right", "stop"]
        for cmd in commands:
            speeds = command_to_wheel_speeds(cmd)
            print(f"Command: {cmd} -> Wheel speeds: {speeds}")
            if cmd == "forward":
                self.assertEqual(speeds, (2.0, 2.0))
            elif cmd == "backward":
                self.assertEqual(speeds, (-2.0, -2.0))
            elif cmd == "turn left":
                self.assertEqual(speeds, (-1.0, 1.0))
            elif cmd == "turn right":
                self.assertEqual(speeds, (1.0, -1.0))
            elif cmd == "stop":
                self.assertEqual(speeds, (0.0, 0.0))

if __name__ == '__main__':
    unittest.main()
