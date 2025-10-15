# Setup and Execution

## Follow these three steps for a seamless demultiplexing run.

### Step 1: Configure Your Paths (Edit Step-1_paths.py)
Open the file Step-1_paths.py in a text editor and update all the placeholder paths to match your files and desired directories.

The most important path to configure is the MR_DEMUXY_INTERNAL_PATH. Since the shell script will automatically create a Conda environment named mr-demuxy_python-3, the internal path for the package files will look similar to this:

/path/to/miniconda/envs/mr-demuxy_python-3/lib/python3.12/site-packages/mr_demuxy

to find where Mr Demuxy is installed, copy the below in your terminal:

```
pip show Mr_demuxy
```
You will see a path after **Location:**, which is what you should use and add the final folder **mr_demuxy** to. 


### Step 2: Make the Workflow Script Executable

In your terminal, navigate to the directory containing the three workflow files (Step-1_paths.py,run_demuxy_workflow.sh, Step-2_update-and-run-demuxy-python3.py) are located, and give the shell script permission to run:

```
chmod +x run_demuxy_workflow.sh
```

### Step 3: Run the Pipeline

Execute the automation script. This single command handles the entire setup, installation, and execution process:

```
./run_demuxy_workflow.sh
```

What the Script Does:

- Environment Setup: Creates (or activates) a dedicated Conda environment named mr-demuxy_python-3 using a stable version of Python (3.12).
- Installation: Installs the Mr_Demuxy package via pip.
- Execution: Runs Step-2_update-and-run-demuxy-python3.py, which:
- Imports your paths.
- Applies your custom Python 3 compatibility patches.
- Executes the final pe_demuxer.py command using the full list of input files.
- Cleanup: Deactivates the Conda environment.


# Troubleshooting
1. **"CRITICAL ERROR: Please update all placeholder paths..."**
-> Cause: You missed updating a path in Step-1_paths.py or left a placeholder value (/path/to/...).
- Fix: Open Step-1_paths.py and ensure every variable contains a correct, absolute path.

2. **"ERROR: Mr_Demuxy failed with exit code..."**  
-> Cause: The demultiplexing process failed. This is typically due to file content issues (malformed FASTQ) or incorrect parameters (barcodes not found).
- Fix: Check the terminal output just above the error message for specific messages from pe_demuxer.py regarding the failure.

3. **Error during Patching**  
-> Cause: If the patching script fails, it likely means the MR_DEMUXY_INTERNAL_PATH in Step-1_paths.py is incorrect, and your script can't find the files it needs to modify.
- Fix: Check the Conda environment directory (/path/to/miniconda/envs/mr-demuxy_python-3/...) to find the exact location of the mr_demuxy folder and update the path in your configuration file.







