# Update Mr Demuxy for python 3+

## Step 1: Install Mr Demuxy following https://github.com/lefeverde/Mr_Demuxy

## Step 2: Find Mr. Demuxy Installation Path


```python
!pip show Mr_Demuxy
```

## Step 3: Add Mr. Demuxy to the PATH (Modify the path accordingly)


```python
import os

mr_demuxy_path = "/your/path/to/mr_demuxy/"
os.environ["PATH"] = f"{mr_demuxy_path}:{os.environ['PATH']}"
!echo $PATH
```

## Step 4: Update scripts to run with Python 3


```python
import os

script_path = '/your/path/to/mr_demuxy/'

scripts = {
    "pe_demuxer": script_path + 'pe_demuxer_dist.py',
    "util_functions": script_path + 'util_functions_dist.py',
    "biopython": script_path + 'biopython.py'
}

def replace_text(file_path, old, new):
    try:
        with open(file_path, 'r+') as file:
            content = file.read()
            file.seek(0)
            file.write(content.replace(old, new))
            file.truncate()
        print(f"Updated '{file_path}' successfully.")
    except FileNotFoundError:
        print(f"Script not found: '{file_path}'")
    except Exception as e:
        print(f"An error occurred '{file_path}': {e}")

for script in [scripts["pe_demuxer"], scripts["util_functions"]]:
    replace_text(script, "rU", "r")

replace_text(scripts["biopython"], "raise StopIteration", "return")
```

## Step 5: Run Mr. Demuxy (Modify paths as needed)


```python
import os

data_path = "/your/path/to/data"
os.chdir(data_path)

!pe_demuxer.py -r1 R1.fastq -r2 R2.fastq -r1_bc R1_barcodes.txt -r2_bc R2_barcodes.txt -o demultiplexed
```

# (Optional) Rename demultiplexed samples

## Step 6: Rename samples to match metadata


```python
!head -n 10 /your/path/to/data/metadata.csv # identify column headers for sample name and well (location in the 96-well plate)
```

## Step 7: Run renaming script. 


```python
import os
import pandas as pd

demultiplexed_dir = "/your/path/to/data/demultiplexed"
metadata_file = "/your/path/to/data/metadata.csv"

well_column_name = "WellName" 
sample_column_name = "SampleID"

metadata = pd.read_csv(metadata_file)

if well_column_name not in metadata.columns or sample_column_name not in metadata.columns:
    raise ValueError(f"Metadata must contain '{well_column_name}' and '{sample_column_name}' columns.")

well_to_sample = dict(zip(metadata[well_column_name], metadata[sample_column_name]))

for root, _, files in os.walk(demultiplexed_dir):
    for filename in files:
        if filename.endswith(".fastq"):
            well_name = filename.split("_")[0]

            if well_name in well_to_sample:
                sample_id = well_to_sample[well_name]
                new_filename = filename.replace(well_name, sample_id)
                os.rename(os.path.join(root, filename), os.path.join(root, new_filename))
                print(f"Renamed: {filename} -> {new_filename}")
            else:
                print(f"Warning: Well name '{well_name}' not found in metadata. Skipping '{filename}'.")
```
