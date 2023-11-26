from copy import deepcopy
import json
import os
from easylang_de.dictionary import CORRECT_GENDERS

from easylang_de.genus import RESOLVERS, Genus, Kasus, Numerus


NOUNS_DIR = "nouns"

MORPH_KASUS = {
    "Acc": Kasus.ACC,
    "Dat": Kasus.DAT,
    "Gen": Kasus.GEN,
    "Nom": Kasus.NOM,
}
MORPH_NUMERUS = {
    "Plur": Numerus.PL,
    "Sing": Numerus.SG,
}
MORPH_GENUS = {
    "Masc": Genus.M,
    "Fem": Genus.F,
    "Neut": Genus.N,
}

GENUS_CORRECT = open("stats/genus_correct.txt", "w")
GENUS_INCORRECT = open("stats/genus_incorrect.txt", "w")


# Get all JSON files under NOUNS_DIR
json_files = []
for root, dirs, files in os.walk(NOUNS_DIR):
    for file in files:
        if file.endswith(".json"):
            json_files.append(os.path.join(root, file))

determiners = []

# Process each JSON file
correct_texts = []
incorrect_texts = []
missing_cases = []
incorrect_each_file = []
for file in json_files:
    data = json.load(open(file))
    spans = data["nouns"]
    current_incorrect = deepcopy(data)
    current_incorrect.pop("nouns")
    current_incorrect["incorrect"] = []

    for span in spans:
        # for word in noun:
        #     if word["pos"] == "DET":
        #         determiners.append(word["text"].lower())
        det = span[0]
        noun = span[-1]

        det_ = det["text"].lower()
        if "lemma" in noun:
            noun_ = noun["lemma"].lower()
        else:
            noun_ = noun["text"].lower()

        # if not noun_ in CORRECT_GENDERS or not det_ in RESOLVERS:
        #     continue
        correct_genders = CORRECT_GENDERS.get(noun_)
        resolver = RESOLVERS.get(det_)

        if correct_genders is None or resolver is None:
            continue

        try:
            kasus_spacy = MORPH_KASUS.get(noun["morph"]["Case"])
            numerus_spacy = MORPH_NUMERUS.get(noun["morph"]["Number"])
            # genus_spacy = MORPH_GENUS.get(noun["morph"]["Gender"])
        except KeyError:
            missing_cases.append(noun)
            continue

        #####################################
        # This is where I check for errors  #
        #####################################

        # If we were to trust the case returned by Spacy, we would only need to
        # just the following line is enough:
        is_correct = resolver.check_possible_genera(
            kasus_spacy, numerus_spacy, correct_genders
        )

        # However, I saw from trial and error that Spacy sometimes returns the
        # wrong case. So I made the check less strict when Spacy detects anything
        # other than nominative case:
        #
        # if kasus_spacy == Kasus.NOM:
        #     is_correct = resolver.check_possible_genera(
        #         kasus_spacy, numerus_spacy, correct_genders
        #     )
        # else:
        #     is_correct1 = resolver.check_possible_genera(
        #         Kasus.NOM, numerus_spacy, correct_genders
        #     )
        #     is_correct2 = resolver.check_possible_genera(
        #         Kasus.ACC, numerus_spacy, correct_genders
        #     )
        #     is_correct3 = resolver.check_possible_genera(
        #         Kasus.DAT, numerus_spacy, correct_genders
        #     )
        #     is_correct4 = resolver.check_possible_genera(
        #         Kasus.GEN, numerus_spacy, correct_genders
        #     )
        #     is_correct = is_correct1 or is_correct2 or is_correct3 or is_correct4
        #
        # is_correct = genus_spacy in correct_genders

        text = " ".join([i["text"] for i in span])
        print(f"{text}, {correct_genders}, {noun['morph']}, {is_correct}")

        if is_correct:
            GENUS_CORRECT.write(f"{text}\n")
            correct_texts.append(text)
        else:
            insert = f"{text}, {correct_genders}, {noun['morph']}"
            GENUS_INCORRECT.write(f"{insert}\n")
            incorrect_texts.append(text)

            # if file not in incorrect_per_file:
            current_incorrect["incorrect"].append(insert)

    if len(current_incorrect["incorrect"]) > 0:
        incorrect_each_file.append(current_incorrect)

total = len(correct_texts) + len(incorrect_texts)
error_rate = len(incorrect_texts) / total

print(f"Number of nouns: {total}")
print(f"Number of correct genus assignment: {len(correct_texts)}")
print(f"Number of definitely incorrect genus assignment: {len(incorrect_texts)}")
print(f"Error rate: {error_rate} ({error_rate*100}%))")
print(f"Missing cases: {len(missing_cases)}")

ofile = open("stats/incorrect_each_file.json", "w")
json.dump(incorrect_each_file, ofile, indent=4)
