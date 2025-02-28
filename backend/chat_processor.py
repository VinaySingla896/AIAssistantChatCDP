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
        return """You are an expert CDP (Customer Data Platform) support agent with deep technical knowledge of 
        Segment (https://segment.com/docs/?ref=nav), 
        mParticle (https://docs.mparticle.com/), 
        Lytics (https://docs.lytics.com/), and 
        Zeotap (https://docs.zeotap.com/home/en-us/). 

        Handle questions with the following approach:
        1. For how-to questions: Provide clear, step-by-step instructions with technical details.
        2. For platform comparisons: Compare features, capabilities, and use cases across CDPs.
        3. For technical questions: Explain implementation details, APIs, and best practices.
        4. For troubleshooting: Guide through common issues and their solutions.
        5. For advanced configurations: Detail complex setups and integrations.

        If a question is not CDP-related, politely explain your focus on CDP platforms.
        Always cite the relevant documentation when providing answers."""

    async def _classify_question(self, question: str) -> Dict:
        """Classify the type of question to provide more targeted responses."""
        question_types = {
            "how_to": ["how to", "how do i", "steps to", "guide for"],
            "comparison": ["compare", "difference between", "versus", "vs"],
            "technical": ["api", "implementation", "code", "sdk"],
            "troubleshooting": ["error", "issue", "problem", "not working"],
            "configuration": ["setup", "configure", "settings", "advanced"]
        }

        question_lower = question.lower()
        for q_type, keywords in question_types.items():
            if any(keyword in question_lower for keyword in keywords):
                return {"type": q_type}
        return {"type": "general"}

    async def get_streaming_response(
        self,
        user_message: str,
        conversation_history: List[Dict],
        doc_processor
    ) -> AsyncGenerator[str, None]:
        try:
            messages = [SystemMessage(content=self._create_system_prompt())]

            # Add conversation history with improved context
            for msg in conversation_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(SystemMessage(content=msg["content"]))

            # Classify the question type
            question_type = await self._classify_question(user_message)

            # Add question classification context
            messages.append(SystemMessage(
                content=f"This appears to be a {question_type['type']} question. "
                       f"Provide a detailed response accordingly."
            ))

            # Get relevant documentation with increased context
            context = doc_processor.get_relevant_docs(
                user_message, 
                k=3  # Increased number of relevant docs
            )
            if context:
                messages.append(SystemMessage(
                    content=f"Relevant documentation for this {question_type['type']} question: {context}"
                ))

            # Add current message
            messages.append(HumanMessage(content=user_message))

            # Stream the response with enhanced error handling
            async for chunk in self.chat_model.astream(messages):
                if chunk.content:
                    yield chunk.content

        except Exception as e:
            print(f"Error in chat processing: {str(e)}")
            yield (
                "I apologize, but I encountered an error while processing your request. "
                "Please try rephrasing your question or breaking it down into smaller parts."
            )