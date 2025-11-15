from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from ..dependencies import get_core

app = FastAPI(title="Document QA Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_file(
    user_id: int = Form(...),
    file: UploadFile = File(...)
):
    core = get_core()

    content = (await file.read()).decode("utf-8")
    core.save_file(
        user_id=user_id,
        file_name=file.filename,
        content=content
    )

    core.history_store.clear(user_id)
    return {"status": "ok", "filename": file.filename}


@app.post("/ask")
async def ask_question(
    user_id: int = Form(...),
    question: str = Form(...)
):
    core = get_core()

    answer = await core.ask(user_id=user_id, question=question)
    return {"answer": answer}
