from sentence_transformers import SentenceTransformer
# Import the embedding model library.

model = SentenceTransformer("all-MiniLM-L6-v2")
# Load a pretrained model that converts text into embeddings.
# We will reuse this model for our AI response evaluations.

def calculate_similarity(reference_answer, actual_answer):
    # Convert both answers into embedding vectors.
    reference_embedding = model.encode(reference_answer)
    actual_embedding = model.encode(actual_answer)

    # Calculate how similar the two meanings are.
    # model.similarity() is the method
    similarity = model.similarity(
        reference_embedding,
        actual_embedding
    )

    return similarity.item()
    # model.similarity() returns something like tensor([[0.87]])
    # .item() extracts the number 0.87 from it.

def validate_similarity(reference_answer, actual_answer, threshold):
    # Compare the reference answer with the actual AI answer.
    similarity = calculate_similarity(reference_answer, actual_answer)

    # Check whether the similarity score meets our required threshold.
    assert similarity >= threshold, \
        f"Similarity score {similarity} is below threshold {threshold}"

    # Return the score so the test can print or use it if needed.
    return similarity