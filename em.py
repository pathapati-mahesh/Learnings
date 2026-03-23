"""
vectorize.py
============
PIPELINE 1 — Build RAPTOR tree and persist to Milvus.

Run this once per PDF (or when the PDF changes).
After this script finishes, retrieve.py can answer questions
without any re-embedding or re-summarisation.

WHAT IT DOES
------------
1. Load PDF with PyPDFLoader  →  pages with page numbers
2. Embed pages (OpenAI)
3. Cluster similar pages (GMM)
4. Summarise each cluster (GPT-4o-mini)
5. Repeat for max_levels
6. Write ALL nodes (leaf + summaries) into a Milvus collection

MILVUS COLLECTION SCHEMA
-------------------------
  id          INT64       auto primary key
  embedding   FLOAT_VECTOR(1536)
  text        VARCHAR(65535)
  metadata    JSON         ← page, pages, raptor_level, origin, source

INSTALL
-------
  pip install pymilvus langchain-openai scikit-learn python-dotenv

LOCAL (no server):
  pip install "pymilvus[model]"     # includes Milvus Lite
  db_uri = "milvus_raptor.db"       # single local file

REMOTE (Milvus server or Zilliz Cloud):
  db_uri = "http://localhost:19530"
  db_uri = "https://<cluster>.zillizcloud.com"
  pass token="<api_key>" for Zilliz Cloud

USAGE
-----
  python vectorize.py \\
      --pdf   manual.pdf \\
      --pdf_id manual_v1 \\
      --uri   milvus_raptor.db

  # force rebuild even if collection already exists
  python vectorize.py --pdf manual.pdf --pdf_id manual_v1 --force
"""

import os
import json
import logging
import argparse
import numpy as np
import pandas as pd
from typing import List, Dict, Any

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_community.document_loaders import PyPDFLoader
from sklearn.mixture import GaussianMixture

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

EMBED_DIM        = 1536          # OpenAI text-embedding-ada-002
MAX_VARCHAR_LEN  = 65_535        # Milvus VARCHAR ceiling


# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def _unwrap(item) -> str:
    return item.content if isinstance(item, AIMessage) else str(item)


def _embed(texts: List[str]) -> List[List[float]]:
    logging.info(f"  embedding {len(texts)} texts ...")
    return OpenAIEmbeddings().embed_documents([_unwrap(t) for t in texts])


def _cluster(matrix: np.ndarray, k: int) -> np.ndarray:
    k = max(2, min(k, len(matrix) - 1))
    logging.info(f"  clustering into {k} groups ...")
    return GaussianMixture(n_components=k, random_state=42).fit_predict(matrix)


def _summarise(texts: List[str], llm: ChatOpenAI) -> str:
    prompt = ChatPromptTemplate.from_template(
        "Summarize the following text concisely in the same language:\n\n{text}"
    )
    return _unwrap((prompt | llm).invoke({"text": "\n\n".join(texts)}))


def _collection_name(pdf_id: str) -> str:
    """Milvus collection names must be alphanumeric + underscore."""
    safe = "".join(c if c.isalnum() else "_" for c in pdf_id)
    return f"raptor_{safe}"


# ═══════════════════════════════════════════════════════════════════════
# MILVUS  —  schema + write
# ═══════════════════════════════════════════════════════════════════════

def _create_collection(client, name: str) -> None:
    """Create the Milvus collection with RAPTOR schema."""
    from pymilvus import DataType

    schema = client.create_schema(auto_id=True, enable_dynamic_field=False)
    schema.add_field("id",        DataType.INT64,        is_primary=True)
    schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=EMBED_DIM)
    schema.add_field("text",      DataType.VARCHAR,       max_length=MAX_VARCHAR_LEN)
    # All RAPTOR metadata (page, pages, raptor_level, origin, source) in one JSON column
    schema.add_field("metadata",  DataType.JSON)

    # HNSW index on the vector field
    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name  = "embedding",
        index_type  = "HNSW",
        metric_type = "COSINE",
        params      = {"M": 16, "efConstruction": 200},
    )

    client.create_collection(
        collection_name = name,
        schema          = schema,
        index_params    = index_params,
    )
    logging.info(f"Milvus: created collection '{name}'")


def _insert_nodes(client, name: str, nodes: List[Dict]) -> None:
    """
    Insert RAPTOR tree nodes into Milvus.

    Each node dict:
        text        str
        embedding   List[float]
        metadata    dict  (page, pages, raptor_level, origin, source)
    """
    rows = []
    for n in nodes:
        meta = dict(n["metadata"])
        # Milvus JSON field accepts Python dicts directly
        # but values must be JSON-serialisable
        clean_meta = {}
        for k, v in meta.items():
            if v is None:
                clean_meta[k] = None
            elif isinstance(v, list):
                clean_meta[k] = v          # lists of int/str are fine
            else:
                clean_meta[k] = v

        rows.append({
            "embedding": n["embedding"],
            "text":      n["text"][:MAX_VARCHAR_LEN],
            "metadata":  clean_meta,
        })

    client.insert(collection_name=name, data=rows)
    logging.info(f"Milvus: inserted {len(rows)} nodes into '{name}'")


# ═══════════════════════════════════════════════════════════════════════
# RAPTOR TREE  (same logic as before, returns flat list of nodes)
# ═══════════════════════════════════════════════════════════════════════

