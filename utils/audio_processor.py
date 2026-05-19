import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR = 'downloads'


os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_audio_from_youtube(url  :str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }
    ],
    "quiet": True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict).replace('.webm', '.wav').replace('.m4a', '.wav')
        return file_name


data = download_audio_from_youtube("https://youtu.be/XuCi1pbp71g?si=otAzNZ6BU9uEt0E5")

def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to wav format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path


print(convert_to_wav(data))


def chunk_audio(wav_path : str , chunk_minutes: int = 10 ) -> list:
    """Chunk a wav file into smaller segments of specified minutes."""
    audio = AudioSegment.from_wav(wav_path)
    chunk_length_ms = chunk_minutes * 60 * 1000
    chunks = []
    
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_path = f"{os.path.splitext(wav_path)[0]}_chunk_{i//chunk_length_ms}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    
    return chunks

print(chunk_audio(convert_to_wav(data)))