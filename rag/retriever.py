from rag.embeddings import model

def retrieve_context(
    query,
    vector_store
):

    query_embedding = model.encode(query)

    results = vector_store.search(
        query_embedding
    )

    return "\n".join(results)