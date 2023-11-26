import argparse
import json
import sys
from typing import Dict, List, Tuple
import spacy
from colour import Color
from spacy import displacy
from spacy.tokens import Span, Token, Doc

MODEL = "de_dep_news_trf"
# MODEL = "de_core_news_lg"
# MODEL = "de_core_news_sm"

try:
    # Load German models for Spacy and Stanza
    nlp_spacy = spacy.load(MODEL)
except OSError:
    import spacy.cli

    print(f"Model {MODEL} not found. Downloading...")
    spacy.cli.download(MODEL)
    "Finished downloading model, please rerun this script"
    sys.exit(0)


def serialize_token(token: Token):
    """
    Serializes relevant information from a token to be saved in a JSON file
    """
    ret = {}
    ret["text"] = token.text
    ret["pos"] = token.pos_
    ret["dep"] = token.dep_
    ret["morph"] = token.morph.to_dict()
    ret["lemma"] = token.lemma_
    ret["shape"] = token.shape_
    ret["tag"] = token.tag_
    ret["lang"] = token.lang_
    ret["prefix"] = token.prefix_
    ret["suffix"] = token.suffix_

    return ret


def extract_nouns(text: str) -> Tuple[Doc, Dict, List]:
    """
    Extracts nouns from a given text and returns the processed Spacy document,
    the displacy options, and a list of nouns for later processing.
    """
    nouns = []

    # Process the sentence with both libraries
    doc_spacy = nlp_spacy(text)

    # Initialize an empty dictionary to store the unique articles
    # and their corresponding colors
    article_colors = {}

    # Create an empty list to contain the entities we want to highlight
    entities = []
    # Print POS tagging and dependency parsing results for debugging
    for token in doc_spacy:
        print(token.text, token.pos_, token.dep_)

    entity_indices = set()

    # Loop through the tokens in the sentence
    for token in doc_spacy:
        # If a noun or follows, pair it with the determiner and any adjectives
        # We could also include proper nouns by adding "PROPN" to the list
        # but that would include names of people, places, etc.
        if token.pos_ in ["NOUN"]:
            case = token.morph
            lefts = list(token.lefts)
            # rights = list(token.rights)
            # print(token.text, token.head, lefts)

            if lefts:
                leftmost_idx = lefts[0].i
            else:
                # leftmost_idx = token.i
                continue

            rightmost_idx = token.i + 1

            # If any of the indices exist in the set of entity indices, skip this token
            if any(idx in entity_indices for idx in range(leftmost_idx, rightmost_idx)):
                continue

            # Add indices leftmost_idx,...,rightmost_idx to the set of entity indices
            entity_indices |= set(range(leftmost_idx, rightmost_idx))

            print(lefts, token, leftmost_idx, token.i)

            tokens = [doc_spacy[i] for i in range(leftmost_idx, rightmost_idx)]
            nouns.append([serialize_token(token) for token in tokens])

            # Construct a new entity spanning from the article to the noun
            # Include the case in the label
            entity = Span(doc_spacy, leftmost_idx, rightmost_idx, label=f"({case})")
            entities.append(entity)

            # For postprocessing
            # Assign a color to the article-case combination if it doesn't have one already
            if entity.label_ not in article_colors:
                # Generate a random color for the article-case combination
                article_colors[entity.label_] = Color(pick_for=entity.label_).hex

    # Overwrite the doc.ents with our new entities
    doc_spacy.ents = entities

    # Set displacy options to use the custom attribute for coloring
    options = {"ents": list(article_colors.keys()), "colors": article_colors}

    return doc_spacy, options, nouns


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract nouns from a JSON file and display a visualization"
    )

    parser.add_argument(
        "json_file", type=str, help="JSON file to display the extracted nouns from"
    )
    args = parser.parse_args()

    # Read json file from the first argument
    with open(args.json_file) as f:
        data = json.load(f)

    doc_spacy, options, nouns = extract_nouns(data["text"])

    # Serve the visualization
    displacy.serve(doc_spacy, style="ent", options=options)
