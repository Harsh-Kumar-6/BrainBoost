from pydantic import BaseModel, Field
from typing import List, Optional
from models.confusion_types import ConfusionType, ExplanationStrategy    

# ── Request Models ──────────────────────────────────────────────

class ExplainRequest(BaseModel):
    concept: str = Field(..., description="The topic/concept the learner is studying")
    user_doubt: str = Field(..., description="What the learner typed - their confusion or question")
    code_snippet: Optional[str] = Field(None, description="Optional code snippet if the doubt is related to programming")
    difficulty_level: Optional[str] = Field("beginner", description="beginner | intermediate | advanced")
    learner_id: Optional[str] = Field(None, description="optional id to track learner")

    class Config:
        schema_extra = {
            "example": {
                "concept": "Recursion",
                "user_doubt": "I don't understand how the base case works in recursion.",
                "code_snippet": None,
                "difficulty_level": "beginner",
                "learner_id": "learner_123"
            }
        }

class PracticeRequest(BaseModel):
    concept: str
    confusion_type: ConfusionType
    explanation_given: str = Field(..., description="The explanation that was given to the learner")
    difficulty_level: Optional[str] = Field("beginner", description="beginner | intermediate | advanced")
    num_questions: Optional[int] = Field(2, ge=1, le=5)

    class Config:
        schema_extra = {
            "example": {
                "concept": "Recursion",
                "confusion_type": "conceptual",
                "explanation_given": "Recursion is like a function calling itself with simpler inputs until it reaches a base case.",
                "difficulty_level": "beginner",
                "num_questions": 3
            }
        }

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
    key_insights: str
    common_mistake: Optional[str] = None
    follow_up_hint: Optional[str] = None

class PracticeQuestion(BaseModel):
    question_id: int
    question: str
    question_type: str  # e.g., "mcq", "coding", "short_answer"
    options: Optional[List[str]] = None  # for MCQs
    correct_answer: Optional[str] = None  # for auto-grading coding/short answer
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
    encouragement: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str