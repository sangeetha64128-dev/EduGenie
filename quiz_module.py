from typing import Any, Dict, List
import json
import re

from gemini_service import generate_text


def _extract_json(text: str) -> Dict[str, Any]:
    """
    Extract JSON from an AI response.
    Handles responses wrapped in ```json ... ``` blocks.
    """
    text = text.strip()

    # Remove markdown code fences
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find the JSON object inside the response
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)

        if match:
            return json.loads(match.group(0))

        raise ValueError("The AI returned invalid JSON.")


def generate_quiz(
    topic: str,
    difficulty: str = "medium",
    number_of_questions: int = 5,
) -> Dict[str, Any]:
    """
    Generate a multiple-choice quiz using the configured AI service.
    """

    # Keep the number of questions within a reasonable range.
    number_of_questions = max(1, min(number_of_questions, 20))

    prompt = f"""
You are an educational quiz generator.

Create a quiz for a student.

Topic: {topic}
Difficulty: {difficulty}
Number of questions: {number_of_questions}

Requirements:
1. Create exactly {number_of_questions} questions.
2. Each question must have exactly four options.
3. Each question must have exactly one correct answer.
4. Options should be plausible and related to the topic.
5. Do not make the correct answer obvious because of its length.
6. Include a short explanation for the correct answer.
7. Return ONLY valid JSON.
8. Do not use Markdown or code fences.

Use this exact JSON structure:

{{
  "topic": "{topic}",
  "difficulty": "{difficulty}",
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_answer": "Option A",
      "explanation": "Short explanation"
    }}
  ]
}}
"""

    response = generate_text(prompt)

    quiz = _extract_json(response)

    # Basic validation
    if "questions" not in quiz:
        raise ValueError("Quiz response does not contain questions.")

    if len(quiz["questions"]) != number_of_questions:
        raise ValueError(
            f"Expected {number_of_questions} questions, "
            f"but received {len(quiz['questions'])}."
        )

    for index, question in enumerate(quiz["questions"], start=1):
        if not isinstance(question, dict):
            raise ValueError(f"Question {index} is invalid.")

        required_fields = [
            "question",
            "options",
            "correct_answer",
            "explanation",
        ]

        for field in required_fields:
            if field not in question:
                raise ValueError(
                    f"Question {index} is missing '{field}'."
                )

        if len(question["options"]) != 4:
            raise ValueError(
                f"Question {index} must have exactly 4 options."
            )

        if question["correct_answer"] not in question["options"]:
            raise ValueError(
                f"Question {index} has an invalid correct answer."
            )

    return quiz


def check_answer(
    question: Dict[str, Any],
    user_answer: str,
) -> Dict[str, Any]:
    """
    Check a student's answer to one quiz question.
    """

    correct_answer = question.get("correct_answer")

    is_correct = (
        user_answer.strip().lower()
        == str(correct_answer).strip().lower()
    )

    return {
        "correct": is_correct,
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "explanation": question.get(
            "explanation",
            "No explanation is available.",
        ),
    }


def calculate_score(
    questions: List[Dict[str, Any]],
    answers: List[str],
) -> Dict[str, Any]:
    """
    Calculate the student's quiz score.
    """

    if len(answers) != len(questions):
        raise ValueError(
            "The number of answers must match the number of questions."
        )

    score = 0
    results = []

    for question, answer in zip(questions, answers):
        result = check_answer(question, answer)

        if result["correct"]:
            score += 1

        results.append(result)

    total = len(questions)

    percentage = (
        round((score / total) * 100, 2)
        if total > 0
        else 0
    )

    return {
        "score": score,
        "total": total,
        "percentage": percentage,
        "results": results,
    }