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
import re

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


MEDIA_PATH_OUT = "/var/web/housify/media/gen/"
MEDIA_PATH_IN = "/var/web/housify/media/in/"

MEDIA_URL_OUT = "https://housify.geniadynamics.org/media/gen/"
MEDIA_URL_IN = "https://housify.geniadynamics.org/media/in/"


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
                img_uuid = uuid4().hex
                image_file_path = MEDIA_PATH_OUT + img_uuid + ".png"
                data.img_output = MEDIA_URL_OUT + img_uuid + ".png"
                image.save(image_file_path)
                data.output_description = await analyze_image(image_file_path)
                data.output_classification = await classify_image(image_file_path)

            await filter_data(data)

            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


async def filter_data(data: RequestSchema):
    regex = r"ASSISTANT: (.*)"
    if data.output_description:
        data.output_description = "Analysis: " + re.search(
            regex, data.output_description
        ).group(1)
    if data.output_classification:
        data.output_classification = "Classification: " + re.search(
            regex, data.output_classification
        ).group(1)

    return data


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
