import re
import time
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

STOP_WORDS  = set(stopwords.words("english"))
stemmer     = PorterStemmer()
lemmatizer  = WordNetLemmatizer()

W_TITLE    = 0.1
W_KEYWORDS = 0.2
W_ABSTRACT = 0.7


def _clean_tokens(text: str) -> list:
    text   = re.sub(r"[^a-zA-Z0-9]+", " ", str(text)).lower().strip()
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 1]
    tokens = [stemmer.stem(t) for t in tokens]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return tokens


def _jaccard(s1: set, s2: set) -> float:
    u = len(s1 | s2)
    return len(s1 & s2) / u if u else 0.0


class ClassicSearchEngine:
    def __init__(self, csv_path: str):
        t0 = time.time()
        self.df = pd.read_csv(csv_path).reset_index(drop=True)
        self.df["keywords"] = self.df["keywords"].fillna("")
        self.df["abstract"] = self.df["abstract"].fillna("")
        self.df["title"]    = self.df["title"].fillna("")
        n = len(self.df)

        titles    = self.df["title"].tolist()
        keywords  = self.df["keywords"].tolist()
        abstracts = self.df["abstract"].tolist()

        # ── Jaccard sets ────────────────────────────────────────────────────
        self._title_sets   = [set(_clean_tokens(t)) for t in titles]
        self._keyword_sets = [set(_clean_tokens(k)) for k in keywords]

        # ── TF-IDF manual (igual Deber 5) ───────────────────────────────────
        tokenized = [_clean_tokens(a) for a in abstracts]

        vocab, seen = [], set()
        for toks in tokenized:
            for t in toks:
                if t not in seen:
                    vocab.append(t); seen.add(t)

        self._vocab_idx = {w: i for i, w in enumerate(vocab)}
        n_vocab = len(vocab)

        tf = np.zeros((n, n_vocab))
        for i, toks in enumerate(tokenized):
            for t in toks:
                if t in self._vocab_idx:
                    tf[i, self._vocab_idx[t]] += 1

        wtf = np.where(tf > 0, 1 + np.log10(tf + 1e-10), 0)
        df_cnt = np.count_nonzero(tf, axis=0)
        df_cnt = np.where(df_cnt == 0, 1, df_cnt)
        self._idf = np.log10(n / df_cnt)

        tfidf = wtf * self._idf
        norms = np.linalg.norm(tfidf, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        self._abstract_norm = tfidf / norms   # (n, vocab)

        # ── Matrices de similitud pre-calculadas ────────────────────────────
        print(f"  Jaccard títulos...")
        M_title = self._jaccard_matrix(self._title_sets)

        print(f"  Jaccard keywords...")
        M_kw = self._jaccard_matrix(self._keyword_sets)

        print(f"  Coseno abstracts...")
        M_abs = self._abstract_norm @ self._abstract_norm.T
        np.fill_diagonal(M_abs, 0)

        self._M_final = W_TITLE * M_title + W_KEYWORDS * M_kw + W_ABSTRACT * M_abs
        print(f"  ClassicSearchEngine listo en {time.time()-t0:.1f}s — {n} papers")

    def _jaccard_matrix(self, sets):
        n = len(sets)
        M = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                v = _jaccard(sets[i], sets[j])
                M[i, j] = v; M[j, i] = v
        return M

    def _query_vec(self, tokens: list) -> np.ndarray:
        tf = np.zeros(len(self._vocab_idx))
        for t in tokens:
            if t in self._vocab_idx:
                tf[self._vocab_idx[t]] += 1
        wtf  = np.where(tf > 0, 1 + np.log10(tf + 1e-10), 0) * self._idf
        norm = np.linalg.norm(wtf)
        return wtf / norm if norm else wtf

    def search(self, query: str, top_k: int = 10, top_rec: int = 3) -> dict:
        t0           = time.time()
        tokens       = _clean_tokens(query)
        query_set    = set(tokens)

        jac_title = np.array([_jaccard(query_set, s) for s in self._title_sets])
        jac_kw    = np.array([_jaccard(query_set, s) for s in self._keyword_sets])
        cos_abs   = self._abstract_norm @ self._query_vec(tokens)

        scores      = W_TITLE * jac_title + W_KEYWORDS * jac_kw + W_ABSTRACT * cos_abs
        top_indices = np.argsort(scores)[::-1][:top_k]
        used        = set(top_indices.tolist())

        results = []
        for idx in top_indices:
            p = self.df.iloc[idx]

            rec_scores = self._M_final[idx].copy()
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
            "method":          "classic_tfidf_jaccard",
        }
