
import json
from pathlib import Path


# Collect all AI evaluation metrics in one dictionary.
def create_evaluation_result(
    similarity,
    relevance,
    faithfulness,
    hallucination,
    latency,
    tokens
):
    evaluation_result = {
        "similarity": similarity,
        "relevance": relevance,
        "faithfulness": faithfulness,
        "hallucination": hallucination,
        "latency": latency,
        "tokens": tokens
    }

    return evaluation_result


# Check whether the AI response meets all quality requirements.
def evaluate_quality(evaluation_result):
    quality_passed = (
        evaluation_result["similarity"] >= 0.60
        and evaluation_result["relevance"] == "RELEVANT"
        and evaluation_result["faithfulness"] == "FAITHFUL"
        and evaluation_result["hallucination"] == "NO_HALLUCINATION"
        and evaluation_result["latency"] <= 10
        and evaluation_result["tokens"] <= 2500
    )

    return quality_passed


# Save each evaluation to the historical results file.
def save_evaluation_result(question, evaluation_result, quality_passed):
    # Store historical results in the test_results folder.
    results_folder = Path("test_results")
    results_folder.mkdir(exist_ok=True)

    # Define the file that keeps results across test runs.
    results_file = results_folder / "evaluation_results.json"

    # Load previously saved results, or start with an empty list.
    if results_file.exists():
        with open(results_file, "r", encoding="utf-8") as file:
            results = json.load(file)
    else:
        results = []

    # Add the current test case and its evaluation outcome.
    results.append({
        "question": question,
        "evaluation": evaluation_result,
        "quality_passed": quality_passed
    })

    # Save the updated history.
    with open(results_file, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)


# Generate a consolidated report from the current test run only.
def save_evaluation_report(results):
    # Create the reports folder if it does not exist.
    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    # Define the consolidated report file.
    report_file = reports_folder / "ai_evaluation_report.json"

    # Count passed and failed test cases from the current run.
    total = len(results)
    passed = sum(
        1 for result in results
        if result["quality_passed"] is True
    )
    failed = total - passed

    # Build a report with summary information and every current result.
    report = {
        "total_test_cases": total,
        "passed": passed,
        "failed": failed,
        "overall_quality_gate": (
            "PASS" if total > 0 and failed == 0 else "FAIL"
        ),
        "results": results
    }

    # Write the consolidated report to a JSON file.
    with open(report_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)