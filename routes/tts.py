from fastapi import APIRouter
from models import TTSTextCreate, TTSTextResponse
from crud_tts import create_tts_entry, get_all_tts_entries, get_tts_entry, delete_tts_entry

router = APIRouter()

@router.post("/tts/")
def add_tts_entry(data: TTSTextCreate):
    return create_tts_entry(data.text, data.language_id)

@router.get("/tts/")
def list_all_tts_entries():
    return get_all_tts_entries()

@router.get("/{tts_id}", response_model=TTSTextResponse)
def fetch_tts_entry(tts_id: int):
    return get_tts_entry(tts_id)

@router.delete("/{tts_id}")
def remove_tts_entry(tts_id: int):
    return delete_tts_entry(tts_id)