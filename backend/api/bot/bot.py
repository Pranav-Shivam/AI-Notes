from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from api.bot.request.bot import BotDocumentsQueryRequest, BotQueryRequest
from api.bot.response.bot import BotQueryResponse

bot_router = APIRouter(prefix="/api/bot", tags=["Bot"])

@bot_router.post("/bot", response_model= BotQueryResponse)
async def get_answer_from_bot(bot: BotQueryResponse):
    pass
    