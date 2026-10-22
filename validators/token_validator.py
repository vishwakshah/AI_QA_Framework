def validate_token_usage(total_tokens, max_tokens):
    # Check whether the AI used tokens within our allowed limit.
    assert total_tokens <= max_tokens, \
        f"Token usage {total_tokens} exceeded maximum {max_tokens}"

    # Return the token count so the test can print or use it.
    return total_tokens