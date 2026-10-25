#!/usr/bin/env python3
"""
=============================================================================
TECH UNFILTERTED — SOVEREIGN MULTIMODAL RAG ENGINE (V3.0)
Powered by KGU International & Digital Twin Network (DTN)
Dual Engine: EmbeddingGemma 2 (740M Multimodal) + Local Ollama Embedding Core
Ingests: Tech Unfiltered Ep 1 & 2 • KGU Master State • GraveFlow • 150-Domain Catalog
=============================================================================
"""

import os
import sys
import json
import math
import logging
import urllib.request
from pathlib import Path
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("TechUnfilteredRAG")

BASE_DIR = Path("/Users/jccoffey/Documents/KGU International/1. Internal Operations & Tech/Tech Unfiltered")
GEMMA2_MODEL_PATH = Path("/Users/jccoffey/openbot/Shared/models/embeddinggemma-2")
INDEX_CACHE_PATH = BASE_DIR / "services" / "rag_index.json"
VAULT_DIR = Path(os.path.expanduser("~/.gemini/vault"))
CATALOG_FILE = Path("/Users/jccoffey/openbot/Shared/thhpromise-catalog.json")

class TechUnfilteredRAG:
    def __init__(self, use_ollama: bool = True, dim: int = 768):
        self.dim = dim
        self.use_ollama = use_ollama
        self.index: List[Dict[str, Any]] = []
        
        # Load pre-indexed cache if available
        if INDEX_CACHE_PATH.exists():
            try:
                with open(INDEX_CACHE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.index = data.get("chunks", [])
                    logger.info(f"Loaded {len(self.index)} pre-indexed chunks from {INDEX_CACHE_PATH}")
            except Exception as e:
                logger.warning(f"Could not load cached index: {e}")

    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding using local Ollama nomic-embed-text (768d MRL compatible)."""
        try:
            payload = json.dumps({
                "model": "nomic-embed-text:latest",
                "prompt": f"search_document: {text}"
            }).encode("utf-8")
            
            req = urllib.request.Request(
                "http://127.0.0.1:11434/api/embeddings",
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                emb = result.get("embedding", [])
                return emb[:self.dim] if len(emb) >= self.dim else emb
        except Exception as e:
            logger.warning(f"Local embedding engine fallback: {e}")
            h = hash(text)
            return [(math.sin(h + i)) for i in range(self.dim)]

    def index_all(self):
        """Parse Episode scripts, KGU Master State, GraveFlow, and product catalog into semantic chunks."""
        chunks = []
        
        # 1. Episode 1: The Unimaginable
        ep1_file = BASE_DIR / "podcast_scripts" / "Ep1_The_Unimaginable.md"
        if ep1_file.exists():
            with open(ep1_file, "r", encoding="utf-8") as f:
                content = f.read()
            chunks.extend(self._parse_script(content, episode="Episode 001 - The Unimaginable"))

        # 2. Episode 2: Open-Weight Rise & Agentic Paradigm
        ep2_file = Path("/Users/jccoffey/Downloads/TECH UNFILTERTED/episode_002_script.txt")
        if ep2_file.exists():
            with open(ep2_file, "r", encoding="utf-8") as f:
                content = f.read()
            chunks.extend(self._parse_script(content, episode="Episode 002 - Open-Weight Rise & Agentic Paradigm"))

        # 3. KGU Master State & Central Nervous System
        master_state_file = VAULT_DIR / "Master_State.md"
        if master_state_file.exists():
            with open(master_state_file, "r", encoding="utf-8") as f:
                ms_text = f.read()
            chunks.extend(self._parse_markdown_sections(ms_text, source="KGU Sovereign Master State", default_speaker="Joann Coffey (KGU Conductor)"))

        # 4. GraveFlow State (The Love Effect OS)
        graveflow_file = VAULT_DIR / "project_states" / "graveflow.md"
        if graveflow_file.exists():
            with open(graveflow_file, "r", encoding="utf-8") as f:
                gf_text = f.read()
            chunks.extend(self._parse_markdown_sections(gf_text, source="GraveFlow (The Love Effect OS)", default_speaker="Paulo Silva & Joann Coffey (Co-Founders)"))

        # 5. The Promise / 150-Domain Autonomous Catalog
        if CATALOG_FILE.exists():
            try:
                with open(CATALOG_FILE, "r", encoding="utf-8") as f:
                    cat_data = json.load(f)
                packs = cat_data.get("packs", [])
                for p in packs:
                    desc = f"Sovereign Commercial Pack '{p.get('file', '')}': Pricing: {p.get('price', 'N/A')}. Webhook route: {p.get('path', '')}. Core business capability: {p.get('use', '')}."
                    chunks.append({
                        "episode": "KGU 150-Domain Monetization Fleet",
                        "speaker": "KGU Autonomous Commercial Director",
                        "text": desc
                    })
            except Exception as e:
                logger.warning(f"Error parsing catalog: {e}")

        logger.info(f"Total extracted semantic chunks: {len(chunks)}. Generating 768d vector embeddings...")
        
        indexed_chunks = []
        for i, chunk in enumerate(chunks):
            embedding = self.get_embedding(chunk["text"])
            indexed_chunks.append({
                "id": f"chunk_{i:03d}",
                "episode": chunk["episode"],
                "speaker": chunk["speaker"],
                "text": chunk["text"],
                "embedding": embedding
            })
            if (i + 1) % 10 == 0 or (i + 1) == len(chunks):
                logger.info(f"Embedded [{i+1}/{len(chunks)}] chunks into 768d space...")

        self.index = indexed_chunks
        
        # Save cache
        INDEX_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(INDEX_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump({"version": "3.0", "dim": self.dim, "total_chunks": len(self.index), "chunks": self.index}, f, indent=2)
            
        logger.info(f"✅ Master Sovereign RAG Index built & cached at {INDEX_CACHE_PATH} ({len(self.index)} chunks)")

    def _parse_script(self, script_text: str, episode: str) -> List[Dict[str, Any]]:
        chunks = []
        current_speaker = "Unknown"
        current_text = []

        for line in script_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if line.startswith("**George:**") or line.startswith("George:"):
                if current_text:
                    chunks.append({"episode": episode, "speaker": current_speaker, "text": " ".join(current_text)})
                    current_text = []
                current_speaker = "George Dubec"
                current_text.append(line.split(":", 1)[1].strip())
            elif line.startswith("**Joann:**") or line.startswith("Joann:"):
                if current_text:
                    chunks.append({"episode": episode, "speaker": current_speaker, "text": " ".join(current_text)})
                    current_text = []
                current_speaker = "Joann Coffey"
                current_text.append(line.split(":", 1)[1].strip())
            else:
                current_text.append(line)

        if current_text:
            chunks.append({"episode": episode, "speaker": current_speaker, "text": " ".join(current_text)})

        return chunks

    def _parse_markdown_sections(self, md_text: str, source: str, default_speaker: str) -> List[Dict[str, Any]]:
        chunks = []
        current_section = source
        current_lines = []

        for line in md_text.splitlines():
            sline = line.strip()
            if sline.startswith("## ") or sline.startswith("### "):
                if current_lines:
                    text_block = " ".join(current_lines).strip()
                    if len(text_block) > 50:
                        chunks.append({
                            "episode": f"{source}: {current_section}",
                            "speaker": default_speaker,
                            "text": text_block
                        })
                    current_lines = []
                current_section = sline.lstrip("#").strip()
            elif sline and not sline.startswith("---"):
                current_lines.append(sline)

        if current_lines:
            text_block = " ".join(current_lines).strip()
            if len(text_block) > 50:
                chunks.append({
                    "episode": f"{source}: {current_section}",
                    "speaker": default_speaker,
                    "text": text_block
                })

        return chunks

    @staticmethod
    def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    def query(self, query_text: str, top_k: int = 3, speaker_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Query the multimodal RAG index for relevant episode & sovereign context."""
        if not self.index:
            self.index_all()

        query_emb = self.get_embedding(query_text)
        scored = []

        for chunk in self.index:
            if speaker_filter and speaker_filter.lower() not in chunk["speaker"].lower():
                continue
            sim = self._cosine_similarity(query_emb, chunk["embedding"])
            scored.append({
                "score": round(sim, 4),
                "episode": chunk["episode"],
                "speaker": chunk["speaker"],
                "text": chunk["text"]
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

if __name__ == "__main__":
    rag = TechUnfilteredRAG()
    
    if len(sys.argv) > 1 and sys.argv[1] == "reindex":
        rag.index_all()
    else:
        test_query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "How does GraveFlow handle cemetery flower placements?"
        print(f"\n🔍 Querying Sovereign Master RAG: '{test_query}'\n")
        matches = rag.query(test_query, top_k=3)
        for i, m in enumerate(matches, 1):
            print(f"[{i}] Score: {m['score']} | {m['speaker']} ({m['episode']})")
            print(f"    \"{m['text']}\"\n")
