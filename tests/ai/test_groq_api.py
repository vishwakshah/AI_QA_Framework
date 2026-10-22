import json
# Import Python's built-in JSON library so we can read our JSON test-data file.

import time
# Import Python's time library to measure elapsed time.

from api_clients.groq_api import Groq_API
# Import our Groq API client class.

from validators.response_validator import validate_ai_answer_not_empty
# Import the validator that checks whether the AI returned an answer.

from validators.similarity_validator import validate_similarity
# Import the reusable AI similarity validator.

from validators.relevance_validator import validate_relevance
# Import the reusable relevance validator.

from validators.faithfulness_validator import evaluate_faithfulness
# Import the reusable faithfulness validator.

from validators.hallucination_validator import validate_hallucination
# Import the hallucination validator so the test can check the AI response.

from validators.toxicity_validator import evaluate_toxicity
# Import the evaluator that asks the LLM judge to check toxicity.

from validators.pii_validator import detect_pii
# Import the PII detector we created.

from validators.prompt_injection_validator import evaluate_prompt_injection
# Import the prompt-injection evaluator so the test can use it.

from validators.json_validator import validate_json_schema
# Import the JSON/schema validator.

from validators.latency_validator import validate_latency
# Import the reusable latency validation function.

from validators.token_validator import validate_token_usage
# Import the reusable token usage validator.

from validators.evaluation_validator import (
    create_evaluation_result,
    evaluate_quality,
    save_evaluation_result,
    save_evaluation_report
)
# Import the functions that collect evaluation results
# and make the overall AI quality decision.


def test_groq_response():
    # Start the main AI response evaluation test.

    print("TEST STARTED")
    # Print a message so we know the test has started.

    with open("test_data/ai_test_data.json", "r") as file:
        # Open our JSON test-data file for reading.

        test_data = json.load(file)
        # Convert the JSON file into a Python dictionary.

    # Load the dataset version information.
    # Convert the dataset version JSON into a Python dictionary.
    with open("test_data/dataset_version.json", "r") as file:
        dataset_info = json.load(file)

    # Get the current dataset version.
    dataset_version = dataset_info["dataset_version"]

    golden_dataset = test_data["golden_dataset"]
    # Get the list of trusted AI evaluation cases.

    api = Groq_API()
    # Create the Groq API client once.
    # The same client can be reused for all golden test cases.

    run_results = []
    # Collect results for this run only, separate from historical results.

    failed_cases = []
    # Keep track of failed cases so all completed golden cases are evaluated.

    for test_case in golden_dataset:
        # Process each golden test case one by one.

        question = test_case["question"]
        # Get the question that we will send to the AI.

        reference_answer = test_case["reference_answer"]
        # Get the trusted reference answer used for similarity evaluation.

        threshold = test_case["threshold"]
        # Get the minimum similarity score required for this test case.

        context = test_case["context"]
        # Get the trusted context used for faithfulness and hallucination evaluation.

        print(f"\nQuestion: {question}")
        # Print the question so we know which golden case is being evaluated.

        start_time = time.perf_counter()
        # Record the time immediately before the AI request.

        response = api.ask_question(question)
        # Send the question to the AI and wait for its response.

        end_time = time.perf_counter()
        # Record the time immediately after receiving the response.

        latency = end_time - start_time
        # Calculate how long the AI request took.

        answer = response.choices[0].message.content
        # Extract the actual AI-generated answer.

        total_tokens = response.usage.total_tokens
        # Get the total tokens used by this specific API request.

        validate_ai_answer_not_empty(answer)
        # Check that the AI returned a non-empty answer.

        similarity = validate_similarity(
            reference_answer,
            answer,
            threshold
        )
        # Calculate similarity and verify that it meets the required threshold.

        print(f"Semantic Similarity: {similarity}")
        # Print the similarity score.

        relevance = validate_relevance(
            api.client,
            question,
            answer
        )
        # Ask the evaluator whether the response answers the question.

        print(f"Relevance: {relevance}")
        # Print the relevance result.

        faithfulness = evaluate_faithfulness(
            api.client,
            context,
            reference_answer,
            answer
        )
        # Check whether the response is supported by the provided context.

        print(f"Faithfulness: {faithfulness}")
        # Print the faithfulness result.

        hallucination = validate_hallucination(
            api.client,
            context,
            reference_answer,
            answer
        )
        # Check whether the response contains unsupported claims.

        print(f"Hallucination: {hallucination}")
        # Print the hallucination result.

        evaluation_result = create_evaluation_result(
            similarity,
            relevance,
            faithfulness,
            hallucination,
            latency,
            total_tokens
        )
        # Combine all collected metrics into one evaluation result.

        # Add the dataset version used for this evaluation.
        evaluation_result["dataset_version"] = dataset_version

        print(f"Question: {question}")
        # Print which golden-dataset question is being evaluated.

        print(f"AI Answer: {answer}")
        # Print the actual answer generated by the AI.

        print(f"Evaluation Result: {evaluation_result}")
        # Print the complete evaluation result.

        quality_passed = evaluate_quality(evaluation_result)
        # Apply the overall quality rules to the evaluation result.

        # Build a record for this run's consolidated report.
        current_result = {
            "question": question,
            "evaluation": evaluation_result,
            "quality_passed": quality_passed
        }

        # Collect the record in memory for the current run's report.
        run_results.append(current_result)

        # Save this evaluation so we can compare it with future test runs.
        save_evaluation_result(
            question,
            evaluation_result,
            quality_passed
        )

        if quality_passed:
            # Handle a case that passes all configured quality gates.
            print("Overall AI Quality: PASS")
            # Print the final evaluation decision for this golden test case.

        else:
            # Record failures without stopping the remaining golden cases.
            failed_cases.append(current_result)

            print("Overall AI Quality: FAIL")
            # Print the final evaluation decision for this golden test case.

    # Write the consolidated report once after processing all golden cases.
    # Pass only this run's results, not the accumulated historical results.
    save_evaluation_report(run_results)

    # Fail the pytest test after the report has been saved.
    # This lets us inspect every completed case, including failed cases.
    assert not failed_cases, (
        f"AI quality evaluation failed for {len(failed_cases)} case(s): "
        f"{failed_cases}"
    )


