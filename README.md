# PEs04 — интерактивный чат-бот через OpenAI API

Учебный проект для дополнительного задания урока «API: как обращаться к модели напрямую» курса [Zerocoder](https://zerocoder.ru/).

Материалы курса размещены на образовательной платформе [university.zerocoder.ru](https://university.zerocoder.ru/).

## Подготовка

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Добавьте свой ключ в локальный `.env`. Этот файл исключён из Git и не должен публиковаться.

## Запуск

```powershell
python main.py
```

Для проверки структуры запроса без обращения к API и без расходов:

```powershell
python main.py --dry-run --question "Объясни, что такое API"
```

Сравнение стиля на одном вопросе:

```powershell
python main.py --temperature 0.3 --question "Предложи название сервиса доставки"
python main.py --temperature 1.0 --question "Предложи название сервиса доставки"
```

В условии урока указана температура `1.5`, но актуальная схема Responses API допускает диапазон от `0` до `1`, поэтому для второго эксперимента используется `1.0`.

Программа выводит готовый текст, полный JSON-ответ и статистику `input_tokens`, `output_tokens`, `total_tokens`.

