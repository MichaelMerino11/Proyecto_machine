<template>
  <div class="app" :class="{ 'has-results': hasSearched }">
    <div class="home-screen" v-if="!hasSearched">
      <nav class="top-nav">
        <div class="top-nav-links">
          <a href="https://www.ups.edu.ec/"
            >Universidad Politécnica Salesiana</a
          >
          <div class="avatar">
            <img src="./img/logo.png" alt="Perfil" />
          </div>
        </div>
      </nav>

      <div class="home-center">
        <div class="google-logo">
          <span class="g-blue">U</span><span class="g-red">P</span
          ><span class="g-yellow">S</span><span class="g-blue">c</span
          ><span class="g-green">h</span><span class="g-red">o</span
          ><span class="g-blue">l</span><span class="g-yellow">a</span
          ><span class="g-green">r</span>
        </div>

        <div class="home-search-wrap">
          <div class="home-search-box" :class="{ focused: inputFocused }">
            <svg class="search-icon-left" viewBox="0 0 24 24" fill="none">
              <path
                d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"
                stroke="#9aa0a6"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
            <input
              ref="homeInput"
              v-model="query"
              class="home-input"
              placeholder=""
              @focus="inputFocused = true"
              @blur="inputFocused = false"
              @keyup.enter="runSearch"
              autocomplete="off"
            />
            <button v-if="query" class="clear-btn" @click="query = ''">
              <svg viewBox="0 0 24 24" fill="#70757a" width="18" height="18">
                <path
                  d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
                />
              </svg>
            </button>
            <div class="divider-v" v-if="query"></div>
            <button class="mic-btn">
              <svg viewBox="0 0 24 24" width="20" height="20">
                <path
                  fill="#4285f4"
                  d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"
                />
                <path
                  fill="#34a853"
                  d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"
                />
              </svg>
            </button>
          </div>

          <div class="home-method-row">
            <button
              v-for="m in methods"
              :key="m.key"
              :class="['method-pill', { active: activeMethod === m.key }]"
              @click="activeMethod = m.key"
            >
              <span class="pill-dot" :class="m.color"></span>
              {{ m.label }}
            </button>
          </div>

          <div class="home-buttons">
            <button class="google-btn" :disabled="loading" @click="runSearch">
              <span v-if="loading" class="g-spinner"></span>
              <span v-else>Búsqueda UPScholar</span>
            </button>
            <button class="google-btn" @click="luckSearch">
              Me siento con suerte
            </button>
          </div>
        </div>

        <p class="home-footer-text">
          305 papers · ICMLA 2019 · Machine Learning
        </p>
      </div>

      <footer class="home-footer">
        <div class="footer-bottom">
          <div class="footer-links">
            <a href="#">Acerca de</a>
            <a href="#">Publicidad</a>
            <a href="#">Negocios</a>
            <a href="#">Cómo funciona</a>
          </div>

          <div class="footer-links footer-right">
            <a href="#">Configuración</a>
            <a href="#">Términos</a>
            <a href="#">Privacidad</a>
          </div>
        </div>
      </footer>
    </div>

    <div class="results-screen" v-else>
      <header class="results-header">
        <div class="results-header-inner">
          <div class="results-logo" @click="resetSearch">
            <span class="g-blue">U</span><span class="g-red">P</span
            ><span class="g-yellow">S</span><span class="g-blue">c</span
            ><span class="g-green">h</span><span class="g-red">o</span
            ><span class="g-blue">l</span><span class="g-yellow">a</span
            ><span class="g-green">r</span>
          </div>

          <div class="results-search-wrap">
            <div class="results-search-box" :class="{ focused: inputFocused }">
              <input
                v-model="query"
                class="results-input"
                @focus="inputFocused = true"
                @blur="inputFocused = false"
                @keyup.enter="runSearch"
                autocomplete="off"
              />
              <button v-if="query" class="clear-btn-sm" @click="query = ''">
                <svg viewBox="0 0 24 24" fill="#70757a" width="16" height="16">
                  <path
                    d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
                  />
                </svg>
              </button>
              <div class="sep-v"></div>
              <button
                class="results-search-btn"
                @click="runSearch"
                :disabled="loading"
              >
                <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
                  <path
                    d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"
                    stroke="#fff"
                    stroke-width="2.5"
                    stroke-linecap="round"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div class="results-tabs-row">
          <div class="tabs-inner">
            <button
              v-for="m in methods"
              :key="m.key"
              :class="['results-tab', { active: activeMethod === m.key }]"
              @click="
                activeMethod = m.key;
                runSearch();
              "
            >
              <span v-if="m.key === 'classic'">
                <svg
                  viewBox="0 0 24 24"
                  width="14"
                  height="14"
                  fill="currentColor"
                  style="margin-right: 4px; vertical-align: -2px"
                >
                  <path d="M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z" />
                </svg>
              </span>
              <span v-else>
                <svg
                  viewBox="0 0 24 24"
                  width="14"
                  height="14"
                  fill="currentColor"
                  style="margin-right: 4px; vertical-align: -2px"
                >
                  <circle cx="12" cy="12" r="10" />
                </svg>
              </span>
              {{ m.label }}
            </button>
          </div>
        </div>
      </header>

      <main class="results-body">
        <div class="results-content">
          <div class="results-stats" v-if="!loading">
            Aproximadamente <strong>{{ results.length }}</strong> resultados ({{
              elapsed
            }}
            segundos)
          </div>

          <div v-if="loading" class="skeleton-wrap">
            <div v-for="i in 5" :key="i" class="skeleton-result">
              <div class="sk-url"></div>
              <div class="sk-title"></div>
              <div class="sk-text"></div>
              <div class="sk-text short"></div>
            </div>
          </div>

          <div v-else class="result-list">
            <div
              v-for="paper in results"
              :key="paper.paper_id"
              class="result-item"
            >
              <div class="result-url-row">
                <div class="result-favicon">📄</div>
                <div>
                  <span class="result-source">ieeexplore.ieee.org</span>
                  <span class="result-breadcrumb">
                    › ICMLA 2019 › {{ paper.session || "Papers" }}</span
                  >
                </div>
              </div>

              <a
                class="result-title"
                :href="paper.doi ? `https://doi.org/${paper.doi}` : '#'"
                target="_blank"
                >{{ paper.title }}</a
              >

              <span class="result-score-badge"
                >{{ (paper.score * 100).toFixed(1) }}% similitud</span
              >

              <p class="result-snippet">
                <span class="snippet-meta"
                  >{{ paper.authors ? formatAuthors(paper.authors) + " · " : ""
                  }}{{ paper.year }} — </span
                >{{ paper.abstract.slice(0, 200) }}...
              </p>

              <div class="result-kws" v-if="paper.keywords">
                <span
                  v-for="kw in formatKeywords(paper.keywords)"
                  :key="kw"
                  class="kw-tag"
                  >{{ kw }}</span
                >
              </div>

              <div class="related-wrap" v-if="paper.recommendations?.length">
                <button
                  class="related-toggle"
                  @click="toggleExpand(paper.paper_id)"
                >
                  <svg
                    viewBox="0 0 24 24"
                    width="14"
                    height="14"
                    fill="#1a0dab"
                  >
                    <path
                      v-if="!expandedIds.has(paper.paper_id)"
                      d="M7 10l5 5 5-5z"
                    />
                    <path v-else d="M7 14l5-5 5 5z" />
                  </svg>
                  {{ expandedIds.has(paper.paper_id) ? "Ocultar" : "Ver" }}
                  artículos relacionados
                </button>
                <div
                  v-if="expandedIds.has(paper.paper_id)"
                  class="related-list"
                >
                  <div
                    v-for="rec in paper.recommendations"
                    :key="rec.paper_id"
                    class="related-item"
                  >
                    <a
                      :href="rec.doi ? `https://doi.org/${rec.doi}` : '#'"
                      target="_blank"
                      class="related-title"
                      >{{ rec.title }}</a
                    >
                    <span class="related-meta"
                      >{{ formatAuthors(rec.authors) }} · {{ rec.year }} ·
                      {{ (rec.score * 100).toFixed(1) }}%</span
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="pagination" v-if="results.length && !loading">
            <div class="page-logo">
              <span class="g-blue">U</span><span class="g-red">P</span
              ><span class="g-yellow">S</span><span class="g-blue">c</span
              ><span class="g-green">h</span><span class="g-red">o</span>
            </div>
            <div class="page-nums">
              <span class="page-current">1</span>
              <span class="page-num">2</span>
              <span class="page-num">3</span>
              <span class="page-num">4</span>
              <span class="page-num">5</span>
              <span class="page-next">Siguiente ›</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { searchClassic, searchEmbeddings, type Paper } from "./api";

