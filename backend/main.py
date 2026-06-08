from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from search_classic    import ClassicSearchEngine
from search_embeddings import EmbeddingSearchEngine

DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset", "icmla2019.csv")

engines = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=== Cargando motores de búsqueda ===")
    print("1/2 Motor clásico (TF-IDF + Jaccard)...")
    engines["classic"] = ClassicSearchEngine(DATASET_PATH)
    print("2/2 Motor embeddings (all-mpnet-base-v2)...")
    engines["embedding"] = EmbeddingSearchEngine(DATASET_PATH)
    print("=== Todos los motores listos ===")
    yield
    engines.clear()

app = FastAPI(title="UPScholar API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search/classic")
def search_classic(
    q: str = Query(..., min_length=2, description="Consulta de búsqueda"),
    top_k: int = Query(10, ge=1, le=20),
    top_rec: int = Query(3, ge=1, le=5),
):
    """Búsqueda con TF-IDF + similitud Jaccard (pesos 0.1/0.2/0.7)."""
    return engines["classic"].search(q, top_k=top_k, top_rec=top_rec)


@app.get("/search/embeddings")
def search_embeddings(
    q: str = Query(..., min_length=2, description="Consulta de búsqueda"),
    top_k: int = Query(10, ge=1, le=20),
    top_rec: int = Query(3, ge=1, le=5),
):
    """Búsqueda con embeddings LLM (all-mpnet-base-v2) sobre abstracts."""
    return engines["embedding"].search(q, top_k=top_k, top_rec=top_rec)


@app.get("/stats")
def stats():
    """Info del dataset cargado."""
    import pandas as pd
    df = pd.read_csv(DATASET_PATH)
    return {
        "total_papers": len(df),
        "dataset": "ICMLA 2019",
        "year": 2019,
        "classic_weights": {"title": 0.1, "keywords": 0.2, "abstract": 0.7},
        "embedding_model": "all-mpnet-base-v2",
    }


@app.get("/health")
def health():
    return {"status": "ok", "engines_loaded": list(engines.keys())}
