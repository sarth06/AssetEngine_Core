import os
import sys
import subprocess
from google import genai
from google.genai import types

# ---------------------------------------------------------
# 1. SMART API KEY RETRIEVAL
# ---------------------------------------------------------
API_KEY = os.environ.get("GEMINI_API_KEY")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not API_KEY and os.path.exists(os.path.join(BASE_DIR, ".env")):
    with open(os.path.join(BASE_DIR, ".env"), "r") as env_file:
        for line in env_file:
            if line.strip().startswith("GEMINI_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip()
                break

if not API_KEY:
    print("[CRITICAL ERROR] GEMINI_API_KEY could not be found.")
    sys.exit(1)

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"[CRITICAL] Failed to initialize Gemini Client: {e}")
    sys.exit(1)

# ---------------------------------------------------------
# 2. NATIVE TOOL DEFINITION (With Strict LLM Guardrails)
# ---------------------------------------------------------
def apply_image_filter(image_filename: str, filter_mode: str) -> str:
    """
    Passes an image to the native AeroCanvas engine to apply a mathematical filter.

    Args:
        image_filename: The name of the file (e.g., 'true_binary.ppm').
        filter_mode: MUST be one of these exact strings: 'invert', 'blur', 'edge', 'sharpen', 'grayscale'.
    """

    # FIX 1: Sanitize the filename to strip out any folder paths the LLM tries to guess
    clean_filename = os.path.basename(image_filename)

    print(f"\n[SYSTEM] Triggering Native Engine -> File: {clean_filename} | Mode: {filter_mode}")

    workspace_dir = os.path.join(BASE_DIR, "workspace_data")
    engine_path = os.path.join(BASE_DIR, "AeroCanvas.exe")

    input_path = os.path.join(workspace_dir, clean_filename)
    output_path = os.path.join(workspace_dir, "high_res_output.ppm")

    if not os.path.exists(input_path):
        return f"Error: The file '{clean_filename}' does not exist in the workspace directory."

    try:
        subprocess.run([engine_path, input_path, output_path, filter_mode], check=True)
        return f"Success! The engine applied '{filter_mode}' and saved the result to high_res_output.ppm"
    except Exception as e:
        return f"Engine Failure: {e}"

# ---------------------------------------------------------
# 3. AGENT CHAT LOOP
# ---------------------------------------------------------
print("========================================")
print(" AeroCanvas AI Orchestrator Online")
print("========================================")

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        tools=[apply_image_filter],
        temperature=0.0, # FIX 2: Set temperature to 0.0 for absolute strictness
        system_instruction="You are the AI interface for AeroCanvas. Convert user requests into tool calls. The default test image is 'true_binary.ppm'. Never guess filter names; use only the explicit filter_mode options provided in the tool documentation."
    )
)

while True:
    user_input = input("\n[You]: ")
    if user_input.lower() in ['exit', 'quit']:
        break

    response = chat.send_message(user_input)
    print(f"[AeroCanvas AI]: {response.text}")