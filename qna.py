from typing import Dict, Any, List
import re
import json

from gemini_service import generate_text


def answer_question(
    question: str,
    context: str = "",
) -> Dict[str, Any]:
    """
    Answer a student's question using the AI service.

    If context is provided, the answer is based primarily
    on that context.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    question = question.strip()

    if context:
        context = context.strip()

        prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question using the provided learning material.

Student question:
{question}

Learning material:
{context}

Requirements:
1. Give a clear and accurate answer.
2. Explain the answer in student-friendly language.
3. Use the learning material as the primary source.
4. Do not invent information that is not supported by the material.
5. If the material does not contain enough information, clearly say so.
6. Include a short explanation.
7. Return ONLY valid JSON.
8. Do not use Markdown code fences.

Use this exact JSON structure:

{{
  "question": "{question}",
  "answer": "Answer to the student's question.",
  "explanation": "Short explanation of the answer.",
  "key_points": [
    "Important point 1",
    "Important point 2"
  ]
}}
"""
    else:
        prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the following student's question:

{question}

Requirements:
1. Give a clear and accurate educational answer.
2. Use simple language appropriate for a student.
3. Explain important concepts rather than giving only a one-line answer.
4. Do not invent facts.
5. Include a short explanation.
6. Return ONLY valid JSON.
7. Do not use Markdown code fences.

Use this exact JSON structure:

{{
  "question": "{question}",
  "answer": "Answer to the student's question.",
  "explanation": "Short explanation of the answer.",
  "key_points": [
    "Important point 1",
    "Important point 2"
  ]
}}
"""

    response = generate_text(prompt)

    result = _extract_json(response)

    _validate_response(result)

    return result


def _extract_json(text: str) -> Dict[str, Any]:
    """
    Extract a JSON object from the AI response.
    """

    if not text or not text.strip():
        raise ValueError("AI returned an empty response.")

    text = text.strip()

    # Remove Markdown JSON code fences.
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    # Try parsing the complete response.
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try finding a JSON object within the response.
    match = re.search(
        r"\{.*\}",
        text,
        flags=re.DOTALL,
    )

    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError("The AI returned invalid JSON.")


def _validate_response(result: Dict[str, Any]) -> None:
    """
    Validate the structure returned by the AI.
    """

    required_fields = [
        "question",
        "answer",
        "explanation",
        "key_points",
    ]

    for field in required_fields:
        if field not in result:
            raise ValueError(
                f"AI response is missing '{field}'."
            )

    if not isinstance(result["answer"], str):
        raise ValueError("Answer must be a string.")

    if not isinstance(result["explanation"], str):
        raise ValueError("Explanation must be a string.")

    if not isinstance(result["key_points"], list):
        raise ValueError("key_points must be a list.")


def get_simple_answer(
    question: str,
    context: str = "",
) -> str:
    """
    Return only the answer text.
    """

    result = answer_question(
        question=question,
        context=context,
    )

    return result["answer"]


def get_explanation(
    question: str,
    context: str = "",
) -> str:
    """
    Return only the explanation.
    """

    result = answer_question(
        question=question,
        context=context,
    )

    return result["explanation"]


def get_key_points(
    question: str,
    context: str = "",
) -> List[str]:
    """
    Return the important points related to the answer.
    """

    result = answer_question(
        question=question,
        context=context,
    )

    return result["key_points"]