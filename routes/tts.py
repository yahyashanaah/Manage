from fastapi import APIRouter
from models import TTSTextCreate, TTSTextResponse
from crud_tts import create_tts_entry, get_tts_entry, delete_tts_entry

router = APIRouter()

@router.post("/", response_model=TTSTextResponse)
def add_tts_entry(data: TTSTextCreate):
    return create_tts_entry(data.text)

@router.get("/{tts_id}", response_model=TTSTextResponse)
def fetch_tts_entry(tts_id: int):
    return get_tts_entry(tts_id)

@router.delete("/{tts_id}")
def remove_tts_entry(tts_id: int):
    return delete_tts_entry(tts_id)