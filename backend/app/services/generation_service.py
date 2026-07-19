from groq import Groq
from app.config.settings import settings

_client = Groq(api_key=settings.GROQ_API_KEY)


def generate_answer(query: str, context_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(context_chunks)

    system_prompt = (
        "You are a helpful assistant that answers questions about AI/ML research papers. "
        "Answer the user's question based ONLY on the provided context. "
        "If the context doesn't contain enough information to answer, say so clearly. "
        "Be concise and accurate."
    )

    user_prompt = f"Context:\n{context}\n\nQuestion: {query}"

    response = _client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content