const query = ref("");
const loading = ref(false);
const results = ref<Paper[]>([]);
const elapsed = ref(0);
const hasSearched = ref(false);
const inputFocused = ref(false);
const expandedIds = ref(new Set<number>());
const activeMethod = ref<"classic" | "embeddings">("classic");

const methods = [
  { key: "classic", label: "TF-IDF + Jaccard", color: "blue" },
  { key: "embeddings", label: "LLM Embeddings", color: "green" },
] as const;

const luckyQueries = [
  "deep learning image classification",
  "natural language processing sentiment",
  "reinforcement learning robotics",
  "anomaly detection time series",
  "neural network optimization",
];

async function runSearch() {
  if (!query.value.trim()) return;
  loading.value = true;
  hasSearched.value = true;
  expandedIds.value.clear();

  try {
    const fn =
      activeMethod.value === "classic" ? searchClassic : searchEmbeddings;
    const resp = await fn(query.value.trim());
    results.value = resp.data.results;
    elapsed.value = resp.data.elapsed_seconds;
  } catch {
    alert("Error conectando con el backend (localhost:8000)");
  } finally {
    loading.value = false;
  }
}

function luckSearch() {
  query.value = luckyQueries[Math.floor(Math.random() * luckyQueries.length)];
  runSearch();
}

