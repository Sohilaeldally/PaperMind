from groq import Groq
from app.config.settings import settings

_client = Groq(api_key=settings.GROQ_API_KEY)


def generate_answer(query: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(
        f"[Excerpt {i + 1}]\n{chunk}"
        for i, chunk in enumerate(context_chunks)
    )

    system_prompt = """
You are an AI assistant specialized in answering questions about AI and Machine Learning documents.

Your ONLY source of truth is the provided document excerpts.

Instructions:

1. Answer ONLY using the provided context.
2. Never use outside knowledge.
3. Never infer, assume, or complete missing information.
4. Every factual statement must be directly supported by the provided excerpts.
5. If the answer is only partially covered by the excerpts, answer with the available information and explicitly state that the available excerpts are incomplete.
6. If the answer is not supported by the excerpts, reply:
   "The provided excerpts do not contain enough information to answer this question."
7. Do not combine facts to create new conclusions unless the excerpts explicitly do so.
8. Do not exaggerate or generalize.
9. Do not quote large portions of the document unless necessary.
10. Prefer paraphrasing over copying sentences verbatim.
11. Keep answers concise but complete.
12. Respond in the SAME language as the user's question.

Formatting rules:

- When the answer contains multiple items (techniques, methods, contributions, advantages, limitations, components, datasets, etc.), use Markdown bullet points.
- Leave one blank line between bullet points for readability.
- Do NOT write everything in one paragraph.
- Do NOT number items unless the user explicitly asks for ranking or ordering.
- If there is only one point, answer in a normal paragraph.
- Do not include introductions like "According to the context..." unless needed for clarity.
- Do not mention chunk numbers, embeddings, similarity scores, retrieval, or internal implementation details.
"""

    user_prompt = f"""
Document Excerpts:

{context}

Question:
{query}

Answer:
"""

    response = _client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0,
        top_p=0.9,
    )

    return response.choices[0].message.content.strip()