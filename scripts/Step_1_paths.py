# ==============================================================================
#                 MR_DEMUXY CONFIGURATION FILE (demuxy_config.py)
#
# INSTRUCTIONS:
# 1. Update the values below with the full paths relevant to your system.
# 2. DO NOT change the variable names.
# ==============================================================================

# --- Path to the internal 'mr_demuxy' package directory for modification ---
# Example: /Users/kgrond/miniconda3/lib/python3.13/site-packages/mr_demuxy
MR_DEMUXY_INTERNAL_PATH = "/Users/kgrond/miniconda3/envs/mr-demuxy_python-3/lib/python3.1/site-packages/mr_demuxy"

# --- Project/Data Directory ---
# Directory where the output folder will be created.
PROJECT_DIR = "/Users/kgrond/Desktop/INBRE-DataScience/Mr_demuxy/2025-10-14_16Sdata_Uhlik/"

# --- Input File Paths (Full Paths) ---
R1_FASTQ_PATH = "/Users/kgrond/Desktop/INBRE-DataScience/Mr_demuxy/2025-10-14_16Sdata_Uhlik/U109-S186-R196-plate3-Uhlik_S3_L001_R1_001.fastq"
R2_FASTQ_PATH = "/Users/kgrond/Desktop/INBRE-DataScience/Mr_demuxy/2025-10-14_16Sdata_Uhlik/U109-S186-R196-plate3-Uhlik_S3_L001_R2_001.fastq"
R1_BARCODE_PATH = "/Users/kgrond/Desktop/INBRE-DataScience/Mr_demuxy/data/R1_barcodes.txt"
R2_BARCODE_PATH = "/Users/kgrond/Desktop/INBRE-DataScience/Mr_demuxy/data/R2_barcodes.txt"

# --- Output Folder Name ---
OUTPUT_DIR_NAME = "demultiplexed_output"