#!/bin/bash

# ==============================================================================
#                 MR_DEMUXY FULL AUTOMATION WORKFLOW
# ==============================================================================

# --- Configuration ---
CONDA_ENV_NAME="mr-demuxy_python-3"
PYTHON_VERSION="3.12" 
PATCH_SCRIPT="Step-2_update-demuxy-scripts-for-python3.py"
RUN_SCRIPT="Step-3_run-demuxy-python3.py"

# --- Script Start ---

echo "--- 1. Setting up Conda Environment ---"
if ! command -v conda &> /dev/null
then
    echo "ERROR: Conda is not installed or not in your PATH. Please install Conda first."
    exit 1
fi

# Ensure base conda is sourced (essential for reliable activation)
# Using `source` is necessary for `conda activate` to work reliably in scripts.
source "$(conda info --base)/etc/profile.d/conda.sh"

# Create the environment if it doesn't exist, otherwise activate it
if conda info --envs | grep -q "${CONDA_ENV_NAME}"; then
    echo "Environment '${CONDA_ENV_NAME}' already exists. Activating..."
    conda activate "${CONDA_ENV_NAME}"
else
    echo "Creating new environment '${CONDA_ENV_NAME}' with Python ${PYTHON_VERSION}..."
    conda create -n "${CONDA_ENV_NAME}" python="${PYTHON_VERSION}" -y
    conda activate "${CONDA_ENV_NAME}"
fi

if [ $? -ne 0 ]; then
    echo "ERROR: Conda environment activation failed. Exiting."
    exit 1
fi

echo "--- 2. Checking and Installing Mr_Demuxy ---"
if pip show Mr_Demuxy &> /dev/null; then
    echo "Mr_Demuxy is already installed in '${CONDA_ENV_NAME}'. Skipping installation."
else
    echo "Mr_Demuxy not found. Installing via pip..."
    pip install Mr_Demuxy
    if [ $? -ne 0 ]; then
        echo "ERROR: Installation of Mr_Demuxy failed. Exiting."
        exit 1
    fi
fi

# --- 3. Determine the EXACT installation path for patching using $CONDA_PREFIX ---
# $CONDA_PREFIX is set by 'conda activate' to the environment's root directory.
# We explicitly construct the path based on Conda's known internal structure.
# NOTE: The Python version is 3.12, but we use the general 'lib' path for flexibility.
MR_DEMUXY_INSTALL_PATH="${CONDA_PREFIX}/lib/python${PYTHON_VERSION:0:3}/site-packages/mr_demuxy/"

echo "Targeting package path: ${MR_DEMUXY_INSTALL_PATH}"

echo "--- 4. Running Python 3 Patch Script ---"

# Use sed to replace the hardcoded 'script_path' variable in the patch script 
# with the reliably calculated path from the activated environment.
PATCH_CONTENT=$(cat "${PATCH_SCRIPT}")
FIXED_PATCH_CONTENT=$(echo "$PATCH_CONTENT" | sed "s|script_path = .*|script_path = \"${MR_DEMUXY_INSTALL_PATH}\"|g")

# Execute the modified patch script content
echo "$FIXED_PATCH_CONTENT" | python

if [ $? -ne 0 ]; then
    echo "--- CRITICAL FAILURE: Python Patch Script failed. Check output above. ---"
    conda deactivate
    exit 1
fi

echo "--- 5. Running Mr_Demuxy Demultiplexing Script ---"

# The run script will use the patched files and read paths from Step_1_paths.py
python "${RUN_SCRIPT}"

# Check the exit status of the run script
if [ $? -eq 0 ]; then
    echo "--- Workflow completed successfully! ---"
else
    echo "--- CRITICAL FAILURE: Mr_Demuxy Run Script failed. Check the output above. ---"
fi

echo "--- Deactivating Conda Environment ---"
conda deactivate

echo "Script finished."