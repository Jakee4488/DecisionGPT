import json
import os
from dataclasses import dataclass
from typing import List, Dict, Any

import numpy as np
from sklearn.neighbors import NearestNeighbors


VECTORS_DIR = os.path.join(os.getcwd(), "storage", "vectors")
INDEX_FILE = os.path.join(VECTORS_DIR, "index.npy")
META_FILE = os.path.join(VECTORS_DIR, "metadatas.json")


@dataclass
class Retrieval:
    text: str
    score: float
    metadata: Dict[str, Any]


class VectorStore:
    def __init__(self) -> None:
        os.makedirs(VECTORS_DIR, exist_ok=True)
        self._embeddings: np.ndarray = np.empty((0, 1), dtype=np.float32)
        self._metadatas: List[Dict[str, Any]] = []
        self._nn: NearestNeighbors | None = None
        self._loaded: bool = False

    def _rebuild_nn(self) -> None:
        if self._embeddings.size == 0:
            self._nn = None
            return
        self._nn = NearestNeighbors(metric="cosine")
        self._nn.fit(self._embeddings)

    def load(self) -> None:
        if os.path.exists(INDEX_FILE) and os.path.exists(META_FILE):
            self._embeddings = np.load(INDEX_FILE)
            with open(META_FILE, "r", encoding="utf-8") as f:
                self._metadatas = json.load(f)
        else:
            self._embeddings = np.empty((0, 1), dtype=np.float32)
            self._metadatas = []
        self._rebuild_nn()
        self._loaded = True

    def save(self) -> None:
        if self._embeddings.size == 0:
            np.save(INDEX_FILE, self._embeddings)
            with open(META_FILE, "w", encoding="utf-8") as f:
                json.dump(self._metadatas, f)
            return
        np.save(INDEX_FILE, self._embeddings)
        with open(META_FILE, "w", encoding="utf-8") as f:
            json.dump(self._metadatas, f, ensure_ascii=False, indent=2)

    def add(self, embeddings: np.ndarray, metadatas: List[Dict[str, Any]]) -> None:
        if embeddings.shape[0] != len(metadatas):
            raise ValueError("Embeddings and metadatas length mismatch")
        if self._embeddings.size == 0:
            self._embeddings = embeddings.astype(np.float32)
        else:
            self._embeddings = np.vstack([self._embeddings, embeddings.astype(np.float32)])
        self._metadatas.extend(metadatas)
        self._rebuild_nn()
        self.save()

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.load()

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Retrieval]:
        self._ensure_loaded()
        if self._embeddings.size == 0:
            return []
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        assert self._nn is not None
        distances, indices = self._nn.kneighbors(query_embedding, n_neighbors=min(k, len(self._metadatas)))
        results: List[Retrieval] = []
        for dist, idx in zip(distances[0], indices[0]):
            meta = self._metadatas[int(idx)]
            results.append(
                Retrieval(
                    text=meta.get("text", ""),
                    score=float(1.0 - dist),
                    metadata={k: v for k, v in meta.items() if k != "text"},
                )
            )
        return results

    def list_documents(self) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        docs: Dict[str, Dict[str, Any]] = {}
        for meta in self._metadatas:
            doc_id = meta.get("document_id")
            if not doc_id:
                continue
            if doc_id not in docs:
                docs[doc_id] = {"document_id": doc_id, "chunks": 0, "filename": meta.get("filename")}
            docs[doc_id]["chunks"] += 1
        return sorted(docs.values(), key=lambda d: d["document_id"])  # type: ignore[index]



