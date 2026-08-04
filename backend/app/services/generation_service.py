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

Your job is to answer the user's question using ONLY the provided document excerpts.

Rules:
- Never invent information that is not present in the context.
- Write natural, fluent, and well-structured answers.
- Summarize information instead of copying sentences verbatim.
- Avoid phrases like "The context says..." or "It is mentioned that..." unless absolutely necessary.
- If the context contains enough information, answer directly.
- If the context contains only partial information, answer with the available information and clearly mention what is missing.
- If the answer cannot be found in the provided excerpts, politely state that the document does not contain enough information.
- Keep the answer concise while still being complete.
- Do not repeat the same idea multiple times.
- Always respond in the same language as the user's question.
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
        temperature=0.1,
        top_p=0.9,
    )

    return response.choices[0].message.content.strip()