def test_toxicity():
    # Start the toxicity test.

    with open("test_data/ai_test_data.json", "r") as file:
        # open() opens our JSON test-data file.
        # "r" means we are opening the file for reading.

        test_data = json.load(file)
        # json.load() reads the JSON file and converts it into a Python dictionary.

    toxicity_cases = test_data["safety_testing"]
    # Get all toxicity test cases from the JSON data.

    for case in toxicity_cases:
        # Run the following steps for each toxicity test case.

        prompt = case["prompt"]
        # Get the prompt for the current test case.

        expected = case["expected"]
        # Get the expected toxicity result for the current test case.

        api = Groq_API()
        # Create an object of our Groq API client.

        response = api.ask_question(prompt)
        # Send the current test prompt to the AI.

        answer = response.choices[0].message.content
        # Extract the actual text generated by the AI.

        result = evaluate_toxicity(api.client, answer)
        # Ask the LLM judge to evaluate the AI response for toxicity.

        assert result == expected, \
            f"Expected {expected}, but got {result}"
        # Compare the judge's result with the expected result from our JSON.

        print(f"Prompt: {prompt}")
        # Print the current test prompt.

        print(f"Toxicity result: {result}")
        # Print the toxicity evaluation result.


def test_pii_detection():
    # Start the PII detection test.

    with open("test_data/ai_test_data.json", "r") as file:
        # Open our JSON test-data file for reading.

        test_data = json.load(file)
        # Convert the JSON data into a Python dictionary.

    pii_cases = test_data["pii_testing"]
    # Get all PII test cases from our JSON file.

    for case in pii_cases:
        # Run the same test logic for every PII test case.

        response = case["response"]
        # Get the sample AI response.

        expected_pii = case["expected_pii"]
        # Get the PII types we expect to find.

        detected_pii = detect_pii(response)
        # Check the response for all supported PII patterns.

        assert detected_pii == expected_pii, \
            f"Expected {expected_pii}, but detected {detected_pii}"
        # Compare what we detected with what we expected.

        print(f"Response: {response}")
        print(f"Detected PII: {detected_pii}")


def test_ai_response_pii():
    # Start the PII leakage test for an actual AI response.

    api = Groq_API()
    # Create the Groq API client.

    prompt = "Explain API testing in simple language."
    # Ask the AI a normal question that should not require personal information.

    response = api.ask_question(prompt)
    # Send the prompt to the AI and get its response.

    answer = response.choices[0].message.content
    # Extract the actual text generated by the AI.

    detected_pii = detect_pii(answer)
    # Check the AI response for supported PII patterns.

    assert detected_pii == [], \
        f"PII leakage detected: {detected_pii}"
    # The expected result is no PII in this response.

    print(f"AI Response: {answer}")
    print(f"Detected PII: {detected_pii}")


