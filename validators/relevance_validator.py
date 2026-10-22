def evaluate_relevance(client, question, response):
    # Create a prompt asking the LLM judge whether the AI response answers the question.
    prompt = f"""
    Determine whether the AI response directly answers the user's question.

    User Question:
    {question}

    AI Response:
    {response}

    Return ONLY one of these:
    RELEVANT
    NOT_RELEVANT
    """

    # Send the question and AI response to the LLM judge.
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    # Extract the judge's text response and remove extra spaces.
    result = completion.choices[0].message.content.strip()

    # Return the judge's decision.
    return result


def validate_relevance(client, question, response):
    # Ask the LLM judge to evaluate whether the response is relevant.
    result = evaluate_relevance(client, question, response)

    # Fail the test if the judge says the response is not relevant.
    assert result == "RELEVANT", \
        f"AI response is not relevant. Judge result: {result}"

    # Return the result so the test can use or print it.
    return result