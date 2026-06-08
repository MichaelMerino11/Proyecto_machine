from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import threading

from search_classic    import ClassicSearchEngine
from search_embeddings import EmbeddingSearchEngine

DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset", "icmla2019.csv")

engines = {}
loading_status = {"classic": False, "embedding": False, "error": None}

def load_engines():
    """Carga los motores en un hilo separado para no bloquear el arranque."""
    try:
        print("=== Cargando motores de búsqueda ===")
        print("1/2 Motor clásico (TF-IDF + Jaccard)...")
        engines["classic"] = ClassicSearchEngine(DATASET_PATH)
        loading_status["classic"] = True
        print("2/2 Motor embeddings (all-mpnet-base-v2)...")
        engines["embedding"] = EmbeddingSearchEngine(DATASET_PATH)
        loading_status["embedding"] = True
        print("=== Todos los motores listos ===")
    except Exception as e:
        loading_status["error"] = str(e)
        print(f"ERROR cargando motores: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Arrancar carga en hilo separado — el servidor levanta inmediatamente
    t = threading.Thread(target=load_engines, daemon=True)
    t.start()
    yield
    engines.clear()

app = FastAPI(title="UPScholar API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _require_engine(name: str):
    if name not in engines:
        raise HTTPException(
            status_code=503,
            detail=f"Motor '{name}' aún cargando. Intenta en unos segundos."
        )
    return engines[name]


@app.get("/search/classic")
def search_classic(
    q: str = Query(..., min_length=2),
    top_k: int = Query(10, ge=1, le=20),
    top_rec: int = Query(3, ge=1, le=5),
):
    return _require_engine("classic").search(q, top_k=top_k, top_rec=top_rec)


@app.get("/search/embeddings")
def search_embeddings(
    q: str = Query(..., min_length=2),
    top_k: int = Query(10, ge=1, le=20),
    top_rec: int = Query(3, ge=1, le=5),
):
    return _require_engine("embedding").search(q, top_k=top_k, top_rec=top_rec)


@app.get("/stats")
def stats():
    import pandas as pd
    df = pd.read_csv(DATASET_PATH)
    return {
        "total_papers": len(df),
        "dataset": "ICMLA 2019",
        "year": 2019,
        "classic_weights": {"title": 0.1, "keywords": 0.2, "abstract": 0.7},
        "embedding_model": "all-mpnet-base-v2",
        "engines_ready": loading_status,
    }


@app.get("/health")
def health():
    return {
        "status": "ok" if loading_status["classic"] and loading_status["embedding"] else "loading",
        "engines_loaded": list(engines.keys()),
        "loading_status": loading_status,
    }