function resetSearch() {
  hasSearched.value = false;
  results.value = [];
  query.value = "";
}

function toggleExpand(id: number) {
  if (expandedIds.value.has(id)) expandedIds.value.delete(id);
  else expandedIds.value.add(id);
  expandedIds.value = new Set(expandedIds.value);
}

function formatAuthors(authors: string): string {
  if (!authors) return "";
  const parts = authors
    .split(";")
    .map((a) => a.trim())
    .filter(Boolean);
  if (parts.length <= 2) return parts.join(", ");
  return `${parts[0]}, ${parts[1]} +${parts.length - 2}`;
}

function formatKeywords(kw: string): string[] {
  return kw
    .split(/[;,]/)
    .map((k) => k.trim())
    .filter((k) => k.length > 1 && k.length < 45)
    .slice(0, 6);
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&family=Roboto:wght@300;400;500&display=swap");

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.app {
  min-height: 100vh;
  font-family: "Roboto", Arial, sans-serif;
  font-size: 14px;
  color: #202124;
  background: #fff;
}

.g-blue {
  color: #4285f4;
}
.g-red {
  color: #ea4335;
}
.g-yellow {
  color: #fbbc05;
}
.g-green {
  color: #34a853;
}

.home-screen {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.top-nav {
  display: flex;
  justify-content: flex-end;
  padding: 14px 16px;
}
.top-nav-links {
  display: flex;
  align-items: center;
  gap: 16px;
}
.top-nav-links a {
  color: #202124;
  text-decoration: none;
  font-size: 13px;
}
.top-nav-links a:hover {
  text-decoration: underline;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.home-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 92px;
}

.google-logo {
  font-family: "Google Sans", "Product Sans", Arial, sans-serif;
  font-size: 74px;
  font-weight: 400;
  letter-spacing: -2px;
  margin-bottom: 28px;
  user-select: none;
}

.home-search-wrap {
  width: 100%;
  max-width: 584px;
}

.home-search-box {
  display: flex;
  align-items: center;
  border: 1px solid #dfe1e5;
  border-radius: 24px;
  padding: 8px 14px;
  background: #fff;
  transition:
    box-shadow 0.2s,
    border-color 0.2s;
  gap: 8px;
}
.home-search-box:hover,
.home-search-box.focused {
  box-shadow: 0 1px 6px rgba(32, 33, 36, 0.28);
  border-color: transparent;
}
.search-icon-left {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.home-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  color: #202124;
  background: transparent;
  caret-color: #4285f4;
}

.clear-btn,
.clear-btn-sm {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 2px;
  border-radius: 50%;
}
.clear-btn:hover,
.clear-btn-sm:hover {
  background: #f1f3f4;
}

.divider-v,
.sep-v {
  width: 1px;
  height: 24px;
  background: #dadce0;
  flex-shrink: 0;
}

.mic-btn {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 2px;
}

.home-method-row {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  justify-content: center;
}
.method-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 14px;
  border: 1px solid #dadce0;
  border-radius: 20px;
  background: #fff;
  font-size: 13px;
  color: #5f6368;
  cursor: pointer;
  transition:
    background 0.15s,
    border-color 0.15s;
}
.method-pill:hover {
  background: #f8f9fa;
}
.method-pill.active {
  border-color: #4285f4;
  color: #4285f4;
  background: #e8f0fe;
}
.pill-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.pill-dot.blue {
  background: #4285f4;
}
.pill-dot.green {
  background: #34a853;
}

.home-buttons {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  justify-content: center;
}
.google-btn {
  padding: 10px 18px;
  background: #f8f9fa;
  border: 1px solid #f8f9fa;
  border-radius: 4px;
  font-size: 14px;
  color: #3c4043;
  cursor: pointer;
  transition:
    border-color 0.1s,
    box-shadow 0.1s;
  min-width: 130px;
  font-family: inherit;
}
.google-btn:hover:not(:disabled) {
  border-color: #dadce0;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
  background: #f8f9fa;
}
.google-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.home-footer-text {
  margin-top: 32px;
  font-size: 12px;
  color: #70757a;
}

.home-footer {
  background: #f2f2f2;
  border-top: 1px solid #dadce0;
  font-size: 14px;
  color: #70757a;
}

.footer-top {
  padding: 15px 30px;
  border-bottom: 1px solid #dadce0;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  flex-wrap: wrap;
}

.footer-links {
  display: flex;
  gap: 24px;
}

.footer-links a {
  color: #70757a;
  text-decoration: none;
}

.footer-links a:hover {
  text-decoration: underline;
}

.g-spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid #dadce0;
  border-top-color: #4285f4;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.results-screen {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.results-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  border-bottom: 1px solid #ebebeb;
}
.results-header-inner {
  display: flex;
  align-items: center;
  padding: 12px 24px;
  gap: 20px;
}

