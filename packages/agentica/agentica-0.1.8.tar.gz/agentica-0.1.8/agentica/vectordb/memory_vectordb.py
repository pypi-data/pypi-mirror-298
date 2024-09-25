# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""

from hashlib import md5
from typing import List

import numpy as np

from agentica.document import Document
from agentica.emb.base import Emb
from agentica.emb.openai_emb import OpenAIEmb
from agentica.vectordb.base import VectorDb, Distance


class MemoryVectorDb(VectorDb):
    def __init__(
            self,
            embedder: Emb = OpenAIEmb(),
            distance: Distance = Distance.cosine,
    ):
        self.embedder = embedder
        self.distance = distance
        self.documents = []

    def create(self) -> None:
        """Create an in-memory storage."""
        self.documents = []

    def doc_exists(self, document: Document) -> bool:
        doc_id = self._generate_doc_id(document.content)
        return any(doc for doc in self.documents if self._generate_doc_id(doc.content) == doc_id)

    def name_exists(self, name: str) -> bool:
        return any(doc for doc in self.documents if doc.name == name)

    def insert(self, documents: List[Document]) -> None:
        """Insert documents into the in-memory storage."""
        for document in documents:
            document.embed(self.embedder)
            if not self.doc_exists(document):
                self.documents.append(document)

    def upsert(self, documents: List[Document]) -> None:
        """Upsert documents into the in-memory storage."""
        for document in documents:
            existing_doc_idx = self._get_doc_idx(document)
            if existing_doc_idx is not None:
                self.documents[existing_doc_idx] = document
            else:
                document.embed(self.embedder)
                self.documents.append(document)

    def search(self, query: str, limit: int = 5) -> List[Document]:
        """Search for documents that are most similar to the query."""
        query_embedding = self.embedder.get_embedding(query)
        if query_embedding is None:
            return []
        try:
            from sklearn.metrics.pairwise import cosine_similarity
        except ImportError:
            raise ImportError(
                "The 'scikit-learn' library is required, please install it via 'pip install scikit-learn'."
            )
        similarities = cosine_similarity(
            [query_embedding], [doc.embedding for doc in self.documents]
        )[0]

        # Get the indices of the documents with the highest similarity scores
        sorted_indices = np.argsort(similarities)[::-1][:limit]
        return [self.documents[idx] for idx in sorted_indices]

    def delete(self) -> None:
        """Delete all documents in the in-memory storage."""
        self.create()

    def exists(self) -> bool:
        """Check if the in-memory storage is initialized."""
        return hasattr(self, 'documents')

    def optimize(self) -> None:
        """No optimization needed for in-memory storage."""
        pass

    def clear(self) -> bool:
        """Clear the in-memory storage."""
        self.delete()
        return True

    def _generate_doc_id(self, content: str) -> str:
        """Generate a unique ID for the document based on its content."""
        return md5(content.encode()).hexdigest()

    def _get_doc_idx(self, document: Document):
        """Get the index of a document in the document list."""
        doc_id = self._generate_doc_id(document.content)
        for idx, doc in enumerate(self.documents):
            if self._generate_doc_id(doc.content) == doc_id:
                return idx
        return None
