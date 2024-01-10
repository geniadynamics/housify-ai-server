import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "core.ai_service:app",
        host="0.0.0.0",
        port=8082,
        # workers=12,
        reload=True,  # Set to false when using multiple workers
    )
