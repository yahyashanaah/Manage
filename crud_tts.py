from gtts import gTTS
import os
from database import get_db
from fastapi import HTTPException

def create_tts_entry(text: str, language: str = 'en'):
    try:
        if language not in ['en', 'ar']:
            raise HTTPException(status_code=400, detail="Unsupported language. Use 'en' or 'ar'.")

        # Generate filename (handle Arabic filenames safely)
        safe_text = text[:10].replace(' ', '_')
        audio_filename = f"tts_{safe_text}.mp3"

        # Ensure "audio" directory exists
        os.makedirs("audio", exist_ok=True)
        file_path = os.path.join("audio", audio_filename)

        # Generate speech
        tts = gTTS(text=text, lang=language)
        tts.save(file_path)

        # Verify file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="TTS file was not saved correctly.")

        # Save to database
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tts_texts (text, audio_file, language) VALUES (?, ?, ?)", 
                           (text, file_path, language))
            conn.commit()
            return {"id": cursor.lastrowid, "text": text, "audio_file": file_path, "language": language}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


def get_tts_entry(tts_id: int):
    with get_db() as conn:
        entry = conn.execute("SELECT * FROM tts_texts WHERE id = ?", (tts_id,)).fetchone()
        if not entry:
            raise HTTPException(status_code=404, detail="Text not found")
        os.system(f"start {entry['audio_file']}")
        return dict(entry)

def delete_tts_entry(tts_id: int):
    with get_db() as conn:
        entry = conn.execute("SELECT * FROM tts_texts WHERE id = ?", (tts_id,)).fetchone()
        if not entry:
            raise HTTPException(status_code=404, detail="Text not found")
        os.remove(entry['audio_file'])
        conn.execute("DELETE FROM tts_texts WHERE id = ?", (tts_id,))
        conn.commit()
        return {"message": "Deleted successfully"}