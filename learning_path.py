from gemini_service import generate_text


def get_learning_recommendations(topic):
    prompt = f"""
Create a simple learning path for the topic: {topic}

Include:
1. Beginner Level
2. Intermediate Level
3. Advanced Level
4. Recommended Resources

Keep it simple and suitable for a college student.
"""

    return generate_text(prompt)