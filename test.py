"""
RAPTOR RAG for Siemens-style Technical Manuals
===============================================
Heading hierarchy detected from the PDF:
    Size 48 / 20  →  Chapter number  (e.g. "3")
    Size 18        →  Document title  (cover / TOC only – skipped)
    Size 14        →  Section heading (e.g. "3.1 Allgemeines")
    Size 11        →  Sub-section heading (e.g. "Zweck der Dokumentation")
    Size 10 / 9    →  Body text
    Size 8  / 6    →  Footer / figure caption  (ignored)

The loader (load_technical_manual) uses pdfplumber to extract text
word-by-word, then reconstructs headings from font-size jumps.
Every text chunk receives rich metadata:
    page, chapter_num, chapter_title, section, subsection,
    heading_path, source
That metadata is propagated all the way up through the RAPTOR
summarisation tree so every node – leaf or summary – carries
full citation information.
"""

import os
import sys
import logging
import re
import numpy as np
import pandas as pd
import pdfplumber

from typing import List, Dict, Any, Optional, Tuple

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_core.messages import AIMessage
from langchain_core.documents import Document
from sklearn.mixture import GaussianMixture

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")


# ═══════════════════════════════════════════════════════════════
# FONT-SIZE CONSTANTS  (calibrated on Siemens SIMATIC manuals)
# ═══════════════════════════════════════════════════════════════

SIZE_CHAPTER_NUMBER = 14.0   # large chapter digit on first page of chapter
SIZE_CHAPTER_TITLE  = 18.0   # chapter title on chapter-opening page
SIZE_SECTION        = 14.0   # "3.1 Allgemeines" etc.
SIZE_SUBSECTION     = 11.0   # bold sub-headings inside a section
SIZE_BODY_HI        = 10.0   # normal body text
SIZE_BODY_LO        =  9.0   # slightly smaller body
SIZE_FOOTER         =  8.0   # footer / document number  → IGNORE
SIZE_CAPTION        =  6.0   # figure labels              → IGNORE

# Font sizes to skip entirely (footers, captions, figure annotations)
SKIP_SIZES = {6.0, 7.0, 7.5, 8.0, 12.0}


# ═══════════════════════════════════════════════════════════════
# 1. PDF LOADER  –  font-size-aware heading extraction
# ═══════════════════════════════════════════════════════════════

def _is_section_number(text: str) -> bool:
    """True for strings like '3', '3.1', '3.1.2'."""
    return bool(re.match(r"^\d+(\.\d+)*$", text.strip()))


