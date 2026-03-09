# Cognisolve 🧠
### Confusion-Aware Adaptive Learning System (CAALS)
**Team Data Dragons | AWS AI for Bharat Hackathon**

> *"We don't just explain concepts — we explain confusion."*

---

## What Is Cognisolve?

Most AI tutors give generic explanations. Cognisolve **diagnoses WHY a learner is stuck** before explaining anything. It classifies the type of confusion, selects the optimal explanation strategy, generates a personalized response, and reinforces understanding with targeted practice questions.

---

## Live Demo

| | |
|---|---|
| **API Docs** | `https://32.192.6.18/api/docs` |
| **Cloud** | AWS EC2 (ap-south-1) |
| **LLM** | Google Gemma 3 12B via AWS Bedrock |

> Note: Uses a self-signed SSL certificate — click **Advanced → Proceed** on first visit.

---

## Repository Structure

```
Cognisolve/
├── frontend/          # Kotlin Multiplatform (Compose for Web)
├── backend/           # Python FastAPI backend
│   ├── main.py
│   ├── api/routes/    # explain.py, practice.py
│   ├── core/          # confusion_detector, strategy_selector, explanation_generator
│   ├── prompts/       # LLM prompt templates per strategy
│   ├── models/        # Pydantic schemas and enums
│   ├── services/      # llm_client.py (AWS Bedrock)
│   └── memory/        # Per-learner session tracking
├── design.md
├── requirements.md
└── README.md
```

---

## How It Works

```
User Input (concept + doubt + code)
        ↓
Confusion Diagnosis (LLM classifies confusion type)
        ↓
Strategy Selection (maps confusion → best explanation style)
        ↓
Adaptive Explanation (LLM generates personalized explanation)
        ↓
Micro-Practice Questions (targeted Q&A to verify understanding)
        ↓
Feedback Loop (re-explain if still confused)
```

---

## Confusion Types & Strategies

| Confusion Type | Meaning | Strategy |
|---------------|---------|----------|
| `conceptual` | Doesn't understand what it IS | Analogy-based |
| `procedural` | Can't apply the steps | Step-by-step walkthrough |
| `abstraction_gap` | Can't see the big picture | Intuition-first |
| `misconception` | Has a wrong mental model | Simplified rephrasing |
| `transfer` | Can't apply to new situations | Code-first |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Kotlin Multiplatform (Compose for Web) |
| Backend | Python, FastAPI |
| LLM | Google Gemma 3 12B |
| Cloud | AWS EC2, AWS Bedrock |
| Web Server | Nginx (reverse proxy + SSL) |
| Process Manager | PM2 |

---

## API Reference

### `POST /api/explain`
Full pipeline: detect confusion → select strategy → generate explanation.

**Request:**
```json
{
  "concept": "recursion",
  "user_doubt": "I don't understand why the function calls itself. Won't it go on forever?",
  "code_snippet": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)",
  "difficulty_level": "beginner",
  "learner_id": "user_001"
}
```

**Response:**
```json
{
  "concept": "recursion",
  "confusion_type": "misconception",
  "strategy_used": "simplified_rephrasing",
  "explanation": "This is a very common belief, but recursion doesn't go on forever because...",
  "analogy": "Think of it like a set of Russian dolls...",
  "key_insight": "Every recursive function must have a base case that stops the recursion.",
  "common_mistake": "Forgetting the base case causes infinite recursion.",
  "follow_up_hint": "Try tracing through factorial(3) step by step."
}
```

### `POST /api/explain/diagnose`
Diagnose confusion type only (no explanation generated).

### `POST /api/practice`
Generate targeted micro-practice questions based on confusion type.

### `POST /api/practice/feedback`
Submit a learner's answer and receive evaluated feedback.

---

## Local Development

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Add your AWS credentials
python main.py
# → http://localhost:8000/docs

---

## Deployment

### Backend (AWS EC2)

```bash
# SSH into EC2
ssh -i "ai-tutor-key.pem" ec2-user@32.192.6.18

# Manage the app with PM2
pm2 status
pm2 logs ai-tutor
pm2 restart ai-tutor

# Update code after changes
scp -i "ai-tutor-key.pem" -r ./backend ec2-user@32.192.6.18:~/backend
pm2 restart ai-tutor
```


# Upload
scp -i "ai-tutor-key.pem" -r build/dist/js/productionExecutable/ ec2-user@32.192.6.18:~/frontend

# Nginx serves it automatically at https://32.192.6.18

---

## Expected Impact

- Faster learning and better conceptual clarity
- Reduced learner frustration
- Improved self-learning for technical students
- Scalable to any programming or STEM concept

## Future Enhancements

- Per-user learning memory (Vector DB)
- Multilingual explanations (Hindi, Tamil, Bengali, etc.)
- Voice-based interaction
- Subject-specific fine-tuning
- Integration with platforms like LeetCode, Coursera

---

## Team

**Team Data Dragons** — AWS AI for Bharat Hackathon
- Team Leader: Harsh Kumar
- Track: Student Track — AI for Learning and Developer Productivity