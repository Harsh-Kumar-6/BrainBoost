from pydantic import BaseModel, Field
from typing import Optional, List
from models.confusion_types import ConfusionType, ExplanationStrategy


# ── Request Models ──────────────────────────────────────────────

class ExplainRequest(BaseModel):
    concept: str = Field(..., description="The topic/concept the learner is studying")
    user_doubt: str = Field(..., description="What the learner typed — their confusion or question")
    code_snippet: Optional[str] = Field(None, description="Optional code the learner is confused about")
    difficulty_level: Optional[str] = Field("beginner", description="beginner | intermediate | advanced")
    learner_id: Optional[str] = Field(None, description="Optional ID to track learner session")

    class Config:
        json_schema_extra = {
            "example": {
                "concept": "recursion",
                "user_doubt": "I don't understand why the function calls itself. Won't it go on forever?",
                "code_snippet": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)",
                "difficulty_level": "beginner",
                "learner_id": "user_001"
            }
        }


class PracticeRequest(BaseModel):
    concept: str
    confusion_type: ConfusionType
    explanation_given: str = Field(..., description="The explanation that was already shown to the learner")
    difficulty_level: Optional[str] = Field("beginner")
    num_questions: Optional[int] = Field(2, ge=1, le=5)

    class Config:
        json_schema_extra = {
            "example": {
                "concept": "recursion",
                "confusion_type": "conceptual",
                "explanation_given": "Think of recursion like Russian dolls...",
                "difficulty_level": "beginner",
                "num_questions": 2
            }
        }


class FeedbackRequest(BaseModel):
    learner_id: str
    concept: str
    question: str
    learner_answer: str
    correct_answer: str
    confusion_type: ConfusionType


# ── Response Models ─────────────────────────────────────────────

class DiagnosisResult(BaseModel):
    confusion_type: ConfusionType
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str


class ExplainResponse(BaseModel):
    concept: str
    confusion_type: ConfusionType
    strategy_used: ExplanationStrategy
    explanation: str
    analogy: Optional[str] = None
    key_insight: Optional[str] = None
    common_mistake: Optional[str] = None
    follow_up_hint: Optional[str] = None


class PracticeQuestion(BaseModel):
    question_id: int
    question: str
    question_type: str  # "mcq" | "true_false" | "short_answer"
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: str


class PracticeResponse(BaseModel):
    concept: str
    confusion_type: ConfusionType
    questions: List[PracticeQuestion]


class FeedbackResponse(BaseModel):
    is_correct: bool
    score: float
    feedback_message: str
    re_explanation: Optional[str] = None
    encouragement: str


class HealthResponse(BaseModel):
    status: str
    version: str