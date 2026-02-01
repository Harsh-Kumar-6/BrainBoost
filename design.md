
# Explain Like I'm Stuck – Design Document

## 1. System Architecture Overview
The system follows a modular architecture that separates user interaction, AI reasoning, and feedback mechanisms.

## 2. High-Level Components
- Frontend (Web Interface)
- Backend Application Server
- AI/NLP Services
- Optional Data Storage

## 3. Module Descriptions

### 3.1 Frontend (Web Interface)
- Collects learner input
- Displays explanations and feedback
- Allows interaction with micro-practice questions

### 3.2 Input Processing Module
- Cleans and structures user input
- Prepares data for AI analysis

### 3.3 Confusion Diagnosis Module
- Uses NLP reasoning to classify confusion type
- Outputs a confusion category for downstream processing

### 3.4 Explanation Strategy Selector
- Maps confusion type to an explanation strategy
- Ensures explanations match learner needs

### 3.5 LLM-based Explanation Generator
- Generates adaptive explanations
- Adjusts tone, depth, and style

### 3.6 Micro-Practice Generator
- Creates short, focused questions
- Targets specific misunderstandings

### 3.7 Feedback Loop
- Evaluates learner responses
- Refines explanations
- Updates learner context

## 4. Data Flow
1. User submits input via frontend
2. Backend processes and diagnoses confusion
3. Explanation strategy is selected
4. AI generates explanation
5. Micro-practice questions are delivered
6. Learner feedback is analyzed
7. Explanation is refined if needed

## 5. External Dependencies
- LLM APIs for explanation generation
- Cloud infrastructure (AWS)
- Optional vector database for learner context

## 6. Design Considerations
- Keep AI components modular
- Maintain clarity and simplicity for student-level deployment
- Highlight AI decision points clearly
