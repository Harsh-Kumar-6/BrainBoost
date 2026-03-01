"""
/practice endpoint — generate micro-practice questions + evaluate answers.
"""

import logging
from fastapi import APIRouter, HTTPException, status

from models.schemas import (
    PracticeRequest,
    PracticeResponse,
    FeedbackRequest,
    FeedbackResponse,
)
from core.practice_generator import generate_practice_questions, evaluate_answer
from memory.learner_memory import get_memory

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/practice", tags=["Practice"])


@router.post(
    "",
    response_model=PracticeResponse,
    summary="Generate micro-practice questions",
    description=(
        "Generates targeted practice questions based on the confusion type "
        "and the explanation already shown to the learner."
    ),
)
async def get_practice_questions(request: PracticeRequest) -> PracticeResponse:
    """
    Generate 1-5 micro-practice questions targeted at the diagnosed confusion type.
    """
    logger.info(f"Practice request: concept='{request.concept}', confusion='{request.confusion_type}'")

    try:
        return generate_practice_questions(
            concept=request.concept,
            confusion_type=request.confusion_type,
            explanation_given=request.explanation_given,
            difficulty_level=request.difficulty_level or "beginner",
            num_questions=request.num_questions or 2,
        )
    except Exception as e:
        logger.exception(f"Error in /practice: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/feedback",
    response_model=FeedbackResponse,
    summary="Evaluate a learner's answer and provide feedback",
)
async def submit_answer(request: FeedbackRequest) -> FeedbackResponse:
    """
    Evaluate the learner's answer against the correct answer.
    Returns feedback, score, and optional re-explanation if incorrect.
    """
    logger.info(f"Feedback request: concept='{request.concept}', learner='{request.learner_id}'")

    try:
        result = evaluate_answer(
            question=request.question,
            correct_answer=request.correct_answer,
            learner_answer=request.learner_answer,
            concept=request.concept,
        )

        # Record to learner memory
        memory = get_memory(request.learner_id)
        if memory:
            memory.record_practice_result(
                concept=request.concept,
                is_correct=result.get("is_correct", False),
                score=result.get("score", 0.0),
            )

        return FeedbackResponse(
            is_correct=result.get("is_correct", False),
            score=result.get("score", 0.0),
            feedback_message=result.get("feedback_message", ""),
            re_explanation=result.get("re_explanation"),
            encouragement=result.get("encouragement", "Keep going!"),
        )

    except Exception as e:
        logger.exception(f"Error in /practice/feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )