"""
retrieve.py
===========
PIPELINE 2 — Query the RAPTOR tree stored in Milvus.

Completely stateless — no PDF needed, no re-embedding, no summaries.
Just connects to Milvus and answers questions.

WHAT IT DOES
------------
1. Connect to Milvus
2. Embed the query (OpenAI)
3. Vector search → top-k nodes from all RAPTOR levels
4. Contextual compression → keep only relevant parts
5. LLM answer
6. Exact page number lookup
7. Return answer + page numbers + similarity scores

USAGE
-----
  # as a script
  python retrieve.py \\
      --pdf_id manual_v1 \\
      --uri    milvus_raptor.db \\
      --query  "What is the OPC-UA port number?"

  # as a module (e.g. in a FastAPI endpoint)
  from retrieve import Retriever

  r = Retriever(pdf_id="manual_v1", uri="milvus_raptor.db")
  result = r.ask("What is the OPC-UA port number?")
  print(result["answer"])        # "Port 4863."
  print(result["page_numbers"])  # [57]
  print(result["scores"])        # [{"score": 0.94, "page": 57, "level": 0}, ...]
"""

import os
import json
import logging
import argparse
import numpy as np
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain.chains import LLMChain

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")


# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def _unwrap(item) -> str:
    return item.content if isinstance(item, AIMessage) else str(item)


def _collection_name(pdf_id: str) -> str:
    safe = "".join(c if c.isalnum() else "_" for c in pdf_id)
    return f"raptor_{safe}"


def _parse_meta(raw_meta: Any) -> Dict:
    """
    Milvus returns JSON fields as dicts or strings depending on SDK version.
    Normalise to a plain dict.
    """
    if isinstance(raw_meta, str):
        try:
            return json.loads(raw_meta)
        except Exception:
            return {}
    return raw_meta or {}


# ═══════════════════════════════════════════════════════════════════════
# EXACT PAGE FINDER
# ═══════════════════════════════════════════════════════════════════════

def _find_exact_pages(
    query_emb:      np.ndarray,
    retrieved_hits: List[Dict],
    leaf_cache:     Dict[int, str],          # page_0based -> leaf text
    embeddings:     OpenAIEmbeddings,
) -> List[int]:
    """
    Return only the exact page(s) where the answer lives.

    Leaf hits  (raptor_level 0) have one page — use directly.
    Summary hits (raptor_level >= 1) carry a pages list — re-rank
    the candidate leaf pages by cosine similarity and keep the best.
    """
    exact: set = set()

    for hit in retrieved_hits:
        meta  = hit["metadata"]
        level = meta.get("raptor_level", 0)

        if level == 0:
            p = meta.get("page")
            if p is not None:
                exact.add(int(p) + 1)                   # 0-based → 1-based
        else:
            candidates = [int(p) for p in (meta.get("pages") or []) if p is not None]
            if not candidates:
                continue

            best_score, best_page = -1.0, None
            for p in candidates:
                leaf_text = leaf_cache.get(p)
                if not leaf_text:
                    continue
                leaf_emb = np.array(embeddings.embed_query(leaf_text))
                score    = float(
                    np.dot(query_emb, leaf_emb)
                    / (np.linalg.norm(query_emb) * np.linalg.norm(leaf_emb) + 1e-9)
                )
                if score > best_score:
                    best_score, best_page = score, p

            if best_page is not None:
                exact.add(best_page + 1)                # 0-based → 1-based

    return sorted(exact)


# ═══════════════════════════════════════════════════════════════════════
# RETRIEVER CLASS
# ═══════════════════════════════════════════════════════════════════════

