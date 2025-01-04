from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from api.question.request.question import QuestionAnswerRequest
from api.question.response.question import QuestionAnswerResponse, SaveQuestionResponse
from app.question.question import QuestionService

question_router = APIRouter(prefix="/api/question", tags=["Questions"])

@question_router.post("/create/response", response_model=SaveQuestionResponse)
async def save_question_answer(query: QuestionAnswerRequest):
    response = QuestionService().save_query_and_response_db(query=query)
    return response