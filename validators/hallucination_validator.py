def evaluate_hallucination(client, context, reference_answer, response):
    # Ask the AI judge whether the response is supported by the trusted information.

    prompt = f"""
    You are evaluating an AI response for hallucination.

    Context:
    {context}

    Trusted Reference Answer:
    {reference_answer}

    AI Response:
    {response}

    Rules:
    - Return NO_HALLUCINATION if the AI response is consistent with the context
      and reference answer.
    - Return HALLUCINATION only if the AI response contains a factual claim
      that contradicts the context/reference or adds unsupported factual information.
    - Do not classify different wording, extra explanation, or rephrasing as hallucination.

    Return ONLY one of these:
    NO_HALLUCINATION
    HALLUCINATION
    """

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    # Ask the Groq model to act as our hallucination evaluator.

    result = completion.choices[0].message.content.strip()
    # Extract the evaluator's final decision.

    return result


def validate_hallucination(client, context, reference_answer, response):
    # Evaluate the response for hallucination.
    result = evaluate_hallucination(
        client,
        context,
        reference_answer,
        response
    )

    # Fail the test only when the evaluator identifies unsupported information.
    assert result == "NO_HALLUCINATION", \
        f"AI response contains hallucination. Judge result: {result}"

    return result