from dotenv import load_dotenv
load_dotenv()
import os
from utils.audio_processor import process_input
from core.transcriber import transcribe_all



source = "https://youtu.be/KQdF1XJ_aRQ?si=Mc_EA5plAPQvnPB_"
language = "hinglish"   # change to "hinglish" to test sarvam

chunks = process_input(source)
transcript = transcribe_all(chunks, language=language)


print("\n=== TRANSCRIPT ===\n")
print(transcript)