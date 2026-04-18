from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION = os.getenv("QDRANT_COLLECTION", "allright_brain")


def ask(question: str) -> str:
    client = QdrantClient(url=QDRANT_URL)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    query_vector = embeddings.embed_query(question)
    results = client.search(
        collection_name=COLLECTION,
        query_vector=query_vector,
        limit=3
    )

    context = "\n\n".join([
        f"{r.payload['title']}: {r.payload['text']}"
        for r in results
    ])
    sources = list(set([r.payload['source'] for r in results]))

    prompt = f"""Ти — All Right Brain, внутрішній AI-асистент компанії All Right.

Правила:
1. Відповідай ТІЛЬКИ на основі наданих фрагментів документів.
2. Завжди вказуй джерело, звідки взяв інформацію: назву документа і дату оновлення.
3. Якщо інформації недостатньо — чесно скажи: "Я не знайшов точної відповіді в базі знань. Спробуй запитати колегу або перевір документацію вручну".
4. Не вигадуй факти, процеси або правила, яких немає в контексті.
5. Відповідай українською, якщо питання українською; англійською, якщо англійською.

Контекст:
{context}

Питання: {question}"""

    llm = ChatOpenAI(model="gpt-4o")
    response = llm.invoke(prompt)

    return f"{response.content}\n\nДжерела: {', '.join(sources)}"


if __name__ == "__main__":
    print(ask("Як оформити відпустку?"))