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


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to wav format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path




def chunk_audio(wav_path : str , chunk_minutes: int = 10 ) -> list:
    """Chunk a wav file into smaller segments of specified minutes."""
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000
    chunks = []
    
    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start:start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")  
        chunks.append(chunk_path)
    
    return chunks


def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print(f"Detected YouTube URL, downloading audio...")
        wav_path = download_audio_from_youtube(source)
    else:
        print(f"Detected local file, converting to wav if necessary...")
        wav_path = convert_to_wav(source)
    
    print(f"Chunking audio into segments...")
    chunk_paths = chunk_audio(wav_path)
    print(f"Audio ready - {len(chunk_paths)} chunk(s) created,")
    return chunk_paths