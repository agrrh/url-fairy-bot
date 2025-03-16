from fastapi import Body, HTTPException
from pydantic import BaseModel

from .utils.url_processing import process_url_request


class URLRequest(BaseModel):
    url: str


async def process_url(request: URLRequest = Body(...)):
    try:
        result = await process_url_request(request.url)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
