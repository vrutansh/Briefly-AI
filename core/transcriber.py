import whisper
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL","small")

_model = None

def load_model():
    global _model
    if _model is None:
       print(f"Loading Whisper model ....")
       _model = whisper.load_model(WHISPER_MODEL)
       print("whisper model loaded successfully")

    return _model


def transcribe_chunk( chunk_path: str, translate: bool = False ) :
      
      model = load_model()

      task = "translate" if translate else "transcribe"

      result = model.transcribe(chunk_path, task=task)

      return result["text"]



def transcribe_all(chunk_paths: list[str], translate: bool = False) -> str:
    full_transcript = ""
    for i, chunk in enumerate(chunk_paths):
        print(f"Transcribing chunk {i+1}...")
        text = transcribe_chunk(chunk, translate=translate)
        full_transcript += text + "\n"
        print("Transcription Completed")
    return full_transcript
    

