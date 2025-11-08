# Incident Tracker API

Минимальный сервис для учёта инцидентов: оператор/мониторинг/партнёр может создать запись, увидеть список и сменить статус.

## Стек

- Python + FastAPI
- SQLite (`sqlmodel`) 
- `uvicorn` для запуска

## Подготовка

```bash
python -m venv .venv
source .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Описание API

### Создать инцидент

- `POST /incidents`
- Тело: `{ "description": "текст", "source": "operator", "status": "new" }`
- Если статус не указан, по умолчанию `new`.

### Получить список инцидентов

- `GET /incidents`
- Параметр `status` (необязательный) фильтрует по статусу.

### Обновить статус

- `PATCH /incidents/{id}/status`
- Тело: `{ "status": "resolved" }`
- При несуществующем `id` возвращает 404.

## Запуск

```bash
uvicorn app.main:app --reload
```

База `incidents.db` создаётся автоматически в корне при первом старте.

### Тестирование api-сервиса по адресу:
`http://localhost:8000/docs#/`

## Запуск тестов
```bash
pytest -q
```