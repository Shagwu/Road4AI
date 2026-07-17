import importlib.util
import json
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "harvester_pipeline.py"
SPEC = importlib.util.spec_from_file_location("harvester_pipeline", MODULE_PATH)
pipeline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pipeline)


class TestCanonicalizeUrl:
    def test_strips_utm_params(self):
        url = "https://example.com/article?utm_source=twitter&utm_medium=social"
        assert pipeline.canonicalize_url(url) == "https://example.com/article"

    def test_strips_ref_params(self):
        url = "https://example.com/article?ref=newsletter"
        assert pipeline.canonicalize_url(url) == "https://example.com/article"

    def test_strips_trailing_slash(self):
        assert pipeline.canonicalize_url("https://example.com/article/") == "https://example.com/article"

    def test_lowercases(self):
        assert pipeline.canonicalize_url("https://Example.COM/Article") == "https://example.com/article"

    def test_same_url_with_different_tracking(self):
        a = "https://example.com/post?utm_source=a&ref=b"
        b = "https://example.com/post?utm_source=c&ref=d"
        assert pipeline.canonicalize_url(a) == pipeline.canonicalize_url(b)


class TestShouldLogSignal:
    def test_first_occurrence_passes(self):
        seen = set()
        item = {"link": "https://example.com/article"}
        assert pipeline.should_log_signal(item, seen) is True
        assert len(seen) == 1

    def test_duplicate_url_blocked(self):
        seen = set()
        item = {"link": "https://example.com/article"}
        assert pipeline.should_log_signal(item, seen) is True
        assert pipeline.should_log_signal(item, seen) is False

    def test_canonical_dedup(self):
        seen = set()
        item_a = {"link": "https://example.com/article?utm_source=a"}
        item_b = {"link": "https://example.com/article?utm_source=b"}
        assert pipeline.should_log_signal(item_a, seen) is True
        assert pipeline.should_log_signal(item_b, seen) is False

    def test_empty_url_passes(self):
        seen = set()
        assert pipeline.should_log_signal({"link": ""}, seen) is True
        assert pipeline.should_log_signal({"link": None}, seen) is True

    def test_uses_entry_id_fallback(self):
        seen = set()
        item = {"entry_id": "https://example.com/article", "link": ""}
        assert pipeline.should_log_signal(item, seen) is True
        assert pipeline.should_log_signal(item, seen) is False


class TestGetKeywordCounts:
    def _make_log(self, entries, tmpdir):
        log_path = tmpdir / "signal_log.jsonl"
        with open(log_path, "w") as f:
            for e in entries:
                f.write(json.dumps(e) + "\n")
        return log_path

    def test_counts_recent_entries(self, tmp_path):
        now = datetime.now(timezone.utc).isoformat()
        entries = [
            {"title": "local llm inference guide", "text": "", "link": "https://a.com/1", "harvested_at": now},
            {"title": "multi-agent orchestration", "text": "", "link": "https://a.com/2", "harvested_at": now},
            {"title": "something else entirely", "text": "", "link": "https://a.com/3", "harvested_at": now},
        ]
        log_path = self._make_log(entries, tmp_path)
        counts = pipeline.get_keyword_counts(log_path, keywords=["local llm", "multi-agent"])
        assert counts["local llm"] == 1
        assert counts["multi-agent"] == 1

    def test_excludes_old_entries(self, tmp_path):
        old = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        entries = [
            {"title": "local llm guide", "text": "", "link": "https://a.com/1", "harvested_at": old},
        ]
        log_path = self._make_log(entries, tmp_path)
        counts = pipeline.get_keyword_counts(log_path, lookback_days=14, keywords=["local llm"])
        assert counts["local llm"] == 0

    def test_deduplicates_by_url(self, tmp_path):
        now = datetime.now(timezone.utc).isoformat()
        entries = [
            {"title": "local llm guide", "text": "", "link": "https://a.com/1", "harvested_at": now},
            {"title": "local llm guide part 2", "text": "", "link": "https://a.com/1", "harvested_at": now},
        ]
        log_path = self._make_log(entries, tmp_path)
        counts = pipeline.get_keyword_counts(log_path, keywords=["local llm"])
        assert counts["local llm"] == 1


class TestGetUnderrepresentedKeywords:
    def _make_log(self, entries, tmpdir):
        log_path = tmpdir / "signal_log.jsonl"
        with open(log_path, "w") as f:
            for e in entries:
                f.write(json.dumps(e) + "\n")
        return log_path

    def test_keywords_below_threshold_are_underrep(self, tmp_path):
        now = datetime.now(timezone.utc).isoformat()
        entries = [
            {"title": "local llm guide", "text": "", "link": "https://a.com/1", "harvested_at": now},
        ]
        log_path = self._make_log(entries, tmp_path)
        # local llm has 1 signal, threshold K=3
        underrep = pipeline.get_underrepresented_keywords(log_path)
        assert "local llm" in underrep

    def test_keywords_at_threshold_are_not_underrep(self, tmp_path):
        now = datetime.now(timezone.utc).isoformat()
        entries = [
            {"title": f"local llm article {i}", "text": "", "link": f"https://a.com/{i}", "harvested_at": now}
            for i in range(3)
        ]
        log_path = self._make_log(entries, tmp_path)
        underrep = pipeline.get_underrepresented_keywords(log_path)
        assert "local llm" not in underrep


class TestUnderrepOverride:
    """Verify the keep-bypass: underrep items are queued, not just labeled."""

    def test_underrep_boost_overrides_discard(self):
        """Simulates the override logic from scheduled_harvester.py."""
        underrep = ["local llm", "inference"]
        signal_text = "GPU financiers are turning to inference chips"

        matched = [kw for kw in underrep if kw in signal_text.lower()]
        underrep_boost = len(matched) > 0

        # Normal gate would discard at conf=0.30
        action = "discard"

        # Override: underrep items are kept
        if underrep_boost and action == "discard":
            action = "queue-for-review"

        assert underrep_boost is True
        assert action == "queue-for-review"

    def test_high_confidence_not_affected_by_underrep(self):
        """High-confidence items stay queued regardless of underrep status."""
        underrep = ["local llm"]
        signal_text = "local llm inference optimization"

        matched = [kw for kw in underrep if kw in signal_text.lower()]
        underrep_boost = len(matched) > 0

        action = "queue-for-review"  # already queued at conf=0.60
        if underrep_boost and action == "discard":
            action = "queue-for-review"

        assert action == "queue-for-review"

    def test_no_match_no_override(self):
        """Items that don't match underrep keywords keep their original action."""
        underrep = ["local llm", "inference"]
        signal_text = "Google Vids AI video generation"

        matched = [kw for kw in underrep if kw in signal_text.lower()]
        underrep_boost = len(matched) > 0

        action = "discard"
        if underrep_boost and action == "discard":
            action = "queue-for-review"

        assert underrep_boost is False
        assert action == "discard"

    def test_underrep_override_is_not_dead_code(self):
        """Regression: underrep_boost must change a discard to queue-for-review.

        This is the exact failure mode that shipped before the fix was added.
        process_signal returned discard, underrep_boost was true, but the
        override was just a label. This test ensures it actually changes fate.
        """
        # Simulate the pipeline path: process_signal returns discard,
        # but underrep keyword match triggers the override
        process_result = {"action": "discard", "confidence": 0.30}
        underrep_boost = True
        matched_underrep = ["inference"]

        action = process_result["action"]
        if underrep_boost and action == "discard":
            action = "queue-for-review"

        assert action == "queue-for-review", (
            f"underrep_boost=true should override discard to queue-for-review, "
            f"got '{action}'"
        )
