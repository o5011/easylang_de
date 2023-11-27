import json
import os

from extract_nouns import extract_nouns
from tqdm import tqdm

DATA_DIR = "transcriptions"
OUTPUT_DIR = "nouns"

# Get all json files in the current directory
json_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]

json_files = sorted(json_files)

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

for file in tqdm(json_files):
    video_name = file.replace(".json", "")
    # Video name is in the format:
    # "10 Austrian Words that Germans don't understand ｜ Easy German 222 [sOXjxZY4FUg]"
    # Create json target file name in output directory
    json_file = os.path.join(OUTPUT_DIR, file)

    # If the json file already exists, skip it
    if os.path.exists(json_file):
        continue

    # Split the last space and get the video id
    video_id = video_name.split(" ")[-1].replace("[", "").replace("]", "")
    video_title = " ".join(video_name.split(" ")[:-1])
    video_link = f"https://www.youtube.com/watch?v={video_id}"

    data = json.load(open(os.path.join(DATA_DIR, file), "r"))
    text = data["text"]
    doc_spacy, options, nouns = extract_nouns(text)

    output = {
        "video_id": video_id,
        "video_title": video_title,
        "video_link": video_link,
        "nouns": nouns,
    }
    json.dump(output, open(json_file, "w"), indent=2)
