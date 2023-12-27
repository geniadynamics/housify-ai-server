from dotenv import load_dotenv
import os
from pathlib import Path

root_path = Path(__file__).parent.parent.parent


def config_db():
    """ """

    env_path = root_path / "src" / ".env"
    load_dotenv(env_path)

    ENV = os.getenv("ENV", "development")
    DB_URL = (
        os.getenv("PROD_DB_URL") if ENV == "production" else os.getenv("DEV_DB_URL")
    )

    return {
        "connections": {"default": DB_URL},
        "apps": {
            "models": {
                "models": [
                    "data.models.image",
                    "data.models.img_edit",
                    "data.models.img_classification",
                    "data.models.img_generated_description",
                    "data.models.img_generation",
                    "data.models.usage",
                    "data.models.inference_model",
                ],
                "default_connection": "default",
            },
        },
    }
