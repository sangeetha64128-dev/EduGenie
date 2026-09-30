from fastapi import APIRouter
from pydantic import BaseModel

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


api_router = APIRouter()


class UserInput(BaseModel):
    text: str


@api_router.post("/qa")
def qa(data: UserInput):
    if not data.text.strip():
        return {"result": "Please enter a question."}

    return {"result": answer_question(data.text)}


@api_router.post("/explain")
def explain(data: UserInput):
    if not data.text.strip():
        return {"result": "Please enter a topic to explain."}

    return {"result": explain_topic(data.text)}


@api_router.post("/quiz")
def quiz(data: UserInput):
    if not data.text.strip():
        return {
            "result": [],
            "error": "Please enter a topic or passage."
        }

    return generate_quiz(data.text)


@api_router.post("/summarize")
def summarize(data: UserInput):
    if not data.text.strip():
        return {"result": "Please enter text to summarize."}

    return {"result": summarize_text(data.text)}


@api_router.post("/learn/recommendations")
def learning_recommendations(data: UserInput):
    if not data.text.strip():
        return {
            "result": "Please enter a topic for the learning path."
        }

    return {
        "result": get_learning_recommendations(data.text)
    }


@api_router.get("/api/test")
def test_api():
    return {"message": "EduGenie API is working!"}