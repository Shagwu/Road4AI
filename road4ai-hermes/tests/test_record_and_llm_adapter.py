import types
import pytest

from road4ai_hermes.adapter import LLMCapture
from road4ai_hermes.bridge import MemoryBridgeV2


class DummyResponse:
    def __init__(self, content: str):
        self.choices = [types.SimpleNamespace(message=types.SimpleNamespace(content=content))]


class DummyOpenAI:
    def __init__(self, response_text: str):
        self._text = response_text
        self.chat = types.SimpleNamespace(completions=types.SimpleNamespace(create=self._create))

    def _create(self, model: str, messages: list):
        return DummyResponse(self._text)


def test_record_conversation_calls_store_and_persist(monkeypatch):
    called = {}

    # Create a fake self for MemoryBridgeV2.record_conversation
    fake_self = types.SimpleNamespace()

    def fake_store(text, vector, metadata=None, expires_at=None, ttl_seconds=None):
        called['store'] = {'text': text, 'vector': vector, 'metadata': metadata}
        return 'fake-id-123'

    def fake_ensure_persist():
        called['persist'] = True

    fake_self.store = fake_store
    fake_self.ensure_persist = fake_ensure_persist

    # Call the unbound method with provided vector to avoid embedding dependency
    mem_id = MemoryBridgeV2.record_conversation(fake_self, user_input='hi', ai_output='hello', model='gpt-test', vector=[0.1, 0.2, 0.3])

    assert mem_id == 'fake-id-123'
    assert 'store' in called
    assert called['store']['metadata']['type'] == 'conversation'
    assert called['store']['metadata']['provenance']['model'] == 'gpt-test'
    assert called.get('persist') is True


def test_llm_adapter_calls_bridge_record_conversation(monkeypatch):
    # Dummy openai client that returns a predictable assistant reply
    openai = DummyOpenAI('assistant reply')

    recorded = {}

    class FakeBridge:
        def record_conversation(self, user_input, ai_output, model=None, metadata=None, vector=None, expires_at=None, ttl_seconds=None):
            recorded['user_input'] = user_input
            recorded['ai_output'] = ai_output
            recorded['model'] = model
            return 'bridge-id-xyz'

    bridge = FakeBridge()
    llm = LLMCapture(openai_client=openai, bridge=bridge)

    messages = [
        {"role": "user", "content": "What is the weather?"},
    ]

    assistant = llm.chat_completion(messages=messages, model='gpt-test')

    assert assistant == 'assistant reply'
    # Bridge should have been called with the combined user prompt and assistant output
    assert recorded['user_input'] == 'What is the weather?'
    assert recorded['ai_output'] == 'assistant reply'
    assert recorded['model'] == 'gpt-test'
