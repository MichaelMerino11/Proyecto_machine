import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:8000" });

export interface Recommendation {
  paper_id: number;
  title: string;
  authors: string;
  year: number;
  doi: string;
  score: number;
  keywords: string;
  abstract: string;
}

export interface Paper {
  paper_id: number;
  title: string;
  authors: string;
  year: number;
  doi: string;
  score: number;
  keywords: string;
  abstract: string;
  session?: string;
  recommendations: Recommendation[];
}

export interface SearchResult {
  results: Paper[];
  elapsed_seconds: number;
  method: string;
}

export const searchClassic    = (q: string) => api.get<SearchResult>("/search/classic",    { params: { q } });
export const searchEmbeddings = (q: string) => api.get<SearchResult>("/search/embeddings", { params: { q } });
export const getStats         = ()          => api.get("/stats");
