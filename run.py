
import subprocess
import os
import signal
import time
import platform

def get_process_children(pid):
    if platform.system() == "Windows":
        # This is a simplified version for Windows. A more robust solution might be needed.
        return []
    else:
        try:
            # Run the pgrep command to find child processes
            result = subprocess.run(['pgrep', '-P', str(pid)], capture_output=True, text=True, check=True)
            # The output is a string of PIDs, separated by newlines.
            # We filter out any empty strings that might result from splitting.
            return [int(p) for p in result.stdout.strip().split('\n') if p]
        except (subprocess.CalledProcessError, FileNotFoundError):
            # pgrep might not be installed or the process might not have children
            return []

def kill_proc_tree(pid, sig=signal.SIGTERM):
    try:
        children = get_process_children(pid)
        for child_pid in children:
            kill_proc_tree(child_pid, sig)
        os.kill(pid, sig)
    except OSError as e:
        print(f"Error killing process {pid}: {e}")


def main():
    # --- Commands to run ---
    backend_command = "uvicorn main:app --reload"
    frontend_command = "npm run dev"

    # --- Directories ---
    backend_dir = "backend"
    frontend_dir = "frontend"

    # --- Start Backend ---
    print("Starting backend...")
    backend_process = subprocess.Popen(
        backend_command,
        shell=True,
        cwd=backend_dir,
        preexec_fn=os.setsid  # Create a new process group
    )

    # --- Start Frontend ---
    print("Starting frontend...")
    frontend_process = subprocess.Popen(
        frontend_command,
        shell=True,
        cwd=frontend_dir,
        preexec_fn=os.setsid  # Create a new process group
    )

    print("\nBackend and Frontend are running.")
    print("Press 'q' to quit.")

    # --- Wait for 'q' to be pressed ---
    while True:
        try:
            # Using a simple input check for broader compatibility
            user_input = input()
            if user_input.lower() == 'q':
                break
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            # Also allow quitting with Ctrl+C or Ctrl+D
            break


    # --- Terminate Processes ---
    print("\nTerminating processes...")

    # Kill the entire process group (including child processes)
    try:
        if platform.system() == "Windows":
            # For Windows, taskkill is more effective
            subprocess.run(f"taskkill /F /T /PID {backend_process.pid}")
            subprocess.run(f"taskkill /F /T /PID {frontend_process.pid}")
        else:
            # For Unix-like systems, os.killpg is preferred
            os.killpg(os.getpgid(backend_process.pid), signal.SIGTERM)
            os.killpg(os.getpgid(frontend_process.pid), signal.SIGTERM)
    except ProcessLookupError as e:
        print(f"Could not find process to kill: {e}")


    # --- Wait for processes to terminate ---
    backend_process.wait()
    frontend_process.wait()

    print("\nAll processes terminated. Exiting.")

if __name__ == "__main__":
    main()
