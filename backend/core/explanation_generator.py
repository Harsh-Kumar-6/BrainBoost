"""
Explanation Generator — builds the adaptive explanation using LLM.
"""

import logging

from models.confusion_types import ConfusionType
from models.schemas import ExplainResponse
from core.strategy_selector import select_strategy, load_prompt_template
from services.llm_client import call_llm_json, LLMError

logger = logging.getLogger(__name__)


def generate_explanation(
    concept: str,
    user_doubt: str,
    confusion_type: ConfusionType,
    code_snippet: str | None = None,
    difficulty_level: str = "beginner",
) -> ExplainResponse:

    strategy = select_strategy(confusion_type)
    template = load_prompt_template(strategy)

    code_context = (
        f"\nCode the learner is working with:\n```\n{code_snippet}\n```"
        if code_snippet
        else ""
    )

    prompt = template.format(
        concept=concept,
        user_doubt=user_doubt,
        code_context=code_context,
        difficulty_level=difficulty_level,
    )

    # Raise error directly — do NOT silently fallback so we can see what's wrong
    data = call_llm_json(prompt)

    return ExplainResponse(
        concept=concept,
        confusion_type=confusion_type,
        strategy_used=strategy,
        explanation=data.get("explanation", "No explanation generated."),
        analogy=data.get("analogy"),
        key_insight=data.get("key_insight") or data.get("key_insights") or "",
        common_mistake=data.get("common_mistake"),
        follow_up_hint=data.get("follow_up_hint"),
    )


def generate_explanation_full_pipeline(
    concept: str,
    user_doubt: str,
    code_snippet: str | None = None,
    difficulty_level: str = "beginner",
):
    from core.confusion_detector import detect_confusion

    diagnosis = detect_confusion(concept, user_doubt, code_snippet)
    explanation = generate_explanation(
        concept=concept,
        user_doubt=user_doubt,
        confusion_type=diagnosis.confusion_type,
        code_snippet=code_snippet,
        difficulty_level=difficulty_level,
    )
    return explanation, diagnosis