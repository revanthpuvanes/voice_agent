from typing import Any
import asyncio
import uuid

from google.genai.types import Content, Part
from google.adk.runners import InMemoryRunner


async def _run_bi_adk_async(
    root_agent,
    app_name: str,
    user_id: str,
    csv_path: str,
    question: str,
) -> dict[str, Any]:
    runner = InMemoryRunner(agent=root_agent, app_name=app_name)

    session_id = f"session_{uuid.uuid4().hex}"

    session = await runner.session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

    user_prompt = f"""
csv_path: {csv_path}
question: {question}
""".strip()

    content = Content(parts=[Part(text=user_prompt)])

    final_text = ""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=content,
    ):
        if getattr(event, "content", None):
            parts = getattr(event.content, "parts", []) or []
            for part in parts:
                text = getattr(part, "text", None)
                if text:
                    final_text += text

    updated_session = await runner.session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session.id,
    )

    return {
        "final_text": final_text,
        "state": dict(updated_session.state),
    }


def run_bi_adk(
    root_agent,
    app_name: str,
    user_id: str,
    csv_path: str,
    question: str,
) -> dict[str, Any]:
    return asyncio.run(
        _run_bi_adk_async(
            root_agent=root_agent,
            app_name=app_name,
            user_id=user_id,
            csv_path=csv_path,
            question=question,
        )
    )