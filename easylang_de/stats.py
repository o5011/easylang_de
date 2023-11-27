import json
import os
from tqdm import tqdm

MP3_DIR = "data"
TRANSCIPTION_DIR = "transcriptions"

# Count the number of .mp3 files under MP3_DIR
mp3_count = 0
mp3_durations = []
for root, dirs, files in os.walk(MP3_DIR):
    for file in tqdm(files):
        if file.endswith(".mp3"):
            mp3_count += 1
            # Get durations of .mp3 files under MP3_DIR
            duration = os.popen(
                f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{os.path.join(root, file)}"'
            ).read()
            duration = float(duration)
            mp3_durations.append(duration)


texts = []
# Get texts from .json files under TRANSCIPTION_DIR
for root, dirs, files in os.walk(TRANSCIPTION_DIR):
    for file in files:
        if file.endswith(".json"):
            data = json.load(open(os.path.join(root, file)))
            texts.append(data["text"])

texts_merged = " ".join(texts)

# Count the number of words in the texts
word_count = len(texts_merged.split())

# Count the number of characters in the texts
char_count = len(texts_merged)
# Count the number of sentences in the texts through punctuation marks
sentence_count = (
    texts_merged.count(".") + texts_merged.count("?") + texts_merged.count("!")
)

# Print the statistics
print("Number of videos:     " + str(mp3_count))
print("Total duration:       " + str(sum(mp3_durations) / 60 / 60) + " hours")
print("Number of words:      " + str(word_count))
print("Number of characters: " + str(char_count))
print("Number of sentences:  " + str(sentence_count))
