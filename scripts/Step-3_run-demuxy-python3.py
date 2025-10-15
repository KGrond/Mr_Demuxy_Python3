import os
import sys
import subprocess

# Import all variables from the configuration file
try:
    from Step_1_paths import *
except ImportError:
    print("CRITICAL ERROR: Could not find 'Step-1_paths.py'. Ensure it is in the same directory.")
    sys.exit(1)

# --- Patching Utility Functions ---

def replace_text(file_path, old, new):
    """Replaces all occurrences of 'old' text with 'new' text in a file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Only rewrite if content actually needs changing
        if old in content:
            new_content = content.replace(old, new)
            with open(file_path, 'w') as file:
                file.write(new_content)
            print(f"Updated '{os.path.basename(file_path)}': replaced '{old}' with '{new}'.")
        else:
            print(f"File '{os.path.basename(file_path)}' already patched or pattern not found.")

    except FileNotFoundError:
        print(f"ERROR: Script not found at: '{file_path}'")
        # Critical failure: Exit the program
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while patching '{file_path}': {e}")
        # Critical failure: Exit the program
        sys.exit(1)


def apply_python3_patches(demuxy_path):
    """
    Applies patches needed for Mr_Demuxy to run on Python 3 using 
    the specific logic requested by the user (rU removal and StopIteration fix).
    """
    print(f"--- Applying Python 3 patches to files in: {demuxy_path} ---")
    
    # 1. Sanity Check for the path
    if "path/to/the/internal/mr_demuxy" in demuxy_path:
        print("WARNING: MR_DEMUXY_INTERNAL_PATH in Step-1_paths.py looks like a placeholder. Skipping patch application.")
        return

    # 2. Define script paths using os.path.join() (FIXED)
    scripts = {
        "pe_demuxer": os.path.join(demuxy_path, 'pe_demuxer_dist.py'),
        "util_functions": os.path.join(demuxy_path, 'util_functions_dist.py'),
        "biopython": os.path.join(demuxy_path, 'biopython.py')
    }
    
    # 3. Apply the 'rU' to 'r' patch (Fixes the ValueError: invalid mode: 'rU')
    for script in [scripts["pe_demuxer"], scripts["util_functions"]]:
        replace_text(script, "rU", "r")

    # 4. Apply the 'raise StopIteration' to 'return' patch (Fixes Python 3 iteration compatibility)
    replace_text(scripts["biopython"], "raise StopIteration", "return")

    print("Patches applied successfully.")


def run_demuxy():
    """
    Constructs and executes the pe_demuxer.py command using subprocess.
    """
    print("\n--- Preparing to run Mr_Demuxy ---")
    
    # 1. Change to the project directory
    try:
        os.chdir(PROJECT_DIR)
        print(f"Changed directory to: {PROJECT_DIR}")
    except FileNotFoundError:
        print(f"Error: Project directory not found at {PROJECT_DIR}. Exiting.")
        sys.exit(1)

    # 2. Construct the shell command as a single, quoted string 
    # This is the reliable method when using shell=True to avoid argument parsing issues.
    command_string = (
        f"pe_demuxer.py "
        f"-r1 '{R1_FASTQ_PATH}' "
        f"-r2 '{R2_FASTQ_PATH}' "
        f"-r1_bc '{R1_BARCODE_PATH}' "
        f"-r2_bc '{R2_BARCODE_PATH}' "
        f"-o '{OUTPUT_DIR_NAME}'"
    )

    # 3. Execute the command
    print("\nExecuting command:")
    print(command_string)
    
    # Use subprocess.run with the single string command and shell=True 
    try:
        subprocess.run(command_string, check=True, shell=True) 
        print("\n--- Mr_Demuxy completed successfully! ---")
        print(f"Output is in: {PROJECT_DIR}/{OUTPUT_DIR_NAME}")
    except subprocess.CalledProcessError as e:
        print(f"\n--- ERROR: Mr_Demuxy failed with exit code {e.returncode} ---")
        print("Please check the terminal output for specific error messages.")
        # Exit with the failure code from the demuxer
        sys.exit(e.returncode) 
    except FileNotFoundError:
        print("\nERROR: 'pe_demuxer.py' not found. Ensure it was installed correctly in the conda environment.")
        sys.exit(1)


if __name__ == "__main__":
    
    # Initial check for placeholder paths
    if "path/to/" in R1_FASTQ_PATH:
        print("CRITICAL ERROR: Please update all placeholder paths in Step-1_paths.py before running.")
        sys.exit(1)
        
    # Step 1: Apply necessary Python 3 patches
    apply_python3_patches(MR_DEMUXY_INTERNAL_PATH)
    
    # Step 2: Run the demultiplexing command
    run_demuxy()