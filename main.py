"""Учебный интерактивный чат-бот для OpenAI Responses API."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any


DEFAULT_INSTRUCTIONS = (
    "Отвечай на русском языке кратко и понятно, как эксперт для новичка. "
    "Если тема сложная, добавь один короткий пример."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Учебный чат-бот OpenAI")
    parser.add_argument("--question", help="Вопрос без интерактивного ввода")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    parser.add_argument("--temperature", type=float, default=0.3)
    parser.add_argument("--max-output-tokens", type=int, default=500)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать запрос без обращения к API и без списания средств",
    )
    return parser.parse_args()


def build_request(args: argparse.Namespace, question: str) -> dict[str, Any]:
    if not 0 <= args.temperature <= 1:
        raise ValueError("Для актуального Responses API temperature должна быть от 0 до 1.")
    if args.max_output_tokens < 16:
        raise ValueError("max_output_tokens должен быть не меньше 16.")
    return {
        "model": args.model,
        "instructions": DEFAULT_INSTRUCTIONS,
        "input": question,
        "temperature": args.temperature,
        "max_output_tokens": args.max_output_tokens,
    }


def run_online(request: dict[str, Any]) -> None:
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "Не найден OPENAI_API_KEY. Скопируйте .env.example в .env "
            "и добавьте свой ключ."
        )

    client = OpenAI(api_key=api_key)
    response = client.responses.create(**request)

    print("\nОтвет модели:\n")
    print(response.output_text)
    print("\nПолная структура ответа:\n")
    print(json.dumps(response.model_dump(), ensure_ascii=False, indent=2))

    usage = response.usage
    if usage:
        print("\nРасход токенов:")
        print(f"  Входные:  {usage.input_tokens}")
        print(f"  Выходные: {usage.output_tokens}")
        print(f"  Всего:    {usage.total_tokens}")


def main() -> None:
    args = parse_args()
    question = (args.question or input("Введите вопрос: ")).strip()
    if not question:
        raise SystemExit("Вопрос не должен быть пустым.")

    try:
        request = build_request(args, question)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    if args.dry_run:
        print(json.dumps(request, ensure_ascii=False, indent=2))
        return

    run_online(request)


if __name__ == "__main__":
    main()

