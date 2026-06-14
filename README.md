# 🤖 СберБизнес AI-ассистент

> Умный ассистент для СберБизнес — отвечает на вопросы, ведёт по навигации приложения и показывает данные пользователя.

## ✨ Возможности

| Возможность | Описание |
|-------------|----------|
| 📚 **RAG по документации** | Отвечает на вопросы по банковским продуктам, инструкциям, памяткам на основе загруженных PDF/DOCX/MD |
| 🧭 **Навигация по приложению** | Понимает, какой экран/функцию ищет пользователь, и возвращает кнопку для перехода |
| 👤 **Данные пользователя** | Выполняет SQL-запросы к тестовой БД платежей — статусы, суммы, получатели |
| 💬 **Диалоговый контекст** | Помнит историю беседы в рамках сессии |

## 🏗️ Архитектура

```
                       ┌──────────┐
                       │  router  │  ← LLM определяет что нужно
                       └────┬─────┘
                  ┌─────────┼──────────┐
                  ▼         ▼          ▼
             ┌────────┐ ┌────────┐ ┌──────────┐
             │  RAG   │ │  NAV   │ │ USERDATA │
             └───┬────┘ └───┬────┘ └─────┬────┘
                 │          │            │
                 ▼          ▼            ▼
             ┌──────────────────────────────┐
             │      control_button_check     │  ← валидация кнопки
             └──────────────┬───────────────┘
                            ▼
             ┌──────────────────────────────┐
             │         controller            │  ← финальный контроль качества
             └──────────────────────────────┘
```

### Три ветки обработки

**📚 RAG** — вопрос по документации/продуктам
```
router → rag_rewriter → document_search → context_build → rag_assistant → controller
```

**🧭 Навигация** — поиск экрана/функции
```
router → nav_navigator → nav_search → context_build → nav_assistant → controller
```

**👤 Данные пользователя** — запрос к БД платежей
```
router → sql_writer → load_data → context_build → rag_rewriter → ... → controller
```

## 🧰 Стек

| Компонент | Технология |
|-----------|-----------|
| Backend | Python 3.14 + FastAPI |
| AI/LLM | LangGraph + OpenAI-compatible API |
| База знаний | ChromaDB + sentence-transformers |
| Эмбеддинги | `intfloat/multilingual-e5-base` |
| База данных | SQLite (тестовые данные) |
| Документы | PDF, DOCX, Markdown |

## 🚀 Быстрый старт

```bash
# 1. Клонировать
git clone <repo>
cd ai-assistant

# 2. Виртуальное окружение
python -m venv .venv
.venv\Scripts\activate  # Windows

# 3. Зависимости
pip install -r requirements.txt

# 4. Настроить .env
cp .env.example .env
# Вписать API_KEY и BASE_URL

# 5. Инициализировать БД платежей
python services/init_db.py

# 6. Загрузить знания (опционально, если папка knowledge пустая)
python ingest.py
python create_navigation_rag.py

# 7. Запустить API
uvicorn app:app --host 0.0.0.0 --port 80 --log-level info
```

### Или консольный режим

```bash
python assistant.py
```

## 🧪 Примеры запросов

### Навигация
```
Как открыть депозит?
→ 🧭 Продукты > Финансы > Депозиты  [openDeposit]

Где посмотреть курсы валют?
→ 🧭 Инфо > Курсы валют  [viewFxRates]
```

### Вопросы по документации
```
Что такое эквайринг?
→ 📚 Ответ на основе загруженных документов

Какие документы нужны для открытия счета?
→ 📚 Поиск по PDF-памяткам
```

### Данные пользователя
```
Покажи мои платежи
→ 📊 SELECT * FROM payments

Какие платежи сейчас в обработке?
→ 📊 SELECT * FROM payments WHERE status = 'IN_PROGRESS'

Почему не прошёл платёж?
→ 📊 Анализ статуса FAILED + RAG по документации
```

## 🔬 Мониторинг

Структурированное логирование каждого шага пайплайна:

```
14:03:45 | 🟣═╗ ПАЙПЛАЙН СТАРТ
14:03:45 |   │ question: Как открыть депозит?
14:03:45 |  ┌─ 🧭 [router]
14:03:46 | 🧭 │ ВЕТКА: NAVIGATION
14:03:46 |  └─ ✓ [router] (0.54s)
14:03:46 |  ┌─ 🧭 [nav_navigator]
14:03:46 |  └─ ✓ [nav_navigator] (0.31s)
14:03:46 |  ┌─ 🔎 [nav_search]
14:03:46 |   ℹ  🧭 dist=0.2209 | Оформить депозит (openDeposit)
14:03:46 |  └─ ✓ [nav_search] (0.15s)
...
14:03:48 | 🟣═╝ ПАЙПЛАЙН КОНЕЦ (2.94s) ✅
```

## 🐳 Docker

```bash
docker build -t ai-assistant .
docker run -p 80:80 \
  -e API_KEY=your_key \
  -e BASE_URL=https://api.aitunnel.ru/v1/ \
  ai-assistant
```

> **Важно:** В Docker обязательно смонтировать `/app/chroma_db` и `/app/services/payments.db` как volume, либо предварительно загрузить знания.

## 📁 Структура проекта

```
ai-assistant/
├── app.py                         # FastAPI приложение
├── assistant.py                   # Консольный клиент
├── graph/
│   ├── builder.py                 # Сборка LangGraph
│   ├── state.py                   # Состояние графа
│   └── nodes/                     # Узлы пайплайна
│       ├── router.py              # Маршрутизатор
│       ├── control.py             # Контроллер качества
│       ├── nav_*.py               # Ветка навигации
│       ├── rag_*.py               # Ветка RAG
│       └── user_*.py              # Ветка данных пользователя
├── services/
│   ├── llm.py                     # OpenAI-клиент
│   ├── rag.py                     # ChromaDB для документов
│   ├── nav_rag.py                 # ChromaDB для навигации
│   ├── db.py                      # SQLite-клиент
│   ├── pipeline_logger.py         # Структурированное логирование
│   └── init_db.py                 # Инициализация тестовой БД
├── prompts/                       # Системные промпты
├── knowledge/                     # База знаний (PDF, DOCX, MD)
├── journeys.json                  # Маршруты навигации
├── ingest.py                      # Загрузка документов в ChromaDB
└── create_navigation_rag.py       # Загрузка маршрутов навигации
```

## 🛣️ Дорожная карта

- [x] MVP: три ветки обработки + API
- [x] Логирование пайплайна
- [ ] Redis для сессий
- [ ] Rate limiting
- [ ] Web UI (чат-интерфейс)
- [ ] Мониторинг в Grafana

---

*MVP проект. Built with LangGraph + FastAPI.*