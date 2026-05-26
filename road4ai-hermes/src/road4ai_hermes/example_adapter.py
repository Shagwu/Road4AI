"""Example adapter showing how to adapt a Memori-based social media agent to use Hermes v2.0

This lightweight example mirrors the twitter_agents patterns but uses MemoryBridgeV2
and LLMCapture to auto-capture LLM calls and provide a small MemoryTool adapter.

Run this file as a demonstration; it does not perform network calls.
"""
import os
from .bridge import MemoryBridgeV2
from .adapter import LLMCapture


def example_initialize_bridge():
    persist_dir = os.getenv("HERMES_PERSIST_DIR", "./chroma_db")
    collection = os.getenv("HERMES_COLLECTION", "twitter_style")
    bridge = MemoryBridgeV2(persist_directory=persist_dir, collection_name=collection)
    return bridge


class HermesMemoryTool:
    def __init__(self, bridge, embed_model_name: str = "all-MiniLM-L6-v2"):
        self.bridge = bridge
        try:
            from sentence_transformers import SentenceTransformer

            self.embed = SentenceTransformer(embed_model_name)
        except Exception:
            self.embed = None

    def execute(self, query: str):
        if self.embed is None:
            return None
        vec = self.embed.encode(query).tolist()
        results = self.bridge.search(query_vector=vec, k=1)
        if results:
            return results[0]["text"]
        return None


def demo():
    bridge = example_initialize_bridge()
    memory_tool = HermesMemoryTool(bridge)

    # Wrap OpenAI client (or any OpenAI-like client) with LLMCapture to auto-store LLM calls
    from types import SimpleNamespace

    # Dummy openai client for demo purposes
    openai = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=lambda model, messages: SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='demo reply'))]))))

    llm = LLMCapture(openai_client=openai, bridge=bridge)

    # Example usage: run a chat completion and let LLMCapture persist the conversation
    messages = [{"role":"user","content":"Write a tweet about Hermes v2"}]
    reply = llm.chat_completion(messages=messages, model="gpt-4o-mini")
    print("LLM reply:", reply)

    # Example retrieval via memory tool
    stored = memory_tool.execute("twitter style tone personality")
    print("Retrieved memory text:", stored)


if __name__ == '__main__':
    demo()
