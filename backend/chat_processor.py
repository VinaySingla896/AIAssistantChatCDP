from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List, Dict, AsyncGenerator
import json
import asyncio

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
        Segment (https://segment.com/docs/?ref=nav), 
        mParticle (https://docs.mparticle.com/), 
        Lytics (https://docs.lytics.com/), and 
        Zeotap (https://docs.zeotap.com/home/en-us/). 

        Focus on providing clear, step-by-step instructions for how-to questions. If a question is not related 
        to these CDPs, politely explain that you can only help with CDP-related queries."""

    async def get_streaming_response(
        self,
        user_message: str,
        conversation_history: List[Dict],
        doc_processor
    ) -> AsyncGenerator[str, None]:
        try:
            messages = [SystemMessage(content=self._create_system_prompt())]

            # Add conversation history
            for msg in conversation_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(SystemMessage(content=msg["content"]))

            # Add current message
            messages.append(HumanMessage(content=user_message))

            # Get relevant documentation context
            context = doc_processor.get_relevant_docs(user_message)
            if context:
                messages.append(SystemMessage(content=f"Relevant documentation: {context}"))

            # Stream the response
            async for chunk in self.chat_model.astream(messages):
                if chunk.content:
                    yield chunk.content

        except Exception as e:
            print(f"Error in chat processing: {str(e)}")
            yield f"I apologize, but I encountered an error while processing your request. Please try again."