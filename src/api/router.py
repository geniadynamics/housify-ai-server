# from fastapi import FastAPI, HTTPException
# from pydantic import UUID4
# from PIL import Image
# from transformers.utils.hub import uuid4
# from data.schemas.request import RequestSchema
# from data.models.request import Request
# from services.inference.edit import edit_image
# from services.inference.generation import generate_image
# from services.inference.analysis import analyze_image
# from services.inference.classify import classify_image
# import asyncio
#
#
# async def create_request(request_data: RequestSchema) -> Request:
#     request = Request(**request_data.model_dump())
#     await request.save()
#     return request
#
#
# async def get_request(request_id: UUID4) -> Request:
#     request = await Request.get(id=request_id)
#     if request is None:
#         raise HTTPException(status_code=404, detail="Request not found")
#     return request
#
#
# app = FastAPI()
#
# lock = asyncio.Lock()
#
#
# @app.post("/inference-request", response_model=RequestSchema)
# async def inference_request(data: RequestSchema):
#     async with lock:
#         try:
#             image: Image.Image | None = None
#             if data.img_input != None:
#                 image = await edit_image(data.img_input, data.input)
#             else:
#                 image = await generate_image(data.input)
#             if image:
#                 data.img_output = uuid4().hex
#                 image.save(data.img_output)
#                 data.output_description = await analyze_image(data.img_output)
#                 data.output_classification = await classify_image(data.img_output)
#
#             return data
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))