def load_technical_manual(path: str) -> List[Dict[str, Any]]:
    """
    Parse a Siemens-style technical manual PDF using pdfplumber.

    Returns one dict per page:
        {
            "text":          str   – page body (headings removed),
            "page":          int   – 1-based page number,
            "chapter_num":   str   – e.g. "3"
            "chapter_title": str   – e.g. "Grundlagen"
            "section":       str   – e.g. "3.1 Allgemeines"
            "subsection":    str   – e.g. "Übersicht"
            "heading_path":  str   – breadcrumb for citations
            "source":        str   – basename of the PDF file
        }
    """
    source = os.path.basename(path)
    pages_out: List[Dict[str, Any]] = []

    # Running heading state – persists across pages
    current_chapter_num:   str = ""
    current_chapter_title: str = ""
    current_section:       str = ""
    current_subsection:    str = ""

    with pdfplumber.open(path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            page_num = page_idx + 1

            # ── extract words with font metadata ──────────────────────
            words = page.extract_words(
                extra_attrs=["size", "fontname"],
                keep_blank_chars=False,
            )

            body_lines: List[str]  = []
            pending_section_num:   str = ""   # buffer for "3.1" before we read its title

            i = 0
            while i < len(words):
                w        = words[i]
                sz       = round(w["size"], 1)
                txt      = w["text"].strip()

                # Skip footer / caption sizes entirely
                if sz in SKIP_SIZES or not txt:
                    i += 1
                    continue

                # ── CHAPTER number (size 48 / 20 at top of chapter page) ──
                if sz >= 20.0 and _is_section_number(txt) and "." not in txt:
                    # Only treat as chapter marker when it appears on a chapter-opening
                    # page, i.e. near the top third of the page.
                    page_height = page.height or 842
                    if w["top"] > page_height * 0.60:   # too low → TOC / index digit
                        body_lines.append(txt)
                        i += 1
                        continue

                    current_chapter_num   = txt
                    current_chapter_title = ""
                    current_section       = ""
                    current_subsection    = ""
                    j = i + 1
                    # Grab following words at size ≥18 on the same vertical zone as title
                    while j < len(words) and round(words[j]["size"], 1) >= 14.0:
                        ctxt = words[j]["text"].strip()
                        # Skip single uppercase letters (e.g. "A", "B" appendix tabs)
                        if ctxt and not _is_section_number(ctxt) and not re.match(r"^[A-Z]$", ctxt):
                            current_chapter_title += (" " if current_chapter_title else "") + ctxt
                        j += 1
                    i = j
                    continue

                # ── SECTION heading (size 14:  "3.1"  "Allgemeines") ──
                if sz >= 14.0:
                    if _is_section_number(txt) and "." in txt:
                        # Collect following words at same size as section title
                        sec_title = txt
                        j = i + 1
                        while j < len(words) and round(words[j]["size"], 1) >= 14.0:
                            stxt = words[j]["text"].strip()
                            if stxt and not _is_section_number(stxt):
                                sec_title += " " + stxt
                            j += 1
                        current_section    = sec_title
                        current_subsection = ""
                        i = j
                        continue
                    elif _is_section_number(txt) and "." not in txt:
                        # Repeated chapter number as running header – skip
                        i += 1
                        continue

                # ── SUB-SECTION heading (size 11, bold-ish single line) ──
                if sz >= 11.0:
                    # Collect all consecutive size-11 words on the same line
                    line_top = w["top"]
                    sub = txt
                    j   = i + 1
                    while j < len(words):
                        nw = words[j]
                        if round(nw["size"], 1) >= 11.0 and abs(nw["top"] - line_top) < 3:
                            sub += " " + nw["text"].strip()
                            j   += 1
                        else:
                            break
                    # Heuristic: treat as sub-section if it looks like a title
                    # (short, no full stop at end, not a plain body sentence)
                    if len(sub.split()) <= 8 and not sub.endswith("."):
                        current_subsection = sub
                        i = j
                        continue
                    else:
                        # It's just bold body text – fall through to body
                        body_lines.append(sub)
                        i = j
                        continue

                # ── BODY text ─────────────────────────────────────────
                body_lines.append(txt)
                i += 1

            # ── Build heading_path breadcrumb ─────────────────────────
            parts = []
            if current_chapter_num:
                chap = f"Kapitel {current_chapter_num}"
                if current_chapter_title:
                    chap += f": {current_chapter_title}"
                parts.append(chap)
            if current_section:
                parts.append(current_section)
            if current_subsection:
                parts.append(current_subsection)
            heading_path = " > ".join(parts) if parts else f"Seite {page_num}"

            page_text = " ".join(body_lines).strip()

            # Skip near-empty pages (e.g. chapter separators)
            if len(page_text) < 50:
                continue

            pages_out.append({
                "text":          page_text,
                "page":          page_num,
                "chapter_num":   current_chapter_num,
                "chapter_title": current_chapter_title,
                "section":       current_section,
                "subsection":    current_subsection,
                "heading_path":  heading_path,
                "source":        source,
            })

    logging.info(f"Loaded {len(pages_out)} content pages from '{source}'")
    return pages_out


# ═══════════════════════════════════════════════════════════════
# 2. RAPTOR HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def extract_text(item) -> str:
    """Unwrap AIMessage or plain string."""
    if isinstance(item, AIMessage):
        return item.content
    return str(item)


def embed_texts(texts: List[str]) -> List[List[float]]:
    emb = OpenAIEmbeddings()
    logging.info(f"Embedding {len(texts)} texts …")
    return emb.embed_documents([extract_text(t) for t in texts])


def perform_clustering(embeddings: np.ndarray, n_clusters: int) -> np.ndarray:
    n_clusters = max(2, min(n_clusters, len(embeddings) - 1))
    logging.info(f"Clustering into {n_clusters} clusters …")
    gm = GaussianMixture(n_components=n_clusters, random_state=42)
    return gm.fit_predict(embeddings)


def summarize_cluster(
    texts: List[str],
    meta_list: List[Dict],
    llm: ChatOpenAI,
) -> Tuple[str, Dict]:
    """
    Summarise a cluster's texts and build aggregated citation metadata.
    Returns (summary_text, merged_metadata).
    """
    logging.info(f"Summarising cluster of {len(texts)} chunks …")

    # ── aggregate source provenance ──
    chapters  = sorted({f"Kapitel {m['chapter_num']}: {m['chapter_title']}"
                         for m in meta_list if m.get("chapter_num")})
    sections  = sorted({m["section"]    for m in meta_list if m.get("section")})
    subsecs   = sorted({m["subsection"] for m in meta_list if m.get("subsection")})
    pages     = sorted({m["page"]       for m in meta_list if m.get("page")})
    sources   = sorted({m["source"]     for m in meta_list if m.get("source")})
    hpaths    = sorted({m.get("heading_path", "") for m in meta_list})

    prompt = ChatPromptTemplate.from_template(
        "Summarize the following technical documentation concisely in the same language:\n\n{text}"
    )
    chain = prompt | llm
    summary_text = extract_text(chain.invoke({"text": "\n\n---\n\n".join(texts)}))

    merged_meta = {
        # flat fields (used for leaf-level citations – cleared for summaries)
        "page":          None,
        "chapter_num":   "",
        "chapter_title": "",
        "section":       "",
        "subsection":    "",
        "heading_path":  "",
        # aggregated fields
        "chapters":      chapters,
        "sections":      sections,
        "subsections":   subsecs,
        "pages":         pages,
        "sources":       sources,
        "heading_paths": hpaths,
    }
    return summary_text, merged_meta


# ═══════════════════════════════════════════════════════════════
# 3. VECTORSTORE
# ═══════════════════════════════════════════════════════════════

def build_vectorstore(tree_results: Dict[int, pd.DataFrame],
                      embeddings: OpenAIEmbeddings) -> FAISS:
    docs: List[Document] = []
    for level, df in tree_results.items():
        for _, row in df.iterrows():
            meta = dict(row["metadata"])
            meta["raptor_level"] = level
            docs.append(Document(page_content=str(row["text"]), metadata=meta))
    logging.info(f"Building FAISS store with {len(docs)} documents …")
    return FAISS.from_documents(docs, embeddings)


def create_retriever(vectorstore: FAISS, llm: ChatOpenAI,
                     k: int = 6) -> ContextualCompressionRetriever:
    base = vectorstore.as_retriever(search_kwargs={"k": k})
    prompt = ChatPromptTemplate.from_template(
        "Extract only the information relevant to the question from the context.\n\n"
        "Context: {context}\nQuestion: {question}\n\nRelevant Information:"
    )
    extractor = LLMChainExtractor.from_llm(llm, prompt=prompt)
    return ContextualCompressionRetriever(base_compressor=extractor,
                                          base_retriever=base)


# ═══════════════════════════════════════════════════════════════
# 4. CITATION FORMATTER
# ═══════════════════════════════════════════════════════════════

def format_citations(docs: List[Document]) -> List[str]:
    """
    Build a human-readable citation string for each retrieved document.

    Leaf nodes  →  single heading_path + page + source
    Summary nodes → list of heading_paths + page range + sources
    """
    citations = []
    seen_paths = set()  # deduplicate identical citations

    for i, doc in enumerate(docs, start=1):
        m = doc.metadata

        # ── location breadcrumb ──
        hpaths = m.get("heading_paths") or []   # summary nodes  (list)
        hpath  = m.get("heading_path",  "")     # leaf nodes     (str)

        if hpaths:
            unique = [p for p in hpaths if p]
            location = " | ".join(sorted(set(unique))) or "Unbekannter Abschnitt"
        elif hpath:
            location = hpath
        else:
            # Reconstruct from individual fields
            parts = []
            if m.get("chapter_num"):
                c = f"Kapitel {m['chapter_num']}"
                if m.get("chapter_title"):
                    c += f": {m['chapter_title']}"
                parts.append(c)
            if m.get("section"):
                parts.append(m["section"])
            if m.get("subsection"):
                parts.append(m["subsection"])
            location = " > ".join(parts) if parts else "Unbekannter Abschnitt"

        # ── page range ──
        pages = m.get("pages") or ([m["page"]] if m.get("page") else [])
        pages = [p for p in pages if p]
        if pages:
            mn, mx = min(pages), max(pages)
            page_str = f"S. {mn}" if mn == mx else f"S. {mn}–{mx}"
        else:
            page_str = ""

        # ── source file ──
        sources    = m.get("sources") or ([m["source"]] if m.get("source") else [])
        source_str = ", ".join(sources) if sources else ""

        # ── RAPTOR level (debug info) ──
        level     = m.get("raptor_level", "?")
        level_tag = f"[L{level}]"

        # ── assemble ──
        parts_out = [f"[{i}] {level_tag} {location}"]
        if page_str:   parts_out.append(page_str)
        if source_str: parts_out.append(source_str)

        citation = " — ".join(parts_out)

        if citation not in seen_paths:
            seen_paths.add(citation)
            citations.append(citation)

    return citations


# ═══════════════════════════════════════════════════════════════
# 5. MAIN RAPTOR CLASS
# ═══════════════════════════════════════════════════════════════

class RAPTORMethod:
    def __init__(self, enriched_pages: List[Dict[str, Any]],
                 max_levels: int = 3):
        self.enriched_pages = enriched_pages
        self.max_levels     = max_levels
        self.embeddings     = OpenAIEmbeddings()
        self.llm            = ChatOpenAI(model_name="gpt-4o-mini")
        self.tree_results   = self._build_raptor_tree()

    # ── tree construction ────────────────────────────────────────

    def _build_raptor_tree(self) -> Dict[int, pd.DataFrame]:
        results: Dict[int, pd.DataFrame] = {}

        # Level 0 – raw pages with full heading metadata
        current_texts = [p["text"] for p in self.enriched_pages]
        current_meta  = [
            {
                "page":          p["page"],
                "chapter_num":   p["chapter_num"],
                "chapter_title": p["chapter_title"],
                "section":       p["section"],
                "subsection":    p["subsection"],
                "heading_path":  p["heading_path"],
                "source":        p["source"],
                "level":         0,
                "origin":        "original",
                "parent_id":     None,
                # aggregated fields (empty at leaf level)
                "chapters":      [],
                "sections":      [],
                "subsections":   [],
                "pages":         [p["page"]],
                "sources":       [p["source"]],
                "heading_paths": [p["heading_path"]],
            }
            for p in self.enriched_pages
        ]

        for level in range(1, self.max_levels + 1):
            logging.info(f"\n{'─'*50}\nRAPTOR Level {level}\n{'─'*50}")

            emb_list       = embed_texts(current_texts)
            n_clusters     = min(10, len(current_texts) // 2)
            cluster_labels = perform_clustering(np.array(emb_list), n_clusters)

            df = pd.DataFrame({
                "text":      current_texts,
                "embedding": emb_list,
                "cluster":   cluster_labels,
                "metadata":  current_meta,
            })
            results[level - 1] = df

            next_texts: List[str] = []
            next_meta:  List[Dict] = []

            for cluster_id in sorted(df["cluster"].unique()):
                rows   = df[df["cluster"] == cluster_id]
                ctexts = rows["text"].tolist()
                cmetas = rows["metadata"].tolist()

                summary_text, agg_meta = summarize_cluster(ctexts, cmetas, self.llm)
                agg_meta.update({
                    "level":     level,
                    "origin":    f"summary_cluster_{cluster_id}_level_{level-1}",
                    "id":        f"summary_{level}_{cluster_id}",
                    "child_ids": [m.get("id") for m in cmetas],
                })
                next_texts.append(summary_text)
                next_meta.append(agg_meta)

            current_texts = next_texts
            current_meta  = next_meta

            if len(current_texts) <= 1:
                results[level] = pd.DataFrame({
                    "text":      current_texts,
                    "embedding": embed_texts(current_texts),
                    "cluster":   [0],
                    "metadata":  current_meta,
                })
                logging.info(f"Tree complete at level {level} (single summary).")
                break

        return results

    # ── query ────────────────────────────────────────────────────

    def run(self, query: str) -> Dict[str, Any]:
        vectorstore   = build_vectorstore(self.tree_results, self.embeddings)
        retriever     = create_retriever(vectorstore, self.llm)

        logging.info(f"Query: {query}")
        relevant_docs = retriever.get_relevant_documents(query)
        citations     = format_citations(relevant_docs)
        citation_block = "\n".join(citations)
        context        = "\n\n".join(d.page_content for d in relevant_docs)

        prompt = ChatPromptTemplate.from_template(
            "You are a technical documentation assistant.\n"
            "Answer the question using ONLY the provided context.\n"
            "After your answer, add a 'Sources:' section listing the citation numbers "
            "[1], [2], … that you relied on.\n\n"
            "Context:\n{context}\n\n"
            "Available citations:\n{citations}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        )
        chain  = LLMChain(llm=self.llm, prompt=prompt)
        answer = chain.run(context=context, citations=citation_block, question=query)

        return {
            "query":               query,
            "answer":              answer,
            "citations":           citations,
            "retrieved_documents": [
                {"content": d.page_content, "metadata": d.metadata}
                for d in relevant_docs
            ],
            "model_used": self.llm.model_name,
        }


# ═══════════════════════════════════════════════════════════════
# 6. CLI ENTRY POINT
# ═══════════════════════════════════════════════════════════════

def parse_args():
    import argparse
    p = argparse.ArgumentParser(
        description="RAPTOR RAG for Siemens-style technical manuals"
    )
    p.add_argument("--path",
                   default="../data/ps7opc_a_de-DE.pdf",
                   help="Path to the technical manual PDF.")
    p.add_argument("--query",
                   default="Wie konfiguriere ich den OPC-UA-Server?",
                   help="Question to ask.")
    p.add_argument("--max_levels", type=int, default=3,
                   help="RAPTOR tree depth (default: 3).")
    return p.parse_args()


if __name__ == "__main__":
    args     = parse_args()
    pages    = load_technical_manual(args.path)

    # Quick sanity-check: print heading structure of first 15 pages
    print("\n── Heading structure (first 15 pages) ──")
    for p in pages[:15]:
        print(f"  p.{p['page']:3d}  {p['heading_path']}")
    print()

    raptor = RAPTORMethod(pages, max_levels=args.max_levels)
    result = raptor.run(args.query)

    print("\n" + "═" * 70)
    print(f"QUERY : {result['query']}")
    print("─" * 70)
    print(f"ANSWER:\n{result['answer']}")
    print("─" * 70)
    print("SOURCES:")
    for c in result["citations"]:
        print(f"  {c}")
    print("═" * 70)
