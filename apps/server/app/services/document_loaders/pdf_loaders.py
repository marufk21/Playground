import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

_script_dir = Path(__file__).resolve().parent
_app_root = _script_dir.parent
_env_path = (_app_root / ".env").resolve()
load_dotenv(_env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PDF_PATH = (_script_dir / "python.pdf").resolve()


def summarize_pdf() -> tuple[bool, str]:
    if not OPENAI_API_KEY:
        return False, "API key missing"

    if not PDF_PATH.exists():
        return False, f"PDF not found at {PDF_PATH}"

    loader = PyPDFLoader(str(PDF_PATH))
    documents = loader.load()
    full_text = "\n\n".join(doc.page_content for doc in documents)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an AI assistant that summarizes text clearly."),
            (
                "human",
                "Summarize the following PDF content in 6-8 bullet points.\n\n{text}",
            ),
        ]
    )

    model = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4o-mini",
        temperature=0,
    )

    try:
        messages = prompt.format_messages(text=full_text)
        res = model.invoke(messages)
        content = res.content
        if isinstance(content, str):
            return True, content
        return True, str(content)
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    ok, detail = summarize_pdf()
    print({"ok": ok, "detail": detail[:500] + "..." if len(detail) > 500 else detail})
