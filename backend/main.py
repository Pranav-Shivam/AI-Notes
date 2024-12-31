from fastapi import FastAPI
from api.route.route import router as testroute
from api.document.document import document_router
from api.bot.bot import bot_router
import uvicorn

app = FastAPI()
app.include_router(testroute)
app.include_router(document_router)
app.include_router(bot_router)



if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)