import asyncio
import logging

from fastapi import FastAPI

from .config import config

from .api import api_router
from .bot import dp

logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
async def on_startup():
    # Start the bot's polling in a background task
    asyncio.create_task(dp.start_polling())


@app.on_event("shutdown")
async def on_shutdown():
    # Shutdown the dispatcher when FastAPI stops
    await dp.storage.close()
    await dp.storage.wait_closed()


logger.info("✨ URL Fairy bot initialized with FastAPI")
