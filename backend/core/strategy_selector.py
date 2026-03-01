"""
Strategy Selector — maps confusion type to the best explanation strategy.
Also loads the corresponding prompt template.
"""

import logging
from pathlib import Path

from models.confusion_types import ConfusionType, ExplanationStrategy, CONFUSION_STRATEGY_MAP

logger = logging.getLogger(__name__)

_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

# Map strategy → prompt filename
_STRATEGY_PROMPT_FILES: dict[ExplanationStrategy, str] = {
    ExplanationStrategy.ANALOGY:       "analogy_based.txt",
    ExplanationStrategy.STEP_BY_STEP:  "step_by_step.txt",
    ExplanationStrategy.INTUITION_FIRST: "intuition_first.txt",
    ExplanationStrategy.CODE_FIRST:    "code_first.txt",
    ExplanationStrategy.VISUAL_REASONING: "intuition_first.txt",  # fallback to intuition
    ExplanationStrategy.SIMPLIFIED:    "simplified_rephrasing.txt",
}

# Cache loaded templates
_template_cache: dict[ExplanationStrategy, str] = {}


def select_strategy(confusion_type: ConfusionType) -> ExplanationStrategy:
    """
    Return the best explanation strategy for a given confusion type.

    Args:
        confusion_type: The diagnosed confusion type

    Returns:
        ExplanationStrategy enum value
    """
    strategy = CONFUSION_STRATEGY_MAP.get(confusion_type, ExplanationStrategy.STEP_BY_STEP)
    logger.info(f"Strategy selected: {strategy} for confusion: {confusion_type}")
    return strategy


def load_prompt_template(strategy: ExplanationStrategy) -> str:
    """
    Load and return the prompt template for the given strategy.
    Templates are cached after first load.

    Args:
        strategy: The explanation strategy to load the prompt for

    Returns:
        Raw prompt template string (with {placeholders} for .format())
    """
    if strategy in _template_cache:
        return _template_cache[strategy]

    filename = _STRATEGY_PROMPT_FILES.get(strategy, "step_by_step.txt")
    template_path = _PROMPTS_DIR / filename

    if not template_path.exists():
        logger.error(f"Prompt file not found: {template_path}")
        raise FileNotFoundError(f"Prompt template missing: {filename}")

    template = template_path.read_text(encoding="utf-8")
    _template_cache[strategy] = template
    logger.debug(f"Loaded prompt template: {filename}")
    return template


def get_strategy_description(strategy: ExplanationStrategy) -> str:
    """Human-readable description of what each strategy does."""
    descriptions = {
        ExplanationStrategy.ANALOGY: "Explains using real-world analogies to build mental models",
        ExplanationStrategy.STEP_BY_STEP: "Breaks down the concept into numbered, sequential steps",
        ExplanationStrategy.INTUITION_FIRST: "Builds intuition by explaining the 'why' before the 'how'",
        ExplanationStrategy.CODE_FIRST: "Uses concrete code examples to derive the concept",
        ExplanationStrategy.VISUAL_REASONING: "Uses visual/spatial reasoning to explain relationships",
        ExplanationStrategy.SIMPLIFIED: "Corrects misconceptions and rephrases with accurate mental model",
    }
    return descriptions.get(strategy, "Adaptive explanation")