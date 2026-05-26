"""Lightweight LLM wrapper that optionally captures conversations to Hermes v2 bridge.

This is a small utility intended to mirror Memori's "register client" auto-capture pattern.
It performs a chat completion using a provided OpenAI-like client, computes an embedding
(if sentence-transformers is available), and writes a conversation record to MemoryBridgeV2.

Usage (example):

from openai import OpenAI
from .bridge import MemoryBridgeV2
# Self import removed as it is now this file

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
bridge = MemoryBridgeV2()
llm = LLMCapture(openai_client=openai_client, bridge=bridge)
response = llm.chat_completion(messages=[{"role":"user","content":"Hello"}], model="gpt-4o-mini")

"""
from typing import Any, Dict, List, Optional

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None  # optional


class LLMCapture:
    def __init__(self, openai_client: Any, bridge: Any, embedding_model_name: str = "all-MiniLM-L6-v2"):
        self.openai_client = openai_client
        self.bridge = bridge
        self.embedding_model_name = embedding_model_name
        self._embed_model = None

    def _ensure_embed_model(self):
        if self._embed_model is None and SentenceTransformer is not None:
            try:
                self._embed_model = SentenceTransformer(self.embedding_model_name)
            except Exception:
                self._embed_model = None

    def _compute_embedding(self, text: str) -> Optional[List[float]]:
        self._ensure_embed_model()
        if self._embed_model is not None:
            return self._embed_model.encode(text).tolist()
        return None

    def chat_completion(self, messages: List[Dict[str, str]], model: str = "gpt-4o-mini", capture: bool = True, metadata: Dict[str, Any] | None = None) -> str:
        """Run a chat completion and optionally capture the conversation to Hermes bridge.

        - messages: list of role/content dicts as expected by openai-like clients
        - model: model id
        - capture: if True, attempt to store the conversation using bridge.record_conversation
        - metadata: optional metadata to attach

        Returns the assistant's content string.
        """
        # Call the underlying client
        resp = self.openai_client.chat.completions.create(model=model, messages=messages)
        assistant_content = resp.choices[0].message.content

        if capture:
            # Build a user_input summary and ai_output
            try:
                user_msgs = [m for m in messages if m.get("role") == "user"]
                user_input = "\n".join([m.get("content", "") for m in user_msgs]) or ""
                ai_output = assistant_content or ""

                # Try to compute embedding; if unavailable, let bridge.record_conversation attempt to compute
                vector = self._compute_embedding(user_input + "\n\n" + ai_output)

                try:
                    self.bridge.record_conversation(user_input=user_input, ai_output=ai_output, model=model, metadata=metadata or {}, vector=vector)
                except Exception:
                    # Swallow any persistence errors to avoid failing LLM call
                    pass
            except Exception:
                pass

        return assistant_content
