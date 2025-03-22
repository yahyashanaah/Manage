from gtts import gTTS
import os
from database import get_db
from fastapi import HTTPException

def create_tts_entry(text: str, language_id: int):
    try:
        with get_db() as conn:
            # Get language code from languages table
            cursor = conn.cursor()
            cursor.execute("SELECT code FROM languages WHERE id = ?", (language_id,))
            language_row = cursor.fetchone()
            
            if not language_row:
                raise HTTPException(status_code=400, detail="Invalid language ID.")

            language_code = language_row[0]  # Extract language code ('en' or 'ar')

            # Generate a safe filename prefix
            safe_text = text[:10].replace(' ', '_')
            audio_filename = f"tts_{safe_text}_{language_code}.mp3"
            file_path = os.path.join("audio", audio_filename)

            # Ensure "audio" directory exists
            os.makedirs("audio", exist_ok=True)

            # Generate speech file
            tts = gTTS(text=text, lang=language_code)
            tts.save(file_path)

            # Verify file exists
            if not os.path.exists(file_path):
                raise HTTPException(status_code=500, detail="TTS file was not saved correctly.")

            # Save to database
            cursor.execute("INSERT INTO tts_texts (text, audio_file, language_id) VALUES (?, ?, ?)", 
                           (text, file_path, language_id))
            conn.commit()

            return {"id": cursor.lastrowid, "text": text, "audio_file": file_path, "language": language_code}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


def get_tts_entry(tts_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tts_texts.audio_file, languages.code 
            FROM tts_texts 
            JOIN languages ON tts_texts.language_id = languages.id 
            WHERE tts_texts.id = ?
        """, (tts_id,))
        entry = cursor.fetchone()

        if not entry:
            raise HTTPException(status_code=404, detail="Text not found")

        audio_file, language_code = entry

        # Play audio (cross-platform method)
        if os.name == "nt":  # Windows
            os.system(f"start {audio_file}")
        else:  # macOS/Linux
            os.system(f"mpg123 {audio_file}")

        return {"audio_file": audio_file, "language": language_code}


def delete_tts_entry(tts_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT audio_file FROM tts_texts WHERE id = ?", (tts_id,))
        entry = cursor.fetchone()

        if not entry:
            raise HTTPException(status_code=404, detail="Text not found")

        audio_file = entry[0]

        # Delete file
        if os.path.exists(audio_file):
            os.remove(audio_file)

        # Delete from database
        cursor.execute("DELETE FROM tts_texts WHERE id = ?", (tts_id,))
        conn.commit()

        return {"message": "Deleted successfully"}
