"""
Learner Memory — persists learner context, confusion history, and progress.
Uses a simple JSON file store by default.
Can be swapped for DynamoDB, Redis, or a vector DB in production.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from models.confusion_types import ConfusionType

logger = logging.getLogger(__name__)

_MEMORY_DIR = Path(os.getenv("MEMORY_DIR", "/tmp/learner_memory"))
_MEMORY_DIR.mkdir(parents=True, exist_ok=True)


class LearnerMemory:
    """
    Stores and retrieves per-learner context:
    - Topics studied
    - Confusion types encountered
    - Concepts mastered vs struggling
    - Session history
    """

    def __init__(self, learner_id: str):
        self.learner_id = learner_id
        self._path = _MEMORY_DIR / f"{learner_id}.json"
        self._data = self._load()

    # ── Core CRUD ──────────────────────────────────────────────

    def _load(self) -> dict:
        if self._path.exists():
            try:
                return json.loads(self._path.read_text())
            except Exception:
                logger.warning(f"Corrupt memory file for {self.learner_id}, resetting")
        return {
            "learner_id": self.learner_id,
            "created_at": datetime.utcnow().isoformat(),
            "sessions": [],
            "concepts_seen": {},
            "confusion_counts": {},
            "mastered_concepts": [],
            "struggling_concepts": [],
        }

    def _save(self) -> None:
        self._path.write_text(json.dumps(self._data, indent=2))

    # ── Public Methods ─────────────────────────────────────────

    def record_session(
        self,
        concept: str,
        confusion_type: ConfusionType,
        strategy_used: str,
        explanation: str,
    ) -> None:
        """Log a learning interaction."""
        session = {
            "timestamp": datetime.utcnow().isoformat(),
            "concept": concept,
            "confusion_type": confusion_type.value,
            "strategy_used": strategy_used,
            "explanation_preview": explanation[:200],
        }
        self._data["sessions"].append(session)

        # Update concept tracking
        if concept not in self._data["concepts_seen"]:
            self._data["concepts_seen"][concept] = {"count": 0, "confusion_types": []}
        self._data["concepts_seen"][concept]["count"] += 1
        self._data["concepts_seen"][concept]["confusion_types"].append(confusion_type.value)

        # Update confusion frequency
        ct = confusion_type.value
        self._data["confusion_counts"][ct] = self._data["confusion_counts"].get(ct, 0) + 1

        self._save()
        logger.debug(f"Session recorded for learner {self.learner_id}: {concept}")

    def record_practice_result(
        self,
        concept: str,
        is_correct: bool,
        score: float,
    ) -> None:
        """Track how the learner performed on practice questions."""
        concept_data = self._data["concepts_seen"].get(concept, {})
        if "practice_scores" not in concept_data:
            concept_data["practice_scores"] = []
        concept_data["practice_scores"].append(score)

        # Auto-classify as mastered or struggling
        scores = concept_data.get("practice_scores", [])
        if len(scores) >= 3:
            avg = sum(scores[-3:]) / 3  # rolling average of last 3
            if avg >= 0.8 and concept not in self._data["mastered_concepts"]:
                self._data["mastered_concepts"].append(concept)
                if concept in self._data["struggling_concepts"]:
                    self._data["struggling_concepts"].remove(concept)
                logger.info(f"Learner {self.learner_id} mastered: {concept}")
            elif avg < 0.5 and concept not in self._data["struggling_concepts"]:
                self._data["struggling_concepts"].append(concept)

        self._data["concepts_seen"][concept] = concept_data
        self._save()

    def get_learner_context(self) -> dict:
        """Return a summary of the learner's history (for adaptive prompting)."""
        return {
            "total_sessions": len(self._data["sessions"]),
            "concepts_seen": list(self._data["concepts_seen"].keys()),
            "mastered": self._data["mastered_concepts"],
            "struggling": self._data["struggling_concepts"],
            "most_common_confusion": self._get_most_common_confusion(),
            "recent_concept": self._get_recent_concept(),
        }

    def get_recent_sessions(self, n: int = 3) -> list:
        """Get the n most recent sessions."""
        return self._data["sessions"][-n:]

    def clear(self) -> None:
        """Reset learner memory."""
        self._data = {
            "learner_id": self.learner_id,
            "created_at": datetime.utcnow().isoformat(),
            "sessions": [],
            "concepts_seen": {},
            "confusion_counts": {},
            "mastered_concepts": [],
            "struggling_concepts": [],
        }
        self._save()

    # ── Private Helpers ────────────────────────────────────────

    def _get_most_common_confusion(self) -> Optional[str]:
        counts = self._data["confusion_counts"]
        if not counts:
            return None
        return max(counts, key=counts.get)

    def _get_recent_concept(self) -> Optional[str]:
        sessions = self._data["sessions"]
        if not sessions:
            return None
        return sessions[-1].get("concept")


# ── Module-level convenience functions ────────────────────────

def get_memory(learner_id: str) -> Optional[LearnerMemory]:
    """Get learner memory if learner_id provided, else None."""
    if not learner_id:
        return None
    return LearnerMemory(learner_id)