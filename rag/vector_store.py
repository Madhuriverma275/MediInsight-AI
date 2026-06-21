import faiss
import numpy as np

class MedicalVectorStore:

    def __init__(self):

        self.index = faiss.IndexFlatL2(384)

        self.documents = []

    def build(self, embeddings, docs):

        self.documents = docs

        self.index.add(
            np.array(
                embeddings
            ).astype("float32")
        )

    def search(self, query_embedding, k=3):

        D, I = self.index.search(
            np.array([query_embedding]).astype("float32"),
            k
        )

        return [
            self.documents[i]
            for i in I[0]
        ]