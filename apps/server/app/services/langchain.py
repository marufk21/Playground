import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_server_root = Path(__file__).resolve().parents[2]

if __package__ in (None, ""):
    sys.path.insert(0, str(_server_root))

load_dotenv(_server_root / ".env")

from langchain_openai import ChatOpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


async def check_openai_with_example_prompt() -> tuple[bool, str]:
    if not OPENAI_API_KEY:
        return False, "API key missing"

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4o-mini",
        temperature=0,
    )

    try:
        res = await llm.ainvoke("Capital of India")
        content = res.content
        if isinstance(content, str):
            return True, content
        return True, str(content)
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    import asyncio

    ok, detail = asyncio.run(check_openai_with_example_prompt())
    print({"ok": ok, "detail": detail[:500] + "..." if len(detail) > 500 else detail})
