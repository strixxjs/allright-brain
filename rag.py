from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from qdrant_client import QdrantClient


def ask(question: str) -> str:
    client = QdrantClient(url="http://localhost:6333")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    query_vector = embeddings.embed_query(question)
    results = client.search(
        collection_name="allright_brain",
        query_vector=query_vector,
        limit=3
    )

    context = "\n\n".join([
        f"{r.payload['title']}: {r.payload['text']}"
        for r in results
    ])
    sources = list(set([r.payload['source'] for r in results]))

    llm = ChatOpenAI(model="gpt-4o")
    response = llm.invoke(f"""
Відповідай тільки на основі наданого контексту.
Якщо відповіді немає — скажи про це чесно.

Контекст:
{context}

Питання: {question}
""")

    return f"{response.content}\n\nДжерела: {', '.join(sources)}"