import unittest
import os
from unittest.mock import patch, MagicMock
import json
from llm_tool import call_llm_tool, command_to_wheel_speeds

class TestLLMTool(unittest.TestCase):
    def setUp(self):
        # Ensure a valid test image file is present.
        # Use absolute path relative to this test file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "sample_images", "test1.png")
        
        if not os.path.exists(image_path):
            self.skipTest(f"Test image file '{image_path}' not found.")
        with open(image_path, "rb") as f:
            self.image = f.read()
        
        self.navigation_prompt = (
            "Giving the front image, navigate the robot to the wall."
        )

    @patch("llm_tool.litellm.completion")
    def test_call_llm_tool_forward(self, mock_completion):
        print("\n--- test_call_llm_tool_forward ---")
        
        # Mock response for "forward"
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps({"command": "forward"})
                    }
                }
            ]
        }
        mock_completion.return_value = mock_response

        command = call_llm_tool(self.image, self.navigation_prompt)
        print("Received command:", command)
        self.assertEqual(command, "forward")

    @patch("llm_tool.litellm.completion")
    def test_call_llm_tool_turn_left(self, mock_completion):
        print("\n--- test_call_llm_tool_turn_left ---")
        
        # Mock response for "turn_left"
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps({"command": "turn_left"})
                    }
                }
            ]
        }
        mock_completion.return_value = mock_response

        command = call_llm_tool(self.image, self.navigation_prompt)
        print("Received command:", command)
        self.assertEqual(command, "turn_left")

    @patch("llm_tool.litellm.completion")
    def test_call_llm_tool_error(self, mock_completion):
        print("\n--- test_call_llm_tool_error ---")
        
        # Mock exception
        mock_completion.side_effect = Exception("API Error")

        command = call_llm_tool(self.image, self.navigation_prompt)
        print("Received command:", command)
        self.assertEqual(command, "stop")

    def test_command_to_wheel_speeds(self):
        print("\n--- test_command_to_wheel_speeds ---")
        # Updated expectations based on actual implementation in llm_tool.py
        test_cases = [
            ("forward", (5.0, 5.0)),
            ("backward", (-3.0, -3.0)),
            ("turn left", (-5.0, 5.0)),
            ("turn_left", (-5.0, 5.0)),
            ("turn right", (5.0, -5.0)),
            ("turn_right", (5.0, -5.0)),
            ("stop", (0.0, 0.0)),
            ("invalid", (0.0, 0.0)),
            (None, (0.0, 0.0))
        ]

        for cmd, expected_speeds in test_cases:
            speeds = command_to_wheel_speeds(cmd)
            print(f"Command: {cmd} -> Wheel speeds: {speeds}")
            self.assertEqual(speeds, expected_speeds, f"Failed for command: {cmd}")

if __name__ == '__main__':
    unittest.main()