.results-logo {
  font-family: "Google Sans", "Product Sans", Arial, sans-serif;
  font-size: 26px;
  font-weight: 400;
  letter-spacing: -0.5px;
  cursor: pointer;
  flex-shrink: 0;
  user-select: none;
}

.results-search-wrap {
  flex: 1;
  max-width: 640px;
}
.results-search-box {
  display: flex;
  align-items: center;
  border: 1px solid #dfe1e5;
  border-radius: 24px;
  padding: 6px 8px 6px 16px;
  gap: 6px;
  transition:
    box-shadow 0.2s,
    border-color 0.2s;
}
.results-search-box:hover,
.results-search-box.focused {
  box-shadow: 0 1px 6px rgba(32, 33, 36, 0.28);
  border-color: transparent;
}
.results-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  color: #202124;
  background: transparent;
  caret-color: #4285f4;
}
.results-search-btn {
  width: 36px;
  height: 36px;
  background: #4285f4;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.15s;
}
.results-search-btn:hover:not(:disabled) {
  background: #1a73e8;
}
.results-search-btn:disabled {
  opacity: 0.6;
}

.results-nav-right {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
}
.results-nav-right a {
  font-size: 13px;
  color: #202124;
  text-decoration: none;
}
.results-nav-right a:hover {
  text-decoration: underline;
}

