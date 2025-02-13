from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from api.bot.request.bot import BotDocumentsQueryRequest, BotQueryRequest, BotRequest
from api.bot.response.bot import BotQueryResponse
from datetime import datetime
from app.bot.bot import BotService, DocumentBotService, BotThreadService

bot_router = APIRouter(prefix="/api/bot", tags=["Bot"])

@bot_router.post("/response", response_model= BotQueryResponse)
async def get_answer_from_bot(bot: BotQueryRequest):
    reponse = BotService().get_answer_from_bot(bot=bot)
    return reponse

@bot_router.post("/document/response", response_model= BotQueryResponse)
async def get_answer_from_document_bot(bot: BotDocumentsQueryRequest):
    response = DocumentBotService().get_response_from_bot_on_document(bot_request= bot)
    return response

@bot_router.post("/thread/response", response_model= BotQueryResponse)
async def get_answer_from_bot(bot: BotRequest):
    reponse = BotThreadService().get_answer_from_thread_bot(bot)
    return reponse