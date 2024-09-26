"""A script to count word families in a text file."""

from collections import Counter
import re
import argparse
import logging
from typing import Tuple, Dict, List
import spacy  # Import spaCy
from contractions import fix  # type: ignore

# Precompile regular expressions for performance
CONTRACTION_SPLIT_REGEX = re.compile(r"(\w+)('ll|'ve|'re|'s|'m|'d)\b")
COMPOUND_WORD_REGEX = re.compile(r"(\w+)(-\w+)+")
REMOVE_CONTRACTIONS_REGEX = re.compile(r"\b('ll|'ve|'re|'s|'m|'d|ll|ve|re|s|m|d)\b")
REMOVE_APOSTROPHE_REGEX = re.compile(r"'")
NUMBER_FILTER_REGEX = re.compile(r"^[\d,\.]+$")


def setup_logging(verbose: bool = False) -> None:
    """Configure the logging settings."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def load_spacy_pipeline(language: str = "en") -> spacy.Language:
    """Load the spaCy pipeline."""
    try:
        # nlp = spacy.load(language, disable=["ner"])
        nlp = spacy.load(language, disable=["ner", "parser"])
        logging.info("Loaded spaCy model for language '%s'.", language)
        return nlp
    except Exception as e:
        logging.error("Error loading spaCy model for language '%s': %s", language, e)
        raise


def preprocess_text(text: str) -> str:
    """
    Preprocess the text by expanding contractions, handling compound words,
    and removing unwanted characters.
    """
    # Split invalid contractions
    text = CONTRACTION_SPLIT_REGEX.sub(r"\1 \2", text)

    # Expand contractions
    text = fix(text)

    # Preserve compound words by replacing hyphens with underscores
    text = COMPOUND_WORD_REGEX.sub(lambda m: m.group().replace("-", "_"), text)

    # Remove common contractions and their remnants
    text = REMOVE_CONTRACTIONS_REGEX.sub("", text)

    # Remove any remaining apostrophes
    text = REMOVE_APOSTROPHE_REGEX.sub("", text)

    return text


def lemmatize_text(text: str, nlp: spacy.Language) -> List[str]:
    """
    Lemmatize the text using spaCy to reduce words to their base form.
    Handles compound words by replacing underscores back to hyphens.
    """
    doc = nlp(text)
    lemmatized_words = []

    for token in doc:
        # Handle compound words by replacing underscores back to hyphens
        token_text = token.text.replace("_", "-")
        lemma = token.lemma_.replace("_", "-").lower()
        if (
            token_text.strip()
            and not NUMBER_FILTER_REGEX.match(token_text)
            and not token.is_punct
            and not token.is_space
        ):
            lemmatized_words.append(lemma)

    return lemmatized_words


def count_word_families(text: str, nlp: spacy.Language) -> Tuple[int, Dict[str, int]]:
    """
    Count word families in the text.
    Returns the total number of words and a dictionary of word family counts.
    """
    preprocessed_text = preprocess_text(text)
    lemmatized_words = lemmatize_text(preprocessed_text, nlp)

    logging.debug("Lemmatized words: %s", lemmatized_words)

    # Filter out numbers and number-like strings
    filtered_words = [
        word for word in lemmatized_words if not NUMBER_FILTER_REGEX.match(word)
    ]

    total_words = len(filtered_words)
    word_family_counts = Counter(filtered_words)

    return total_words, word_family_counts


def process_file(file_path: str) -> str:
    """
    Process the file based on its extension using appropriate converter.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            logging.info("Reading text file '%s'.", file_path)
            return file.read()
    except Exception as e:
        logging.error("Error reading file '%s': %s", file_path, e)
        raise


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Calculate the frequency of word families in a text file."
    )
    parser.add_argument("file_path", help="Path to the text file")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Increase output verbosity for debugging purposes.",
    )
    parser.add_argument(
        "--language",
        default="en_core_web_sm",
        help="spaCy model to use for processing (default: en_core_web_sm)",
    )
    return parser.parse_args()


def main() -> None:
    """Main function to execute the word family counter."""
    args = parse_arguments()
    setup_logging(args.verbose)

    try:
        text = process_file(args.file_path)
    except Exception as e:  # pylint: disable=W0718
        logging.error("Failed to process the file: %s", e)
        return

    try:
        nlp = load_spacy_pipeline(args.language)
    except Exception as e:  # pylint: disable=W0718
        logging.error("Failed to initialize spaCy pipeline: %s", e)
        return

    try:
        total_words, word_family_counts = count_word_families(text, nlp)
    except Exception as e:  # pylint: disable=W0718
        logging.error("Error during word family counting: %s", e)
        return

    logging.info("Word family frequencies in '%s':", args.file_path)
    logging.info("Total words: %d", total_words)
    logging.info("Total unique word families: %d", len(word_family_counts))

    # Sort word families by count (descending) and then alphabetically
    sorted_word_families = sorted(
        word_family_counts.items(), key=lambda x: (-x[1], x[0])
    )

    for word, count in sorted_word_families:
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