def build_raptor_tree(
    texts:      List[str],
    metadatas:  List[Dict],
    llm:        ChatOpenAI,
    max_levels: int = 3,
) -> List[Dict[str, Any]]:
    """
    Build the RAPTOR tree and return every node as a flat list.

    Each node:
        {
            "text":      str
            "embedding": List[float]
            "metadata":  {
                "raptor_level": int,
                "page":         int | None,   # 0-based, None for summaries
                "pages":        List[int],    # all source pages
                "origin":       str,
                "source":       str,
            }
        }
    """
    all_nodes: List[Dict] = []

    current_texts = [_unwrap(t) for t in texts]
    current_meta  = [
        {
            "raptor_level": 0,
            "origin":       "original",
            "page":         m.get("page"),
            "pages":        [m.get("page")],
            "source":       m.get("source", ""),
        }
        for m in metadatas
    ]

    for level in range(1, max_levels + 1):
        logging.info(f"\n── RAPTOR level {level} ──")

        embs   = _embed(current_texts)
        k      = min(10, len(current_texts) // 2)
        labels = _cluster(np.array(embs), k)

        # Store current level nodes
        for text, emb, meta in zip(current_texts, embs, current_meta):
            node_meta = dict(meta)
            node_meta["raptor_level"] = level - 1
            all_nodes.append({
                "text":      text,
                "embedding": emb,
                "metadata":  node_meta,
            })

        # Summarise each cluster
        next_texts: List[str]  = []
        next_meta:  List[Dict] = []

        for cid in sorted(set(labels)):
            idx    = [i for i, l in enumerate(labels) if l == cid]
            ctexts = [current_texts[i] for i in idx]
            cmetas = [current_meta[i]  for i in idx]

            logging.info(f"  cluster {cid}: summarising {len(ctexts)} chunks ...")
            summary = _summarise(ctexts, llm)

            all_pages = sorted(set(
                p for m in cmetas for p in (m.get("pages") or [])
                if p is not None
            ))

            next_texts.append(summary)
            next_meta.append({
                "raptor_level": level,
                "origin":       f"summary_cluster_{cid}_level_{level-1}",
                "page":         None,
                "pages":        all_pages,
                "source":       cmetas[0].get("source", "") if cmetas else "",
            })

        current_texts = next_texts
        current_meta  = next_meta

        if len(current_texts) <= 1:
            # Root node — store and stop
            root_emb = _embed(current_texts)
            all_nodes.append({
                "text":      current_texts[0],
                "embedding": root_emb[0],
                "metadata":  {**current_meta[0], "raptor_level": level},
            })
            logging.info(f"Tree complete at level {level} (root node).")
            break

    logging.info(f"Total nodes in tree: {len(all_nodes)}")
    return all_nodes


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Vectorize PDF into Milvus")
    parser.add_argument("--pdf",        required=True,
                        help="Path to the PDF file")
    parser.add_argument("--pdf_id",     default=None,
                        help="Unique ID for this PDF (default: filename)")
    parser.add_argument("--uri",        default="milvus_raptor.db",
                        help="Milvus URI — local .db file or http://host:port")
    parser.add_argument("--token",      default="",
                        help="Milvus/Zilliz API token (for cloud)")
    parser.add_argument("--max_levels", type=int, default=3)
    parser.add_argument("--force",      action="store_true",
                        help="Drop and recreate collection if it already exists")
    args = parser.parse_args()

    pdf_id          = args.pdf_id or os.path.splitext(os.path.basename(args.pdf))[0]
    collection_name = _collection_name(pdf_id)

    # ── connect to Milvus ──────────────────────────────────────────────
    try:
        from pymilvus import MilvusClient
    except ImportError:
        raise ImportError("Run:  pip install pymilvus")

    client = MilvusClient(uri=args.uri, token=args.token)
    logging.info(f"Connected to Milvus @ '{args.uri}'")

    # ── skip if already built ──────────────────────────────────────────
    exists = client.has_collection(collection_name)
    if exists and not args.force:
        count = client.get_collection_stats(collection_name)["row_count"]
        logging.info(
            f"Collection '{collection_name}' already exists ({count} nodes). "
            "Use --force to rebuild."
        )
        return

    if exists and args.force:
        client.drop_collection(collection_name)
        logging.info(f"Dropped existing collection '{collection_name}'")

    # ── load PDF ───────────────────────────────────────────────────────
    logging.info(f"Loading '{args.pdf}' ...")
    documents = PyPDFLoader(args.pdf).load()
    texts     = [doc.page_content for doc in documents]
    metadatas = [doc.metadata     for doc in documents]
    logging.info(f"Loaded {len(texts)} pages")

    # ── build RAPTOR tree ──────────────────────────────────────────────
    llm   = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    nodes = build_raptor_tree(texts, metadatas, llm, max_levels=args.max_levels)

    # ── create collection + insert ─────────────────────────────────────
    _create_collection(client, collection_name)
    _insert_nodes(client, collection_name, nodes)

    # ── summary ────────────────────────────────────────────────────────
    stats = client.get_collection_stats(collection_name)
    print(f"\n✓ Vectorization complete")
    print(f"  Collection : {collection_name}")
    print(f"  URI        : {args.uri}")
    print(f"  Nodes      : {stats['row_count']}")
    print(f"  PDF pages  : {len(texts)}")
    print(f"\nNow run retrieve.py to query this collection.")


if __name__ == "__main__":
    main()
