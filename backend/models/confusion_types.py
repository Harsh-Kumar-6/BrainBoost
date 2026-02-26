"""
This file tells the type of confusion that we will be diagnosing in our system.
And the explanation strategy that we will be using for each type of confusion.
"""

from enum import Enum

class ConfusionType(str, Enum):
    CONCEPTUAL = "conceptual"
    PROCEDURAL = "procedural"
    ABSTRACTION_GAP = "abstraction_gap"
    MISCONCEPTION = "misconception"
    TRANSFER = "transfer"
    UNKNOWN = "unknown"

class ExplanationStrategy(str, Enum):
    ANALOGY = "analogy_based"
    STEP_BY_STEP = "step_by_step"
    INTUITION_FIRST = "intuition_first"
    CODE_FIRST = "code_first"
    VISUAL_REASONING = "visual_reasoning"
    SIMPLIFIED = "simplified_rephrasing"

# Mapping of confusion types to explanation strategies
CONFUSION_STRATEGY_MAP: dict[ConfusionType, ExplanationStrategy] = {
    ConfusionType.CONCEPTUAL: ExplanationStrategy.ANALOGY,
    ConfusionType.PROCEDURAL: ExplanationStrategy.STEP_BY_STEP,
    ConfusionType.ABSTRACTION_GAP: ExplanationStrategy.INTUITION_FIRST,
    ConfusionType.MISCONCEPTION: ExplanationStrategy.CODE_FIRST,
    ConfusionType.TRANSFER: ExplanationStrategy.VISUAL_REASONING,
    ConfusionType.UNKNOWN: ExplanationStrategy.SIMPLIFIED,
}