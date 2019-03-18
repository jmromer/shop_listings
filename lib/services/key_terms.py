"""
Given a corpus of Etsy shop listing data, determine the most meaningful terms
across the corpus.
"""

from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer

STOP_WORDS: List[str] = [
    'about', 'all', 'also', 'and', 'any', 'are', 'but', 'can', 'com', 'etc',
    'etsy', 'for', 'here', 'http', 'https', 'more', 'not', 'other', 'our',
    'out', 'quot', 'read', 'see', 'that', 'the', 'these', 'this', 'will',
    'with', 'www', 'you', 'your'
]


def compute_key_terms(corpus: list, number: int = 5) -> tuple:
    """
    Determine the NUMBER (default: 5) most meaningful terms from the provided
    list CORPUS using a TF-IDF vectorizer.
    """
    if not corpus:
        return tuple()

    vectorizer = TfidfVectorizer(
        analyzer='word',
        ngram_range=(1, 1),
        min_df=0.1,
        token_pattern=r'\b[a-z]{3,}\b',
        max_features=number,
        strip_accents='ascii',
        lowercase=True,
        stop_words=STOP_WORDS)

    vectorizer.fit_transform(corpus)

    return tuple(vectorizer.get_feature_names())
