import os

from dotenv import load_dotenv

from src.agent.agent import ReActAgent
from src.tools import get_cafe_tools


def build_provider():
    provider = os.getenv("DEFAULT_PROVIDER", "openai").lower()
    model = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")

    if provider == "openai":
        from src.core.openai_provider import OpenAIProvider

        return OpenAIProvider(
            model_name=model,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    if provider in {"google", "gemini"}:
        from src.core.gemini_provider import GeminiProvider

        return GeminiProvider(
            model_name=model or "gemini-1.5-flash",
            api_key=os.getenv("GEMINI_API_KEY"),
        )

    if provider == "local":
        from src.core.local_provider import LocalProvider

        return LocalProvider(
            model_path=os.getenv("LOCAL_MODEL_PATH", "./models/Phi-3-mini-4k-instruct-q4.gguf"),
        )

    raise ValueError(f"Unsupported DEFAULT_PROVIDER: {provider}")


def main():
    load_dotenv()
    agent = ReActAgent(
        llm=build_provider(),
        tools=get_cafe_tools(),
        max_steps=8,
    )

    default_question = (
        "Toi muon mua 2 ca phe sua va 1 tra dao, dung ma GIAM10, "
        "giao toi Quan 1. Tong tien bao nhieu?"
    )

    print("Smart Cafe Order Agent")
    print("Nhap cau hoi cua ban. Bam Enter de dung cau demo, hoac go 'exit' de thoat.")

    while True:
        question = input("\nUser: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Bye!")
            break

        if not question:
            question = default_question
            print(f"User: {question}")

        print("Agent:", agent.run(question))


if __name__ == "__main__":
    main()
