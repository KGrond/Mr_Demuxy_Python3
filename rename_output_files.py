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