"""
LLM Client — Google Gemma via AWS Bedrock
"""

import os
import re
import json
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

LLM_MAX_TOKENS  = int(os.getenv("LLM_MAX_TOKENS", "1024"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.4"))


def call_llm(
    prompt: str,
    system_prompt: str = "You are a helpful AI tutor that diagnoses learner confusion and explains technical concepts.",
    json_mode: bool = True,
) -> str:
    import boto3

    if json_mode:
        prompt += "\n\nCRITICAL: Your response must start with '{' and end with '}'. Output ONLY the JSON object. No explanation, no markdown, no code fences."

    full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "ap-south-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    body = json.dumps({
        "messages": [{"role": "user", "content": full_prompt}],
        "max_tokens": LLM_MAX_TOKENS,
        "temperature": LLM_TEMPERATURE,
    })

    try:
        response = bedrock.invoke_model(
            body=body,
            modelId=os.getenv("BEDROCK_MODEL_ID", "google.gemma-3-12b-it"),
        )
        result = json.loads(response["body"].read())
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        raise LLMError(f"Bedrock call failed: {str(e)}") from e


def _extract_json(raw: str) -> str:
    """
    Robustly extract JSON from LLM output that may have extra text.
    Tries multiple strategies in order.
    """
    raw = raw.strip()

    # Strategy 1: Already clean JSON
    if raw.startswith("{") or raw.startswith("["):
        return raw

    # Strategy 2: Strip markdown code fences
    if "```" in raw:
        parts = raw.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{") or part.startswith("["):
                return part

    # Strategy 3: Find first { and last }
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        return raw[start:end + 1]

    # Strategy 4: Find first [ and last ]
    start = raw.find("[")
    end = raw.rfind("]")
    if start != -1 and end != -1 and end > start:
        return raw[start:end + 1]

    return raw


def call_llm_json(prompt: str, system_prompt: str = "") -> dict:
    raw = call_llm(prompt, system_prompt, json_mode=True)
    logger.debug(f"Raw LLM response: {raw[:300]}")
    try:
        cleaned = _extract_json(raw)
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM JSON: {raw}")
        raise LLMError(f"LLM returned invalid JSON: {str(e)}") from e


def call_llm_json_list(prompt: str, system_prompt: str = "") -> list:
    raw = call_llm(prompt, system_prompt, json_mode=True)
    logger.debug(f"Raw LLM response: {raw[:300]}")
    try:
        cleaned = _extract_json(raw)
        result = json.loads(cleaned)
        if isinstance(result, list):
            return result
        for v in result.values():
            if isinstance(v, list):
                return v
        raise LLMError("LLM response was not a JSON list")
    except json.JSONDecodeError as e:
        raise LLMError(f"LLM returned invalid JSON list: {str(e)}") from e


class LLMError(Exception):
    pass