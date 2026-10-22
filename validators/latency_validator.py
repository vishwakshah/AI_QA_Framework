def validate_latency(latency, max_latency):
    # Check whether the actual API response time is within the allowed limit.
    assert latency <= max_latency, \
        f"Latency {latency:.2f}s exceeded maximum {max_latency}s"

    # Return the latency so the test can print or use the value.
    return latency