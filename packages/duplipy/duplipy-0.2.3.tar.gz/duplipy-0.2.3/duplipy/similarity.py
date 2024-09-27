"""
Text similarity testing.

Available functions:
- `edit_distance_score(text1, text2)`: Calculate the edit distance score between two texts.
- `bleu_score(reference, candidate)`: Calculate the BLEU score between a reference sentence and a candidate sentence.
- `jaccard_similarity_score(text1, text2)`: Calculate Jaccard similarity between two texts.
"""

import nltk
from nltk.metrics import distance
from nltk.translate.bleu_score import sentence_bleu

def edit_distance_score(text1, text2):
    """
    Calculate the edit distance score between two texts.

    The edit distance, also known as Levenshtein distance, is a measure of the
    minimum number of single-character edits (insertions, deletions, or
    substitutions) required to transform one text into another.

    Parameters:
    - `text1` (str): The first text.
    - `text2` (str): The second text.

    Returns:
    - `int`: The edit distance score between the two texts. A lower score
      indicates greater similarity, with 0 meaning the texts are identical.
    """
    try:
        # Calculate the edit distance
        edit_dist = distance.edit_distance(text1, text2)
        return edit_dist
    except Exception as e:
        print(f"An error occurred during edit distance calculation: {str(e)}")
        return 0
    
def bleu_score(reference, candidate):
    """
    Calculate the BLEU (Bilingual Evaluation Understudy) score between a reference sentence and a candidate sentence.

    BLEU is a metric commonly used for evaluating the quality of machine-translated text. It measures the precision of the
    candidate sentence's n-grams (contiguous sequences of n items) against the reference sentence.

    Parameters:
    - `reference` (str): The reference sentence.
    - `candidate` (str): The candidate sentence.

    Returns:
    - `float`: The BLEU score. The score ranges from 0 (no similarity) to 1 (perfect match).
    """
    try:
        # Tokenize the reference and candidate sentences
        reference_tokens = nltk.word_tokenize(reference)
        candidate_tokens = nltk.word_tokenize(candidate)

        # Calculate the BLEU score
        bleu = sentence_bleu([reference_tokens], candidate_tokens)
        return bleu
    except Exception as e:
        print(f"An error occurred during BLEU score calculation: {str(e)}")
        return 0.0
    
# DupliPy 0.2.0

def jaccard_similarity_score(text1, text2):
    """
    Calculate Jaccard similarity between two texts.

    Jaccard similarity is a measure of similarity between two sets. In the context
    of text comparison, it calculates the similarity between the sets of words
    in two texts.

    Parameters:
    - `text1` (str): The first text for comparison.
    - `text2` (str): The second text for comparison.

    Returns:
    - `float`: Jaccard similarity score between the two texts. The score ranges
      from 0 (no similarity) to 1 (complete similarity).
    """
    set1 = set(text1.split())
    set2 = set(text2.split())
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity_score = intersection / union if union != 0 else 0
    return similarity_score