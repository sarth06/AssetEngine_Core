import os
import sys
import json
import requests
from google import genai
from google.genai import types

# 1. SMART API KEY RETRIEVAL LAYER
API_KEY = os.environ.get("GEMINI_API_KEY")

# Fallback: If the Windows environment variable isn't found, look for a local .env file
if not API_KEY and os.path.exists(".env"):
    with open(".env", "r") as env_file:
        for line in env_file:
            if line.strip().startswith("GEMINI_API_KEY="):
                # Split at the '=' symbol and extract the key cleanly
                API_KEY = line.split("=", 1)[1].strip()
                break

if not API_KEY:
    print("[CRITICAL ERROR] GEMINI_API_KEY could not be found.")
    print("Please ensure your key is added to the '.env' file in this directory.")
    sys.exit(1)

# Initialize the modern client
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"[CRITICAL] Failed to initialize Gemini Client: {e}")
    sys.exit(1)

# 2. DEFINE THE NATIVE COMPUTE TOOL
def trigger_native_engine(file_path: str, mode: str) -> str:
    """
    Processes a local .ppm image file using the high-performance native AOT C++ engine.

    Args:
        file_path: The local path to the input .ppm file (e.g., 'assets/true_binary.ppm').
        mode: The mathematical filter matrix to apply. Must be exactly one of these:
              'blur'        -> 3x3 Box Blur matrix transformation
              'invert'      -> Absolute color inversion (Negative)
              'grayscale'   -> Black and white luminosity conversion
              'sharpen'     -> High-pass image sharpening kernel
              'edge'        -> High-contrast edge detection line art kernel
    Returns:
        A JSON formatted string detailing the success asset path or error trace.
    """
    print(f"\n[AGENT TOOL INTERACTION] Gemini initiated 'trigger_native_engine'")
    print(f" -> Target Asset: {file_path}")
    print(f" -> Chosen Mode:  {mode.upper()}")

    if not os.path.exists(file_path):
        return json.dumps({"error": f"Local image source file not found at {file_path}"})

    url = "http://127.0.0.1:8000/process-image/"
    try:
        print("[AGENT NETWORK] Streaming payload chunks to local FastAPI gateway...")
        with open(file_path, "rb") as image_file:
            files = {"file": (os.path.basename(file_path), image_file, "application/octet-stream")}
            data = {"mode": mode}
            response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            print("[AGENT NETWORK] Handshake success. 200 OK returned.")
            return json.dumps(response.json())
        else:
            return json.dumps({"error": f"HTTP {response.status_code}", "details": response.text})
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": "Gateway connection refused. Is your Uvicorn server online?", "details": str(e)})


# 3. AGENT ORCHESTRATION LAYER
SYSTEM_INSTRUCTION = """
You are the master agentic supervisor for AeroCanvas, an ultra-low-latency native image core.
Your purpose is to interpret natural language requests from the human operator, determine the correct mathematical computation matrix, and execute the 'trigger_native_engine' tool.

Map user intents to these modes exactly:
- Blurry / Smooth / Softened -> 'blur'
- Negative / Inverted / Flipped colors -> 'invert'
- Black and White / Gray / Monochrome -> 'grayscale'
- Crisp / Sharp / Detailed -> 'sharpen'
- Sketch / Outline / Line Art / Edges -> 'edge'

Once the tool finishes running, report back to the user with a concise technical summary and the output asset link.
"""

def boot_agent():
    print("\n==================================================")
    print("      AeroCanvas Agentic Interface v2.0           ")
    print("==================================================")
    print("Engine: google-genai SDK (Live Function Calling)")
    print("Ready for processing intents. Type 'exit' to quit.\n")

    # Set up the execution configuration including our tool array
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[trigger_native_engine],
        temperature=0.2 # Lower temperature forces deterministic tool routing
    )

    # Begin automated chat session using the current recommended model tier
    try:
        chat = client.chats.create(model="gemini-2.5-flash", config=config)
    except Exception as e:
        # Fallback to 1.5 if your workspace constraints prefer it
        try:
            chat = client.chats.create(model="gemini-1.5-flash", config=config)
        except Exception as inner_e:
            print(f"[ERROR] Could not build chat session: {inner_e}")
            sys.exit(1)

    while True:
        try:
            user_prompt = input("You: ")
            if user_prompt.lower() in ['exit', 'quit']:
                print("Disconnecting agent core...")
                break

            if not user_prompt.strip():
                continue

            print("Gemini is analyzing matrix routing...")
            response = chat.send_message(user_prompt)
            print(f"\nAI: {response.text}\n")

        except Exception as e:
            print(f"\n[CORE ERROR]: {str(e)}\n")

if __name__ == "__main__":
    boot_agent()