from fastapi import FastAPI, Request
from tortoise.contrib.fastapi import register_tortoise

from tortoise import Tortoise

from core.orm_config import config_db


app = FastAPI()


DATABASE_CONFIG = config_db()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to Housify AI-Server API"}


async def on_startup():
    await Tortoise.init(config=DATABASE_CONFIG)
    await Tortoise.generate_schemas()


app.add_event_handler("startup", on_startup)


register_tortoise(
    app,
    config=DATABASE_CONFIG,
    generate_schemas=False,
    add_exception_handlers=True,
)
