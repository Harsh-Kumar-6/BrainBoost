
# Explain Like I'm Stuck – Requirements Document

## 1. Overview
Explain Like I’m Stuck is an AI-powered learning assistant designed to help learners overcome conceptual confusion by identifying *why* they are stuck and adapting explanations accordingly.

## 2. Problem Statement
Learners often struggle not because information is unavailable, but because explanations do not align with their specific type of confusion. Existing AI tutors provide generic explanations and assume learners can precisely articulate their doubts.

## 3. Objectives
- Diagnose different types of learner confusion
- Provide adaptive, personalized explanations
- Validate understanding through micro-practice
- Refine explanations using a feedback loop

## 4. Target Users
- Students learning programming, DSA, or technical subjects
- Self-learners using online educational platforms
- Beginners trying to understand codebases or concepts

## 5. Functional Requirements
- Accept user input (concept, code, or question)
- Identify confusion type (conceptual, procedural, abstraction gap, misconception)
- Select an appropriate explanation strategy
- Generate adaptive explanations using AI
- Generate micro-practice questions
- Collect learner feedback and responses
- Refine explanations based on feedback

## 6. Non-Functional Requirements
- Low latency for responses
- Simple and intuitive user interface
- Scalable backend architecture
- Secure handling of user input

## 7. Assumptions & Constraints
- Uses pre-trained large language models
- Prototype-level system for hackathon
- Internet connectivity available