def test_prompt_injection():
    # Start the prompt-injection test.

    with open("test_data/ai_test_data.json", "r") as file:
        # Open the JSON test-data file.

        test_data = json.load(file)
        # Convert JSON into a Python dictionary.

    cases = test_data["prompt_injection_testing"]
    # Get the prompt-injection test cases.

    for case in cases:
        # Run each prompt-injection case.

        prompt = case["prompt"]
        # Get the malicious test prompt.

        expected = case["expected"]
        # Get the expected safety result.

        api = Groq_API()
        # Create the Groq API client.

        response = api.ask_question(prompt)
        # Send the prompt to the AI.

        answer = response.choices[0].message.content
        # Extract the AI's response.

        result = evaluate_prompt_injection(api.client, answer)
        # Ask the evaluator whether the response handled the injection safely.

        assert result == expected, \
            f"Expected {expected}, but got {result}"
        # Compare the evaluator's result with our expected result.

        print(f"Prompt Injection result: {result}")


def test_ai_json_schema():
    # Start the AI JSON/schema validation test.

    with open("test_data/ai_test_data.json", "r") as file:
        # Open our JSON test-data file.

        test_data = json.load(file)
        # Convert the test-data JSON into a Python dictionary.

    test_case = test_data["json_schema_testing"]
    # Get the JSON/schema test configuration.

    prompt = test_case["prompt"]
    # Get the prompt that asks the AI to return JSON.

    expected_fields = test_case["expected_fields"]
    # Get the fields that must exist in the AI response.

    api = Groq_API()
    # Create the Groq API client.

    response = api.ask_question(prompt)
    # Send the JSON request to the AI.

    answer = response.choices[0].message.content
    # Extract the AI-generated response.

    print(f"AI Response: {answer}")

    data = validate_json_schema(answer, expected_fields)
    # Validate that the response is valid JSON
    # and contains all required fields.

    print(f"Validated JSON: {data}")
    # Print the parsed JSON after successful validation.


def test_ai_latency():
    # Start the AI latency test.

    with open("test_data/ai_test_data.json", "r") as file:
        # Open the JSON test-data file.

        test_data = json.load(file)
        # Convert JSON into a Python dictionary.

    test_case = test_data["latency_testing"]
    # Get the latency test configuration.

    prompt = test_case["prompt"]
    # Get the prompt to send to the AI.

    max_latency = test_case["max_latency_seconds"]
    # Get the maximum allowed response time.

    api = Groq_API()
    # Create the Groq API client.

    start_time = time.perf_counter()
    # Record the time immediately before the API call.

    response = api.ask_question(prompt)
    # Send the request and wait for the AI response.

    end_time = time.perf_counter()
    # Record the time immediately after the response is received.

    latency = end_time - start_time
    # Calculate how long the API call took.

    validate_latency(latency, max_latency)
    # Reuse our latency validator to check whether the response was fast enough.

    print(f"AI Latency: {latency:.2f} seconds")
    # Print the measured latency.


def test_ai_token_usage():
    # Start the AI token usage test.

    with open("test_data/ai_test_data.json", "r") as file:
        # Open the JSON test-data file.

        test_data = json.load(file)
        # Convert the JSON file into a Python dictionary.

    test_case = test_data["token_testing"]
    # Get the token testing configuration.

    prompt = test_case["prompt"]
    # Get the prompt we will send to the AI.

    max_tokens = test_case["max_total_tokens"]
    # Get the maximum total tokens allowed by our test requirement.

    api = Groq_API()
    # Create the Groq API client.

    response = api.ask_question(prompt)
    # Send the request and receive the AI response.

    total_tokens = response.usage.total_tokens
    # Read the total number of tokens used by this API request.

    print(f"Total Tokens: {total_tokens}")
    # Print the actual token usage.

    validate_token_usage(total_tokens, max_tokens)
    # Validate that token usage is within our allowed limit.

    print(f"Prompt Tokens: {response.usage.prompt_tokens}")
    # Shows how many tokens were used for our input/prompt.

    print(f"Completion Tokens: {response.usage.completion_tokens}")
    # Shows how many tokens were used to generate the AI's answer.

    print(f"Total Tokens: {response.usage.total_tokens}")
    # Shows prompt tokens + completion tokens.