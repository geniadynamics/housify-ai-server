from fastapi import FastAPI, Request, HTTPException
from pydantic import UUID4
from tortoise.contrib.fastapi import register_tortoise

from services.inference.edit import edit_image
from services.inference.generation import generate_image
from services.inference.analysis import analyze_image
from services.inference.classify import classify_image

from PIL import Image
from data.schemas.request import RequestSchema
from data.models.request import Request
from tortoise import Tortoise
import asyncio
from uuid import uuid4

from core.orm_config import config_db


async def create_request(request_data: RequestSchema) -> Request:
    request = Request(**request_data.model_dump())
    await request.save()
    return request


async def get_request(request_id: UUID4) -> Request:
    request = await Request.get(id=request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


lock = asyncio.Lock()


app = FastAPI()


DATABASE_CONFIG = config_db()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to Housify AI-Server API"}

MEDIA_PATH="/var/web/housify/media/"


@app.post("/inference-request", response_model=RequestSchema)
async def inference_request(data: RequestSchema):
    async with lock:
        try:
            image: Image.Image | None = None
            if data.img_input != None:
                image = await edit_image(data.img_input, data.input)
            else:
                image = await generate_image(data.input)
            if image:
                data.img_output = uuid4().hex
                image.save(data.img_output)
                data.output_description = await analyze_image(data.img_output)
                data.output_classification = await classify_image(data.img_output)

            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


async def on_startup():
    await Tortoise.init(config=DATABASE_CONFIG)
    await Tortoise.generate_schemas()


app.add_event_handler("startup", on_startup)


register_tortoise(
    app,
    config=DATABASE_CONFIG,
    generate_schemas=True,
    add_exception_handlers=True,
)
