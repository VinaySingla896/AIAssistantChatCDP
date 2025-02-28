from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List, Dict, AsyncGenerator
import json

class ChatProcessor:
    def __init__(self, api_key: str):
        # the newest OpenAI model is "gpt-4o-mini" which was released in 2025
        self.chat_model = ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=api_key,
            streaming=True,
            temperature=0.7
        )

    def _create_system_prompt(self) -> str:
        return """You are a helpful CDP (Customer Data Platform) support agent. You can answer questions about 
        Segment, mParticle, Lytics, and Zeotap. Focus on providing clear, step-by-step instructions for how-to 
        questions. If a question is not related to these CDPs, politely explain that you can only help with 
        CDP-related queries. Base your answers on official documentation."""

    async def get_streaming_response(
        self,
        user_message: str,
        conversation_history: List[Dict],
        doc_processor
    ) -> AsyncGenerator[str, None]:
        messages = [SystemMessage(content=self._create_system_prompt())]

        # Add conversation history
        for msg in conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(SystemMessage(content=msg["content"]))

        # Add current message
        messages.append(HumanMessage(content=user_message))

        # Get relevant documentation context
        context = doc_processor.get_relevant_docs(user_message)
        if context:
            messages.append(SystemMessage(content=f"Relevant documentation: {context}"))

        response = await self.chat_model.agenerate([messages])

        async for chunk in response.chunks:
            if chunk.content:
                yield chunk.content
