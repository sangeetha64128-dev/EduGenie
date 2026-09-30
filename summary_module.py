from typing import Dict, Any
import re

from gemini_service import generate_text


def summarize_text(
    text: str,
    max_length: int = 250,
) -> Dict[str, Any]:
    """
    Generate a concise educational summary from the supplied text.
    """

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    text = text.strip()

    prompt = f"""
You are an educational AI assistant.

Summarize the following text for a student.

Requirements:
1. Keep the important facts and main ideas.
2. Use simple and clear language.
3. Do not add information that is not present in the supplied text.
4. Organize the summary into short paragraphs or bullet points when useful.
5. Keep the summary approximately {max_length} words or fewer.
6. Include the key concepts and important details.
7. Return ONLY valid JSON.
8. Do not use Markdown code fences.

Use this exact JSON structure:

{{
  "summary": "The concise summary goes here.",
  "key_points": [
    "Important point 1",
    "Important point 2",
    "Important point 3"
  ]
}}

Text to summarize:

{text}
"""

    response = generate_text(prompt)

    result = _extract_json(response)

    if "summary" not in result:
        raise ValueError("AI response does not contain a summary.")

    if "key_points" not in result:
        result["key_points"] = []

    if not isinstance(result["key_points"], list):
        result["key_points"] = [str(result["key_points"])]

    return result


def _extract_json(text: str) -> Dict[str, Any]:
    """
    Extract JSON from the AI response.
    """

    text = text.strip()

    # Remove Markdown code fences if the model adds them.
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

    # Try normal JSON parsing first.
    import json

    try:
        return json.loads(text)

    except json.JSONDecodeError:
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


def create_short_summary(text: str) -> str:
    """
    Return only the summary text.
    """

    result = summarize_text(
        text=text,
        max_length=150,
    )

    return result["summary"]


def extract_key_points(text: str) -> list:
    """
    Extract the important learning points from the supplied text.
    """

    result = summarize_text(
        text=text,
        max_length=250,
    )

    return result.get("key_points", [])