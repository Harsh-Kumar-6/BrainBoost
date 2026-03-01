"""
Confusion Detector — analyzes learner input to classify confusion type.
Uses the LLM with a structured prompt to return a DiagnosisResult.
"""

import logging
from pathlib import Path

from models.confusion_types import ConfusionType
from models.schemas import DiagnosisResult
from services.llm_client import call_llm_json, LLMError

logger = logging.getLogger(__name__)

# Load prompt template once at startup
_BASE_DIR = Path(__file__).resolve().parent.parent
_PROMPT_PATH = _BASE_DIR / "prompts" / "confusion_detection.txt"
_PROMPT_TEMPLATE = _PROMPT_PATH.read_text(encoding="utf-8")


def detect_confusion(
    concept: str,
    user_doubt: str,
    code_snippet: str | None = None,
) -> DiagnosisResult:
    """
    Classify the type of confusion a learner is experiencing.

    Args:
        concept:      The topic being studied (e.g., "recursion")
        user_doubt:   Raw text of what the learner said/typed
        code_snippet: Optional code the learner is confused about

    Returns:
        DiagnosisResult with confusion_type, confidence, and reasoning
    """
    code_context = f"Code:\n```\n{code_snippet}\n```" if code_snippet else "No code provided."

    prompt = _PROMPT_TEMPLATE.format(
        concept=concept,
        user_doubt=user_doubt,
        code_snippet=code_context,
    )

    try:
        data = call_llm_json(prompt)
        confusion_type = _safe_parse_confusion_type(data.get("confusion_type", "unknown"))
        confidence = float(data.get("confidence", 0.7))
        reasoning = data.get("reasoning", "Unable to determine reasoning.")

        result = DiagnosisResult(
            confusion_type=confusion_type,
            confidence=min(max(confidence, 0.0), 1.0),  # clamp to [0,1]
            reasoning=reasoning,
        )
        logger.info(f"Confusion diagnosed: {result.confusion_type} (confidence={result.confidence:.2f})")
        return result

    except LLMError as e:
        logger.warning(f"LLM failed for confusion detection, defaulting to UNKNOWN: {e}")
        return DiagnosisResult(
            confusion_type=ConfusionType.UNKNOWN,
            confidence=0.0,
            reasoning="Could not diagnose confusion type due to an error.",
        )


def _safe_parse_confusion_type(value: str) -> ConfusionType:
    """Parse string to ConfusionType enum, defaulting to UNKNOWN."""
    try:
        return ConfusionType(value.lower().strip())
    except ValueError:
        logger.warning(f"Unknown confusion type from LLM: '{value}', defaulting to UNKNOWN")
        return ConfusionType.UNKNOWN