from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import shutil
import os
from pathlib import Path

from ..config import settings
from ..core.core import Core
from ..core.loader import makeReader

router = APIRouter()
core = Core()

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_file(user_id: int = Form(...), file: UploadFile = File(...)):
    """
    Upload a document file for the user, process and store its content.
    """
    # save file
    user_dir = UPLOAD_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    dest = user_dir / file.filename
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        reader = makeReader(str(dest))
        content = reader.read(str(dest))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot read file: {e}")

    core.save_file(user_id=user_id, file_name=file.filename, content=content)
    return JSONResponse({"status": "ok", "message": "file uploaded and processed"})

@router.post("/ask")
async def ask(user_id: int = Form(...), question: str = Form(...)):
    """
    Ask a question based on the user's stored document content.
    """
    # get user's stored content and retriever
    context_chunks = core.retriever.get_relevant_chunks(user_id, question, top_k=4)
    if not context_chunks:
        # fallback to full content (if exists) but warn
        content = core.user_store.get_content(user_id)
        if not content:
            raise HTTPException(status_code=404, detail="No document found for user")
        # As fallback, chunk content and add to retriever
        core.retriever.add_document(user_id, content)
        context_chunks = core.retriever.get_relevant_chunks(user_id, question, top_k=4)

    history = core.history_store.get_history(user_id)
    answer = await core.ask(user_id=user_id, question=question, history=history)
    # save history
    core.history_store.add_message(user_id, role="user", text=question)
    core.history_store.add_message(user_id, role="assistant", text=answer)
    return JSONResponse({"answer": answer})

@router.get("/history/{user_id}")
def get_history(user_id: int):
    history = core.history_store.get_history(user_id)
    return JSONResponse({"history": history})
