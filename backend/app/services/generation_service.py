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

Your task is to answer the user's question using ONLY the provided document excerpts.

Instructions:
- Base every statement only on the provided context.
- Do not use your own knowledge, assumptions, or external information.
- Do not infer facts that are not explicitly supported by the context.
- If the context fully answers the question, provide a clear and direct answer.
- If the context only partially answers the question, answer using the available information and clearly state what is missing.
- If the answer cannot be found in the provided excerpts, say that the document does not contain enough information to answer the question.
- If the user asks for "all", "every", "complete", or "full" information but the retrieved context appears incomplete, explain that the available excerpts may not contain the complete answer.
- Write natural, fluent, and well-structured responses.
- Summarize the information instead of copying sentences verbatim.
- Avoid phrases such as "The context says..." or "It is mentioned that..." unless they are necessary for clarity.
- Keep the answer concise while including all relevant information from the context.
- Do not repeat the same information.
- Always respond in the same language as the user's question.
- When the user asks to list or summarize techniques, methods, advantages, limitations, or contributions,
prefer using bullet points instead of writing a narrative paragraph.
- Do not combine multiple facts into conclusions that are not explicitly stated in the context.
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