import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_server_root = Path(__file__).resolve().parents[2]

if __package__ in (None, ""):
    sys.path.insert(0, str(_server_root))

load_dotenv(_server_root / ".env")

from langchain_core.messages import HumanMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

def _resolve_hf_token() -> str | None:
    for key in ("HUGGINGFACEHUB_API_TOKEN", "HF_TOKEN", "HUGGING_FACE_HUB_TOKEN"):
        raw = os.getenv(key)
        if raw and (stripped := raw.strip()):
            return stripped
    return None


HUGGINGFACEHUB_API_TOKEN = _resolve_hf_token()
HF_CHAT_REPO_ID = os.getenv("HF_CHAT_REPO_ID", "deepseek-ai/DeepSeek-V4-Pro")


def _aimessage_content_to_text(content: object) -> str:
    """Normalize AIMessage.content (str or multimodal blocks) to a plain string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
            else:
                parts.append(str(block))
        return "".join(parts)
    return str(content)


async def check_huggingface_with_example_prompt() -> tuple[bool, str]:
    if not HUGGINGFACEHUB_API_TOKEN:
        return False, "API key missing (set HUGGINGFACEHUB_API_TOKEN or HF_TOKEN)"

    llm = HuggingFaceEndpoint(
        repo_id=HF_CHAT_REPO_ID,
        task="text-generation",
        max_new_tokens=256,
        do_sample=False,
        repetition_penalty=1.03,
        provider=os.getenv("HF_INFERENCE_PROVIDER", "auto"),
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    )
    chat_model = ChatHuggingFace(llm=llm)

    try:
        res = await chat_model.ainvoke(
            [HumanMessage(content="Capital of India and PAkistan")],
        )
        return True, _aimessage_content_to_text(res.content)
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    import asyncio

    ok, detail = asyncio.run(check_huggingface_with_example_prompt())
    print({"ok": ok, "detail": detail[:500] + "..." if len(detail) > 500 else detail})
