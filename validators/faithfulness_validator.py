def evaluate_faithfulness(client, context, reference_answer, response):
    # Ask the AI judge whether the response is factually supported.

    prompt = f"""
You are an AI quality evaluator checking factual faithfulness.

Context:
{context}

Trusted Reference Answer:
{reference_answer}

AI Response:
{response}

Evaluate the AI response using these rules:

1. Return FAITHFUL if the response is factually consistent with the
   context or reference answer.

2. Return FAITHFUL if the response contains additional general knowledge
   that does not contradict the context or reference answer.

3. Return NOT_FAITHFUL only when the response contains a factual claim
   that directly contradicts the trusted information or makes a specific
   claim that clearly cannot be supported.

4. Do NOT require the response to contain only information from the
   reference answer.

5. Different wording, examples, explanations, and additional correct
   information are NOT failures.

6. Do not judge relevance, writing style, completeness, or similarity.

Return ONLY:
FAITHFUL
or
NOT_FAITHFUL
"""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    # Ask the LLM judge to evaluate factual faithfulness.

    result = completion.choices[0].message.content.strip()
    # Extract the judge's decision.

    return result