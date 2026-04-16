from fastapi import FastAPI, Request
import httpx

app = FastAPI()


@app.post("/webhook/google-drive")
async def handle_drive_change(request: Request):
    data = await request.json()
    file_id = data.get("fileId")

    async with httpx.AsyncClient() as client:
        # Отримуємо оновлений текст документу
        response = await client.get(
            f"https://docs.googleapis.com/v1/documents/{file_id}",
            headers={"Authorization": f"Bearer {GOOGLE_TOKEN}"}
        )
        doc = response.json()
        text = extract_text(doc)
        source_url = f"https://docs.google.com/document/d/{file_id}"
        title = doc["title"]

    # Переіндексовуємо
    ingest_document(text, source_url, title)
    return {"status": "reindexed", "file_id": file_id}