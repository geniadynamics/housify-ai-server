# from services.queue_system import InferenceQueue
#
#
#
# class InferenceService:
#
#     def __init__(self, ):
#         self.a = 0
#
#     async def process(self):
#         pass
#
#     async def new_request(self):
#         pass

# import asyncio
# from typing import Dict, Union, Any
# from enum import Enum, auto
# from .inference.generation import generate_image
# from .inference.analysis import analyze_image
# from .inference.edit import edit_image
# from .inference.classify import classify_image
#
#
# class RequestType(Enum):
#     GENERATION = auto()
#     EDIT = auto()
#     ANALYSIS = auto()
#
#
# class InferenceRequest:
#     def __init__(self, request_type: RequestType, data: Dict[str, Any]):
#         self.request_type = request_type
#         self.data = data
#
#
# request_queue = asyncio.Queue()
#
#
# async def process_request():
#     while True:
#         request: InferenceRequest = await request_queue.get()
#         try:
#             if request.request_type == RequestType.GENERATION:
#                 image = await generate_image(request.data["prompt"])
#             elif request.request_type == RequestType.EDIT:
#                 image = await edit_image(request.data["url"], request.data["prompt"])
#             elif request.request_type == RequestType.ANALYSIS:
#                 analysis_result = await analyze_image(request.data["image_file"])
#                 print(f"Analysis Result: {analysis_result}")
#         except Exception as e:
#             print(f"Error processing request: {e}")
#         finally:
#             request_queue.task_done()
#
#
# async def add_request(request_type: RequestType, data: Dict[str, Any]):
#     request = InferenceRequest(request_type, data)
#     await request_queue.put(request)
#
#
# asyncio.create_task(process_request())

# Example usage (should be inside an async function)
# await add_request(RequestType.GENERATION, {"prompt": "Modern House Interior"})
# await add_request(
#     RequestType.EDIT, {"url": "example.jpg", "prompt": "turn him into cyborg"}
# )
# await add_request(RequestType.ANALYSIS, {"image_file": "image3.png"})
