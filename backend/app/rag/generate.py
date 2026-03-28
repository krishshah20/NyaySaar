from groq import Groq
import os


# Initialize Groq client using API key from .env
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(user_query, relevant_chunks, persona_type="common"):
    """
    Generates answer using retrieved chunks and LLM
    """
    # ✅ ADD IT HERE (first thing inside function)
    if not relevant_chunks:
        return "No relevant information found in the document."

    # Combine all retrieved chunks into one context block
    combined_context = "\n\n".join(relevant_chunks)

    # Build prompt with strict instructions
    final_prompt = f"""
You are a legal assistant.

Explain the answer for a {persona_type}.

STRICT RULES:
- Use ONLY the context below
- Do NOT add extra information
- If answer not found, say "Not found in document"

Context:
{combined_context}

Question:
{user_query}
"""

    # Call Groq LLM
    llm_response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": final_prompt}],
        temperature=0
    )

    # Extract final answer text
    generated_answer = llm_response.choices[0].message.content

    return generated_answer