# All Right Brain

Внутрішня AI-база знань компанії All Right.
Концепт реалізація для тестового завдання на позицію Automation Engineer.

## Огляд

All Right Brain збирає знання з Google Docs, Confluence, Slack та GitHub,
індексує їх через embeddings і дозволяє будь-кому отримати відповідь з посиланням на джерело
через Slack бот, REST API або Web UI.

## Архітектура

![Architecture diagram](architecture2.png)

## Структура проекту

- `ingestion.py` — розбиття документів на чанки, створення embeddings та індексація в Qdrant
- `rag.py` — семантичний пошук та генерація відповіді з посиланням на джерело
- `webhook.py` — автоматична переіндексація при зміні документу

## Технології

- **Vector DB:** Qdrant
- **Embeddings:** OpenAI text-embedding-3-small
- **LLM:** GPT-5
- **Framework:** FastAPI, LangChain
- **Джерела фази 1:** Google Docs, Confluence
- **Джерела фази 2:** Slack, GitHub

## Як це працює

1. Документи завантажуються → розбиваються на чанки → перетворюються на embeddings → зберігаються в Qdrant
2. При зміні документу → webhook тригерить автоматичну переіндексацію
3. Користувач ставить питання → семантичний пошук знаходить релевантні чанки → LLM генерує відповідь з посиланням на джерело

## Примітка

Це концепт реалізація, а не production-ready код.
