"""
/explain endpoint — main explanation pipeline.
POST /explain → detect confusion → select strategy → generate explanation
"""

import logging
from fastapi import APIRouter, HTTPException, status

from models.schemas import ExplainRequest, ExplainResponse, DiagnosisResult
from core.confusion_detector import detect_confusion
from core.explanation_generator import generate_explanation
from memory.learner_memory import get_memory

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/explain", tags=["Explanation"])


@router.post(
    "",
    response_model=ExplainResponse,
    summary="Generate a confusion-aware explanation",
    description=(
        "Diagnoses the learner's confusion type, selects the optimal "
        "explanation strategy, and returns a personalized explanation."
    ),
)
async def explain_concept(request: ExplainRequest) -> ExplainResponse:
    """
    Full pipeline:
    1. Detect confusion type from learner input
    2. Select best explanation strategy
    3. Generate adaptive explanation
    4. Optionally store in learner memory
    """
    logger.info(f"Explain request: concept='{request.concept}', learner='{request.learner_id}'")

    try:
        # Step 1: Diagnose confusion
        diagnosis: DiagnosisResult = detect_confusion(
            concept=request.concept,
            user_doubt=request.user_doubt,
            code_snippet=request.code_snippet,
        )

        # Step 2 + 3: Generate explanation
        response: ExplainResponse = generate_explanation(
            concept=request.concept,
            user_doubt=request.user_doubt,
            confusion_type=diagnosis.confusion_type,
            code_snippet=request.code_snippet,
            difficulty_level=request.difficulty_level or "beginner",
        )

        # Step 4: Persist to learner memory (optional)
        memory = get_memory(request.learner_id)
        if memory:
            memory.record_session(
                concept=request.concept,
                confusion_type=diagnosis.confusion_type,
                strategy_used=response.strategy_used.value,
                explanation=response.explanation,
            )

        return response

    except Exception as e:
        logger.exception(f"Unexpected error in /explain: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate explanation: {str(e)}",
        )


@router.post(
    "/diagnose",
    response_model=DiagnosisResult,
    summary="Only diagnose confusion type (no explanation)",
    description="Useful for debugging or pre-fetching the diagnosis before generating an explanation.",
)
async def diagnose_only(request: ExplainRequest) -> DiagnosisResult:
    """Return only the confusion diagnosis without generating an explanation."""
    try:
        return detect_confusion(
            concept=request.concept,
            user_doubt=request.user_doubt,
            code_snippet=request.code_snippet,
        )
    except Exception as e:
        logger.exception(f"Error in /explain/diagnose: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )