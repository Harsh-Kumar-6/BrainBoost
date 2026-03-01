"""
End-to-end API test — runs against the live server.
Make sure python main.py is running before executing this.

Run: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def print_section(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print('='*55)


def print_result(response):
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"❌ Error {response.status_code}: {response.text}")


# ── Test 1: Health Check ───────────────────────────────────────
print_section("Test 1: Health Check")
r = requests.get(f"{BASE_URL}/health")
if r.status_code == 200:
    print(f"✅ Server is up: {r.json()}")
else:
    print(f"❌ Server not reachable. Is main.py running?")
    exit(1)


# ── Test 2: Full Explain Pipeline ─────────────────────────────
print_section("Test 2: Explain — Conceptual Confusion")
r = requests.post(f"{BASE_URL}/explain", json={
    "concept": "recursion",
    "user_doubt": "I don't understand why the function calls itself. Won't it go on forever?",
    "code_snippet": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)",
    "difficulty_level": "beginner",
    "learner_id": "test_user_001"
})
print_result(r)


# ── Test 3: Diagnose Only ──────────────────────────────────────
print_section("Test 3: Diagnose Confusion Type Only")
r = requests.post(f"{BASE_URL}/explain/diagnose", json={
    "concept": "pointers in C",
    "user_doubt": "I know what a pointer is but I keep getting segfaults when I use them",
    "difficulty_level": "intermediate"
})
print_result(r)


# ── Test 4: Practice Questions ────────────────────────────────
print_section("Test 4: Generate Practice Questions")
r = requests.post(f"{BASE_URL}/practice", json={
    "concept": "recursion",
    "confusion_type": "conceptual",
    "explanation_given": "Think of recursion like Russian dolls — each doll contains a smaller version of itself. Every recursive function must have a base case that stops the recursion.",
    "difficulty_level": "beginner",
    "num_questions": 2
})
print_result(r)


# ── Test 5: Answer Feedback ───────────────────────────────────
print_section("Test 5: Submit Answer & Get Feedback")
r = requests.post(f"{BASE_URL}/practice/feedback", json={
    "learner_id": "test_user_001",
    "concept": "recursion",
    "question": "What is the purpose of a base case in recursion?",
    "learner_answer": "The base case stops the recursion from going on forever",
    "correct_answer": "The base case is a condition that stops the recursive calls",
    "confusion_type": "conceptual"
})
print_result(r)


print(f"\n{'='*55}")
print("  All tests complete!")
print(f"{'='*55}\n")