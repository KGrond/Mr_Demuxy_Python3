import os

script_path = '/Users/kgrond/miniconda3/lib/python3.13/site-packages/mr_demuxy/'

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