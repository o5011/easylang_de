import json
import os

import openai
from tqdm import tqdm

DATA_DIR = "data"
OUTPUT_DIR = "transcriptions"

# Get all mp3 files in the current directory
mp3_files = [
    f for f in os.listdir(DATA_DIR) if os.path.isfile(f) and f.endswith(".mp3")
]

mp3_files = sorted(mp3_files)

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

for file in tqdm(mp3_files):
    # Create json target file name in output directory
    json_file = os.path.join(OUTPUT_DIR, file.replace(".mp3", ".json"))

    # If the json file already exists, skip it
    if os.path.exists(json_file):
        print(f"Skipping {file} because {json_file} already exists")
        continue

    # Check if the file is greater than 25MB
    if os.path.getsize(file) > 25 * 1024 * 1024:
        print(f"Skipping {file} because it is greater than 25MB")
        continue

    print(f"Running {file}")
    try:
        output = openai.Audio.transcribe(
            model="whisper-1",
            file=open(file, "rb"),
            format="verbose_json",
        )
        output = output.to_dict()
        json.dump(output, open(json_file, "w"), indent=2)
    except openai.error.APIError:
        print(f"Skipping {file} because of API error")
        continue
