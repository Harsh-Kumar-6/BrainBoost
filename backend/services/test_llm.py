"""
Quick test to verify your LLM client is working.
Run from the project root: python test_llm.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from llm_client import call_llm, call_llm_json

print("=" * 50)
print("Testing LLM Client")
print(f"Provider : {os.getenv('LLM_PROVIDER', 'openai')}")
print(f"Model    : {os.getenv('LLM_MODEL', 'gpt-4o-mini')}")
print("=" * 50)

# ── Test 1: Plain text response ────────────────────────────────
print("\n[Test 1] Plain text call...")
try:
    response = call_llm("Say hello in one sentence.", json_mode=False)
    print(f"✅ Success: {response}")
except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

# ── Test 2: JSON response ──────────────────────────────────────
print("\n[Test 2] JSON response call...")
try:
    response = call_llm_json(
        'Return a JSON object with keys "status" and "message". Status should be "ok".'
    )
    print(f"✅ Success: {response}")
    assert response.get("status") == "ok", "Expected status: ok"
except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

# ── Test 3: Simulate confusion detection ──────────────────────
print("\n[Test 3] Simulated confusion detection...")
try:
    response = call_llm_json("""
A student says: "I don't understand what recursion is."
Classify their confusion. Respond ONLY with JSON:
{"confusion_type": "conceptual", "confidence": 0.95, "reasoning": "short reason"}
""")
    print(f"✅ Success: {response}")
    assert "confusion_type" in response
except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

print("\n" + "=" * 50)
print("✅ All tests passed! LLM client is working.")
print("=" * 50)