.results-tabs-row {
  padding: 0 168px;
  overflow-x: auto;
}
.tabs-inner {
  display: flex;
  gap: 0;
}
.results-tab {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  font-size: 13px;
  color: #70757a;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  white-space: nowrap;
  transition: color 0.15s;
}
.results-tab:hover {
  color: #202124;
  background: #f8f9fa;
}
.results-tab.active {
  color: #1a73e8;
  border-bottom-color: #1a73e8;
}

.results-body {
  padding: 20px 0 40px;
}
.results-content {
  max-width: 660px;
  margin: 0 auto 0 168px;
  padding: 0 16px;
}

.results-stats {
  font-size: 13px;
  color: #70757a;
  margin-bottom: 20px;
}

.skeleton-wrap {
  display: flex;
  flex-direction: column;
  gap: 28px;
}
.skeleton-result {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.sk-url {
  height: 13px;
  width: 200px;
  background: #e8eaed;
  border-radius: 4px;
  animation: shimmer 1.4s infinite;
}
.sk-title {
  height: 20px;
  width: 420px;
  background: #e8eaed;
  border-radius: 4px;
  animation: shimmer 1.4s infinite 0.1s;
}
.sk-text {
  height: 13px;
  width: 580px;
  background: #e8eaed;
  border-radius: 4px;
  animation: shimmer 1.4s infinite 0.2s;
}
.sk-text.short {
  width: 380px;
}
@keyframes shimmer {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    opacity: 1;
  }
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.result-item {
  max-width: 660px;
}

.result-url-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.result-favicon {
  font-size: 16px;
}
.result-source {
  font-size: 14px;
  color: #202124;
}
.result-breadcrumb {
  font-size: 13px;
  color: #4d5156;
}

.result-title {
  display: block;
  font-size: 20px;
  color: #1a0dab;
  text-decoration: none;
  line-height: 1.3;
  font-family: "Google Sans", Arial, sans-serif;
  font-weight: 400;
  margin-bottom: 4px;
}
.result-title:hover {
  text-decoration: underline;
}
.result-title:visited {
  color: #681da8;
}

.result-score-badge {
  display: inline-block;
  font-size: 11px;
  color: #137333;
  background: #e6f4ea;
  padding: 2px 8px;
  border-radius: 10px;
  margin-bottom: 6px;
  font-weight: 500;
}

.result-snippet {
  font-size: 14px;
  color: #4d5156;
  line-height: 1.58;
}
.snippet-meta {
  color: #70757a;
}

.result-kws {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}
.kw-tag {
  font-size: 12px;
  color: #1a73e8;
  background: #e8f0fe;
  padding: 2px 10px;
  border-radius: 12px;
  cursor: pointer;
}
.kw-tag:hover {
  background: #d2e3fc;
}

.related-wrap {
  margin-top: 10px;
}
.related-toggle {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  font-size: 13px;
  color: #1a0dab;
  cursor: pointer;
  padding: 0;
}
.related-toggle:hover {
  text-decoration: underline;
}

.related-list {
  margin-top: 8px;
  border-left: 3px solid #e8eaed;
  padding-left: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.related-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.related-title {
  font-size: 14px;
  color: #1a0dab;
  text-decoration: none;
  line-height: 1.3;
}
.related-title:hover {
  text-decoration: underline;
}
.related-meta {
  font-size: 12px;
  color: #70757a;
}

.pagination {
  margin-top: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}
.page-logo {
  font-family: "Google Sans", Arial, sans-serif;
  font-size: 36px;
  letter-spacing: -1px;
}
.page-nums {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #70757a;
}
.page-current {
  color: #202124;
  font-weight: 700;
  background: #f8f9fa;
  padding: 6px 12px;
  border-radius: 50%;
}
.page-num {
  padding: 6px 12px;
  cursor: pointer;
  border-radius: 50%;
}
.page-num:hover {
  background: #f8f9fa;
  color: #202124;
}
.page-next {
  padding: 6px 12px;
  color: #1a0dab;
  cursor: pointer;
}
.page-next:hover {
  text-decoration: underline;
}
</style>
