import re


# Keywords that may appear in suspicious documents
SUSPICIOUS_KEYWORDS = [
    "fake",
    "fraud",
    "forged",
    "forgery",
    "invalid",
    "altered",
    "tampered",
    "duplicate",
    "counterfeit",
    "unauthorized",
    "mismatch",
]


def count_digits(text):
    """Count the number of digits in the document."""
    return len(re.findall(r"\d", text))


def count_special_characters(text):
    """Count special characters."""
    return len(re.findall(r"[^a-zA-Z0-9\s]", text))


def count_suspicious_keywords(text):
    """Count suspicious keywords."""
    text_lower = text.lower()

    count = 0

    for keyword in SUSPICIOUS_KEYWORDS:
        count += text_lower.count(keyword)

    return count


def get_word_count(text):
    """Return total number of words."""
    return len(text.split())


def get_character_count(text):
    """Return total number of characters."""
    return len(text)


def extract_features(text):
    """
    Extract basic fraud-detection features
    from document text.
    """

    word_count = get_word_count(text)

    character_count = get_character_count(text)

    digit_count = count_digits(text)

    special_character_count = count_special_characters(text)

    suspicious_keyword_count = count_suspicious_keywords(text)

    features = {
        "word_count": word_count,
        "character_count": character_count,
        "digit_count": digit_count,
        "special_character_count": special_character_count,
        "suspicious_keyword_count": suspicious_keyword_count,
    }

    return features