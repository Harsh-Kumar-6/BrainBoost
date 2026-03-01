"""
Practice Generator — generates targeted micro-practice questions
based on the concept, confusion type, and explanation given.
"""

import logging
from pathlib import Path

from models.confusion_types import ConfusionType
from models.schemas import PracticeResponse, PracticeQuestion
from services.llm_client import call_llm_json_list, LLMError

logger = logging.getLogger(__name__)

_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "practice_questions.txt"
_PROMPT_TEMPLATE = _PROMPT_PATH.read_text(encoding="utf-8")


def generate_practice_questions(
    concept: str,
    confusion_type: ConfusionType,
    explanation_given: str,
    difficulty_level: str = "beginner",
    num_questions: int = 2,
) -> PracticeResponse:
    """
    Generate micro-practice questions to validate understanding.

    Args:
        concept:            The topic the learner is studying
        confusion_type:     The type of confusion that was diagnosed
        explanation_given:  The explanation already shown to the learner
        difficulty_level:   beginner | intermediate | advanced
        num_questions:      Number of questions to generate (1-5)

    Returns:
        PracticeResponse with list of targeted questions
    """
    num_questions = max(1, min(num_questions, 5))  # clamp to 1-5

    prompt = _PROMPT_TEMPLATE.format(
        concept=concept,
        confusion_type=confusion_type.value,
        explanation_given=explanation_given[:800],  # Truncate to avoid token overflow
        difficulty_level=difficulty_level,
        num_questions=num_questions,
    )

    try:
        raw_questions = call_llm_json_list(prompt)
        questions = [_parse_question(q, idx) for idx, q in enumerate(raw_questions, 1)]

        return PracticeResponse(
            concept=concept,
            confusion_type=confusion_type,
            questions=questions,
        )

    except LLMError as e:
        logger.error(f"Practice generation failed: {e}")
        return PracticeResponse(
            concept=concept,
            confusion_type=confusion_type,
            questions=[_fallback_question(concept)],
        )


def evaluate_answer(
    question: str,
    correct_answer: str,
    learner_answer: str,
    concept: str,
) -> dict:
    """
    Evaluate a learner's answer and provide feedback.

    Returns dict with: is_correct, score, feedback_message, encouragement
    """
    from services.llm_client import call_llm_json

    prompt = f"""
A learner answered a practice question about "{concept}".

Question: {question}
Correct Answer: {correct_answer}
Learner's Answer: {learner_answer}

Evaluate the answer. Be encouraging and constructive.

Respond ONLY with valid JSON:
{{
  "is_correct": <true|false>,
  "score": <float 0.0-1.0>,
  "feedback_message": "<specific feedback on what they got right/wrong>",
  "re_explanation": "<if incorrect: a brief re-explanation of the key point, else null>",
  "encouragement": "<a short, warm encouraging message>"
}}
"""
    try:
        return call_llm_json(prompt)
    except LLMError:
        return {
            "is_correct": learner_answer.strip().lower() == correct_answer.strip().lower(),
            "score": 1.0 if learner_answer.strip().lower() == correct_answer.strip().lower() else 0.0,
            "feedback_message": "Could not evaluate answer automatically.",
            "re_explanation": None,
            "encouragement": "Keep practicing!",
        }


# ── Helpers ─────────────────────────────────────────────────────

def _parse_question(data: dict, idx: int) -> PracticeQuestion:
    """Safely parse a raw dict into a PracticeQuestion."""
    return PracticeQuestion(
        question_id=data.get("question_id", idx),
        question=data.get("question", "Question unavailable."),
        question_type=data.get("question_type", "short_answer"),
        options=data.get("options"),
        correct_answer=str(data.get("correct_answer", "")),
        explanation=data.get("explanation", ""),
    )


def _fallback_question(concept: str) -> PracticeQuestion:
    """Returns a generic fallback question when LLM fails."""
    return PracticeQuestion(
        question_id=1,
        question=f"In your own words, explain what '{concept}' means and give one example.",
        question_type="short_answer",
        options=None,
        correct_answer="Open-ended — focus on demonstrating understanding",
        explanation="This question checks if you can articulate the concept in your own words.",
    )