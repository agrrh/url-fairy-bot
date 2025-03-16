from fastapi import APIRouter

from .api.handlers import process_url

api_router = APIRouter()

api_router.add_api_route("/process_url/", process_url, methods=["POST"])
