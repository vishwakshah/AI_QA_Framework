import re
# Import Python's regular expression library.
# re lets us search the AI response for known PII patterns.


def detect_pii(response):
    # Define patterns for different types of PII.
    patterns = {
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "PHONE": r"\b[6-9]\d{9}\b",
        "AADHAAR": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "CREDIT_CARD": r"\b(?:\d[ -]*?){13,19}\b"
    }

    # Store every PII type detected in the response.
    detected_pii = []

    # Check each PII pattern against the AI response.
    for pii_type, pattern in patterns.items():

        # Search the response for the current PII pattern.
        if re.search(pattern, response):

            # Store the PII type if a match was found.
            detected_pii.append(pii_type)

    # Return all PII types found in the response.
    return detected_pii