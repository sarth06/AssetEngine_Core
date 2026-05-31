import subprocess
import time

def trigger_java_engine():
    print("[Python Agent] Mission Authorized. Waking the Java Engine...")
    
    # 1. Define the exact terminal command to run your Java Main class
    # This is identical to typing it into a Bash/CMD terminal
    java_command = ["java", "-cp", "out/production/AssetEngine_Core", "Main"]
    
    # 2. Execute the command and capture everything the Java engine prints
    try:
        start_time = time.time()
        
        # subprocess.run actually fires the terminal command
        process = subprocess.run(
            java_command, 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        end_time = time.time()
        
        # 3. Output the results
        print("\n[Python Agent] Engine execution complete. Intercepted Logs:")
        print("==================================================")
        print(process.stdout)  # This contains all your Java System.out.printlns!
        print("==================================================")
        print(f"[Python Agent] Total Python oversight time: {(end_time - start_time):.4f} seconds.")
        
    except subprocess.CalledProcessError as e:
        print("[Python Agent] FATAL ERROR: The Java Engine crashed.")
        print(e.stderr)

# Initialize the sequence
if __name__ == "__main__":
    trigger_java_engine()