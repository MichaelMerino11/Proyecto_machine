import time
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from pathlib import Path
import hashlib

MODEL_NAME  = "all-mpnet-base-v2"
CACHE_DIR   = Path(__file__).parent / "dataset" / ".cache"


def _cache_path(csv_path: str) -> Path:
    """Genera un path de caché único basado en el CSV."""
    CACHE_DIR.mkdir(exist_ok=True)
    csv_hash = hashlib.md5(Path(csv_path).read_bytes()).hexdigest()[:8]
    return CACHE_DIR / f"embeddings_{csv_hash}.npz"


class EmbeddingSearchEngine:
    def __init__(self, csv_path: str):
        t0 = time.time()
        self.df = pd.read_csv(csv_path).reset_index(drop=True)
        self.df["abstract"] = self.df["abstract"].fillna("")
        self.df["title"]    = self.df["title"].fillna("")

        abstracts  = self.df["abstract"].tolist()
        cache_file = _cache_path(csv_path)

        print(f"  Cargando modelo {MODEL_NAME}...")
        self._model = SentenceTransformer(MODEL_NAME)

        if cache_file.exists():
            print(f"  Cargando embeddings desde caché ({cache_file.name})...")
            data = np.load(cache_file)
            self._embeddings = data["embeddings"]
            print(f"  Embeddings cargados en {time.time()-t0:.1f}s")
        else:
            print(f"  Generando embeddings para {len(abstracts)} abstracts (primera vez, ~10min)...")
            emb = self._model.encode(
                abstracts,
                batch_size=64,
                show_progress_bar=True,
                normalize_embeddings=True,
            )
            self._embeddings = emb
            np.savez_compressed(cache_file, embeddings=emb)
            print(f"  Embeddings guardados en caché: {cache_file}")

        print("  Calculando matriz de similitud coseno...")
        self._M_sim = self._embeddings @ self._embeddings.T
        np.fill_diagonal(self._M_sim, 0)

        print(f"  EmbeddingSearchEngine listo en {time.time()-t0:.1f}s")

    def search(self, query: str, top_k: int = 10, top_rec: int = 3) -> dict:
        t0 = time.time()

        query_emb = self._model.encode([query], normalize_embeddings=True)[0]
        scores    = self._embeddings @ query_emb

        top_indices = np.argsort(scores)[::-1][:top_k]
        used        = set(top_indices.tolist())

        results = []
        for idx in top_indices:
            p = self.df.iloc[idx]

            rec_scores = self._M_sim[idx].copy()
            for ui in used:
                rec_scores[ui] = -1
            rec_indices = np.argsort(rec_scores)[::-1][:top_rec]

            recs = []
            for ri in rec_indices:
                r = self.df.iloc[ri]
                recs.append({
                    "paper_id": int(r["paper_id"]),
                    "title":    r["title"],
                    "authors":  str(r.get("authors", "")),
                    "year":     int(r["year"]),
                    "doi":      str(r.get("doi", "")),
                    "score":    round(float(rec_scores[ri]), 4),
                    "keywords": r["keywords"],
                    "abstract": r["abstract"][:300] + "..." if len(r["abstract"]) > 300 else r["abstract"],
                })

            results.append({
                "paper_id":        int(p["paper_id"]),
                "title":           p["title"],
                "authors":         str(p.get("authors", "")),
                "year":            int(p["year"]),
                "doi":             str(p.get("doi", "")),
                "score":           round(float(scores[idx]), 4),
                "keywords":        p["keywords"],
                "abstract":        p["abstract"],
                "recommendations": recs,
            })

        return {
            "results":         results,
            "elapsed_seconds": round(time.time() - t0, 3),
            "method":          "llm_embeddings_mpnet",
        }