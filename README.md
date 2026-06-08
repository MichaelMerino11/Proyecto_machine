# UPScholar — Buscador de Papers ICMLA 2019

## Estructura
```
upscholar/
├── backend/
│   ├── main.py              # FastAPI
│   ├── search_classic.py    # TF-IDF + Jaccard (pesos 0.1/0.2/0.7)
│   ├── search_embeddings.py # Embeddings LLM (all-mpnet-base-v2)
│   └── dataset/
│       └── icmla2019.csv    # 305 papers ICMLA 2019
├── frontend/                # Vue 3 + TypeScript + Vite
├── requirements.txt
└── start_backend.sh
```

## Arrancar

### Backend
```bash
./start_backend.sh
# o manualmente:
cd backend && uvicorn main:app --reload
```

### Frontend
```bash
cd frontend && npm install && npm run dev
```

## Endpoints
- GET /search/classic?q=deep+learning     → TF-IDF + Jaccard
- GET /search/embeddings?q=deep+learning  → LLM embeddings
- GET /stats                               → Info del dataset
- GET /health                              → Estado de los motores
