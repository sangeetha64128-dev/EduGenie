from typing import Dict, Any
import json
import re

from gemini_service import generate_text


def explain_topic(
    topic: str,
    level: str = "beginner",
    context: str = "",
) -> Dict[str, Any]:
    """
    Generate a student-friendly explanation of a topic.
    """

    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty.")

    topic = topic.strip()
    level = level.strip() or "beginner"

    if context:
        context = context.strip()

        prompt = f"""
You are EduGenie, an educational AI assistant.

Explain the following topic to a student.

Topic:
{topic}

Student level:
{level}

Learning material:
{context}

Requirements:
1. Explain the topic clearly and accurately.
2. Use language appropriate for the student's level.
3. Use the supplied learning material as the primary source.
4. Do not invent information that is not supported by the material.
5. Break difficult ideas into smaller steps.
6. Include a simple example when the material supports one.
7. Include the most important points.
8. If the material does not provide enough information, say so.
9. Return ONLY valid JSON.
10. Do not use Markdown code fences.

Use this exact JSON structure:

{{
  "topic": "{topic}",
  "level": "{level}",
  "explanation": "Clear explanation of the topic.",
  "key_points": [
    "Important point 1",
    "Important point 2",
    "Important point 3"
  ],
  "example": "A simple example related to the topic.",
  "quick_check": "A short question the student can use to check their understanding."
}}
"""

    else:
        prompt = f"""
You are EduGenie, an educational AI assistant.

Explain the following topic to a student.

Topic:
{topic}

Student level:
{level}

Requirements:
1. Explain the topic clearly and accurately.
2. Use language appropriate for the student's level.
3. Start with the basic idea before introducing harder details.
4. Break difficult ideas into smaller steps.
5. Include a simple example.
6. Include the most important points.
7. Do not invent unsupported facts.
8. Return ONLY valid JSON.
9. Do not use Markdown code fences.

Use this exact JSON structure:

{{
  "topic": "{topic}",
  "level": "{level}",
  "explanation": "Clear explanation of the topic.",
  "key_points": [
    "Important point 1",
    "Important point 2",
    "Important point 3"
  ],
  "example": "A simple example related to the topic.",
  "quick_check": "A short question the student can use to check their understanding."
}}
"""

    response = generate_text(prompt)

    result = _extract_json(response)

    _validate_explanation(result)

    return result


def _extract_json(text: str) -> Dict[str, Any]:
    """
    Extract JSON from an AI response.
    """

    if not text or not text.strip():
        raise ValueError("AI returned an empty response.")

    text = text.strip()

    # Remove Markdown code fences if present.
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

    # Try finding a JSON object inside the response.
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


def _validate_explanation(
    result: Dict[str, Any],
) -> None:
    """
    Validate the generated explanation.
    """

    required_fields = [
        "topic",
        "level",
        "explanation",
        "key_points",
        "example",
        "quick_check",
    ]

    for field in required_fields:
        if field not in result:
            raise ValueError(
                f"Explanation is missing '{field}'."
            )

    if not isinstance(result["explanation"], str):
        raise ValueError(
            "explanation must be a string."
        )

    if not isinstance(result["key_points"], list):
        raise ValueError(
            "key_points must be a list."
        )

    if not isinstance(result["example"], str):
        raise ValueError(
            "example must be a string."
        )

    if not isinstance(result["quick_check"], str):
        raise ValueError(
            "quick_check must be a string."
        )


def get_explanation(
    topic: str,
    level: str = "beginner",
    context: str = "",
) -> str:
    """
    Return only the explanation text.
    """

    result = explain_topic(
        topic=topic,
        level=level,
        context=context,
    )

    return result["explanation"]


def get_key_points(
    topic: str,
    level: str = "beginner",
    context: str = "",
) -> list:
    """
    Return only the key learning points.
    """

    result = explain_topic(
        topic=topic,
        level=level,
        context=context,
    )

    return result["key_points"]


def get_example(
    topic: str,
    level: str = "beginner",
    context: str = "",
) -> str:
    """
    Return only the example.
    """

    result = explain_topic(
        topic=topic,
        level=level,
        context=context,
    )

    return result["example"]


def get_quick_check(
    topic: str,
    level: str = "beginner",
    context: str = "",
) -> str:
    """
    Return a quick understanding-check question.
    """

    result = explain_topic(
        topic=topic,
        level=level,
        context=context,
    )

    return result["quick_check"]