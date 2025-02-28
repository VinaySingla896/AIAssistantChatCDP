from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from chat_processor import ChatProcessor
from document_processor import DocumentProcessor
from sse_starlette.sse import EventSourceResponse
import asyncio

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    api_key: str
    conversation_history: Optional[List[dict]] = []

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        chat_processor = ChatProcessor(request.api_key)
        doc_processor = DocumentProcessor()

        async def generate_response():
            async for chunk in chat_processor.get_streaming_response(
                request.message,
                request.conversation_history,
                doc_processor
            ):
                yield chunk

        return EventSourceResponse(generate_response())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