class Retriever:
    """
    Stateless retriever — reads everything from Milvus.
    Instantiate once and call ask() many times.

    Parameters
    ----------
    pdf_id    : same id used in vectorize.py  e.g. "manual_v1"
    uri       : Milvus URI  e.g. "milvus_raptor.db" or "http://localhost:19530"
    token     : API token for Zilliz Cloud (leave "" for local)
    """

    def __init__(
        self,
        pdf_id: str,
        uri:    str = "milvus_raptor.db",
        token:  str = "",
    ):
        try:
            from pymilvus import MilvusClient
        except ImportError:
            raise ImportError("Run:  pip install pymilvus")

        self._pdf_id          = pdf_id
        self._collection_name = _collection_name(pdf_id)
        self._embeddings      = OpenAIEmbeddings()
        self._llm             = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

        self._client = MilvusClient(uri=uri, token=token)

        if not self._client.has_collection(self._collection_name):
            raise ValueError(
                f"Collection '{self._collection_name}' not found in Milvus @ '{uri}'.\n"
                f"Run vectorize.py first with --pdf_id {pdf_id}"
            )

        count = self._client.get_collection_stats(self._collection_name)["row_count"]
        logging.info(
            f"Retriever ready: '{self._collection_name}' ({count} nodes) @ '{uri}'"
        )

        # Build leaf-page cache once for exact page lookup
        # (only fetches level-0 nodes — minimal data transfer)
        self._leaf_cache: Dict[int, str] = self._build_leaf_cache()

    def _build_leaf_cache(self) -> Dict[int, str]:
        """
        Fetch all level-0 (leaf) nodes from Milvus and build a
        {page_0based: text} lookup used by _find_exact_pages.
        """
        results = self._client.query(
            collection_name = self._collection_name,
            filter          = 'metadata["raptor_level"] == 0',
            output_fields   = ["text", "metadata"],
            limit           = 16_384,   # enough for very large PDFs
        )
        cache: Dict[int, str] = {}
        for row in results:
            meta = _parse_meta(row.get("metadata", {}))
            p    = meta.get("page")
            if p is not None:
                cache[int(p)] = row.get("text", "")
        logging.info(f"Leaf cache built: {len(cache)} pages")
        return cache

    # ── PUBLIC ────────────────────────────────────────────────────────

    def ask(self, query: str, k: int = 6) -> Dict[str, Any]:
        """
        Answer a question using the stored RAPTOR tree.

        Parameters
        ----------
        query : the question
        k     : number of Milvus hits to retrieve (default 6)

        Returns
        -------
        {
            "query":        str
            "answer":       str    or "Content not found in document."
            "page_numbers": list   exact page numbers ([] if not found)
            "scores":       list   [{"score", "page", "pages", "level"}]
            "model_used":   str
        }
        """
        logging.info(f"Query: {query!r}")

        # ── 1. embed query ─────────────────────────────────────────────
        query_emb = self._embeddings.embed_query(query)

        # ── 2. vector search in Milvus ─────────────────────────────────
        search_res = self._client.search(
            collection_name = self._collection_name,
            data            = [query_emb],
            anns_field      = "embedding",
            search_params   = {"metric_type": "COSINE", "params": {"ef": 64}},
            limit           = k,
            output_fields   = ["text", "metadata"],
        )
        # search_res[0] = hits for the first (only) query vector
        raw_hits = [
            {
                "text":     hit["entity"]["text"],
                "metadata": _parse_meta(hit["entity"]["metadata"]),
                "score":    round(hit["distance"], 4),   # cosine similarity [0,1]
            }
            for hit in search_res[0]
        ]

        # ── 3. contextual compression ──────────────────────────────────
        comp_prompt = ChatPromptTemplate.from_template(
            "Extract only the information relevant to the question.\n\n"
            "Context: {context}\n"
            "Question: {question}\n\n"
            "Relevant Information:"
        )
        compressed = self._compress(query, raw_hits, comp_prompt)

        # ── 4. exact page numbers ──────────────────────────────────────
        source_pages = _find_exact_pages(
            query_emb  = np.array(query_emb),
            retrieved_hits = compressed,
            leaf_cache = self._leaf_cache,
            embeddings = self._embeddings,
        )

        # ── 5. answer ──────────────────────────────────────────────────
        context    = "\n\n".join(h["text"] for h in compressed)
        ans_prompt = ChatPromptTemplate.from_template(
            "Answer the question using ONLY the context below.\n"
            "If the answer is not present in the context, reply with exactly: "
            '"Content not found in document."\n\n'
            "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        )
        answer = LLMChain(llm=self._llm, prompt=ans_prompt).run(
            context=context, question=query
        ).strip()

        if "content not found" in answer.lower():
            source_pages = []

        # ── 6. scores output ───────────────────────────────────────────
        scores = []
        for hit in compressed:
            meta = hit["metadata"]
            p    = meta.get("page")
            scores.append({
                "score":  hit["score"],
                "page":   (int(p) + 1) if p is not None else None,
                "pages":  meta.get("pages"),
                "level":  meta.get("raptor_level"),
            })
        scores.sort(key=lambda x: x["score"] or 0, reverse=True)

        return {
            "query":        query,
            "answer":       answer,
            "page_numbers": source_pages,
            "scores":       scores,
            "model_used":   self._llm.model_name,
        }

    def _compress(
        self,
        query:   str,
        hits:    List[Dict],
        prompt:  ChatPromptTemplate,
    ) -> List[Dict]:
        """
        Run contextual compression per hit — keep only the part relevant
        to the query.  Returns hits with updated "text" fields.
        Hits whose text is compressed to nothing are dropped.
        """
        compressed = []
        for hit in hits:
            try:
                relevant = _unwrap(
                    (prompt | self._llm).invoke({
                        "context":  hit["text"],
                        "question": query,
                    })
                ).strip()
            except Exception:
                relevant = hit["text"]

            if relevant and relevant.lower() not in (
                "no relevant information", "none", ""
            ):
                compressed.append({**hit, "text": relevant})

        return compressed if compressed else hits   # fallback: uncompressed


# ═══════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Query RAPTOR tree from Milvus")
    parser.add_argument("--pdf_id",  required=True,
                        help="PDF identifier used during vectorization")
    parser.add_argument("--uri",     default="milvus_raptor.db",
                        help="Milvus URI")
    parser.add_argument("--token",   default="",
                        help="API token for Zilliz Cloud")
    parser.add_argument("--query",   required=True,
                        help="Question to ask")
    parser.add_argument("--k",       type=int, default=6,
                        help="Number of nodes to retrieve (default 6)")
    args = parser.parse_args()

    r      = Retriever(pdf_id=args.pdf_id, uri=args.uri, token=args.token)
    result = r.ask(args.query, k=args.k)

    print(f"\nQuery   : {result['query']}")
    print(f"Answer  : {result['answer']}")

    if result["page_numbers"]:
        print(f"Pages   : {result['page_numbers']}")
    else:
        print("Pages   : Content not found in document.")

    print("\nSimilarity scores:")
    for s in result["scores"]:
        pg  = f"p.{s['page']}" if s["page"] is not None else f"pp.{s['pages']}"
        bar = "█" * int((s["score"] or 0) * 20)
        print(f"  [{s['score']:.4f}] {bar:<20}  L{s['level']}  {pg}")


if __name__ == "__main__":
    main()
