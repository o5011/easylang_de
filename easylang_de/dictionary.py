from easylang_de.genus import Genus


CORRECT_GENDERS = {}


with open("nomen_genus.csv", "r") as f:
    lines = f.readlines()[1:]
    for line in lines:
        noun, genus = line.split(",")
        genus = Genus(genus.strip())
        noun = noun.strip().lower()
        if noun not in CORRECT_GENDERS:
            CORRECT_GENDERS[noun] = []

        CORRECT_GENDERS[noun].append(genus)

# Get the nouns with multiple genders
for key, val in CORRECT_GENDERS.items():
    if len(val) > 1:
        print(key, val)