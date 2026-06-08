#!/bin/bash
cd "$(dirname "$0")/backend"
echo "=== UPScholar Backend ==="
echo "Instalando dependencias..."
pip install -r ../requirements.txt -q
python3 -c "import nltk; nltk.download('stopwords',quiet=True); nltk.download('wordnet',quiet=True); nltk.download('omw-1.4',quiet=True)"
echo "Iniciando servidor en http://localhost:8000 ..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
