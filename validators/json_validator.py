import json
# Import Python's JSON library.
# json.loads() will convert the AI's JSON text into a Python dictionary.


def validate_json_schema(response, expected_fields):
    # Remove Markdown code fences if the AI wrapped the JSON in them.
    response = response.replace("```json", "").replace("```", "").strip()

    # Convert the cleaned AI response from JSON text into a Python object.
    data = json.loads(response)

    # Check that the AI returned a JSON object (dictionary).
    assert isinstance(data, dict), \
        "AI response is not a JSON object"

    # Check that every required field exists in the response.
    for field in expected_fields:
        assert field in data, \
            f"Missing required field: {field}"

    # Return the parsed JSON data so the test can use it.
    return data