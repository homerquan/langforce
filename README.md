# langforce
A demo of SLM on robotic control

**You need to replace your own API key in app.py**

## Requirements
1. Install Webots on Mac: [Webots Installation Guide](https://cyberbotics.com/doc/guide/installation-procedure#from-the-homebrew-package)
2. Python setup and run server:
   1. **Create a virtual environment:**
      ```bash
      python3 -m venv venv
      ```
   2. **Activate the virtual environment:**
      ```bash
      source venv/bin/activate   # macOS/Linux
      ```
   3. **Install required packages:**
      ```bash
      pip install -r requirements.txt
      ```
   4. **Run the application:**
      ```bash
      python app.py
      ```

## How to demo online
1. Run the demo script:
   ```bash
   sh start.sh