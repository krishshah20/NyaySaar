from .retriever import get_relevant_chunks
from .generator import generate_answer

def process_user_query(user_query, persona_type="common"):
    """
    Main pipeline:
    - Finds relevant chunks
    - Generates answer using those chunks
    """
    # Step 1: Get relevant chunks from vector database
    relevant_chunks = get_relevant_chunks(user_query)

    # Step 2: If nothing found, return early
    if not relevant_chunks:
        return {
            "answer": "No relevant information found in the document.",
            "chunks_used": []
        }

    # Step 3: Generate answer using LLM
    final_answer = generate_answer(user_query, relevant_chunks, persona_type)

    # Step 4: Return result
    return {
        "answer": final_answer,
        "chunks_used": relevant_chunks
    }