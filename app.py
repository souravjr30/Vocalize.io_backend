from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from summarizer import TextSummarizer
from tts_engine import TTSEngine
import whisper
from dotenv import load_dotenv
from pydub import AudioSegment
import os
import subprocess
import yt_dlp as youtube_dl
from fpdf import FPDF
from fitz import open as fitz_open  # PyMuPDF
from translator import translate_text
from braille_converter import text_to_braille
import torch

app = Flask(__name__)
CORS(app)
load_dotenv()

# Define output directory
#OUTPUT_DIR = r"C:/Users/soura/Demo/outputs"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", r"C:/Users/soura/Demo/outputs")

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Initialize components
summarizer = TextSummarizer()
tts_engine = TTSEngine(speaker_wav_path=os.getenv("SPEAKER_WAV_PATH", r"C:/Users/soura/Demo/AI.wav"), output_dir=OUTPUT_DIR)
#tts_engine = TTSEngine(speaker_wav_path = r"C:\Users\soura\Demo\AI.wav", output_dir=OUTPUT_DIR)

'''if not os.path.exists('./outputs'):
    os.makedirs('./outputs')'''

# Utility Functions
def convert_mp3_to_wav(mp3_path):
    audio = AudioSegment.from_mp3(mp3_path)
    #wav_path = os.path.splitext(mp3_path)[0] + ".wav"
    wav_path = os.path.join(OUTPUT_DIR, os.path.splitext(os.path.basename(mp3_path))[0] + ".wav")
    audio.export(wav_path, format="wav")
    return wav_path

'''def transcribe_audio_to_text(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]'''

def transcribe_audio_to_text(audio_path):
    # Load the model and move it to GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")  # Optional: Print to confirm device

    model = whisper.load_model("base").to(device)

    # Transcribe the audio
    result = model.transcribe(audio_path)
    return result["text"]

def extract_audio_from_youtube(youtube_url):
    ydl_opts = {'format': 'bestaudio[abr<=128k]/bestaudio/best', 'quiet': True, 'no_warnings': True}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            for f in info_dict['formats']:
                #if 'acodec' in f and 'vcodec' in f and f['acodec'] != 'none' and f['vcodec'] == 'none':
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    return f['url']
    except Exception as e:
        print(f"Error extracting audio from YouTube: {e}")
        return None
    return None

def convert_audio_to_wav(audio_url, output_path="audio.wav"):
    '''command = [
        'ffmpeg', '-i', audio_url, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_path
    ]'''
    command = [
    'ffmpeg',
    '-i', audio_url,
    '-vn',                         # No video
    '-acodec', 'pcm_s16le',         # Audio codec: PCM 16-bit little-endian
    '-ar', '44100',                 # Audio sampling rate: 44100 Hz
    '-ac', '2',                     # Audio channels: Stereo
    '-preset', 'ultrafast',         # FFmpeg preset for the fastest encoding
    '-threads', '6',                # Use 6 threads (you can adjust this based on your CPU)
    '-y',                           # Overwrite output file if it exists
    output_path
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during audio conversion: {e}")
        raise
    return output_path
    #subprocess.run(command, check=True)
    #return output_path

'''def extract_audio_from_youtube(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'outtmpl': os.path.join(OUTPUT_DIR, 'youtube_audio.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            audio_file = ydl.prepare_filename(info_dict)
            return audio_file
    except Exception as e:
        print(f"Error extracting audio from YouTube: {e}")
        return None

def convert_audio_to_wav(audio_path, output_path="audio.wav"):
    if not os.path.exists(audio_path):
        print(f"Error: File not found at {audio_path}")
        return None
    command = [
        'ffmpeg', '-i', audio_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_path
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during audio conversion: {e}")
        raise
    return output_path
'''
def extract_text_from_pdf(pdf_path):
    pdf_document = fitz_open(pdf_path)
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

def create_pdf_from_text(text, output_filename="summary.pdf"):
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(190, 10, text)
    pdf.output(output_path)
    return output_path

def save_text_as_brf(text, output_filename="summary.brf"):
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    braille_text = text_to_braille(text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(braille_text)
    return output_path

# Routes
@app.route("/summarize", methods=["POST"])
def summarize_input():
    input_type = request.form.get("input_type")
    file = request.files.get("file")
    text = request.form.get("text")
    youtube_url = request.form.get("youtube_url")
    target_language = request.form.get("language")

    if input_type == "text" and text:
        summary = summarizer.summarize(text)

    elif input_type == "file" and file:
        file_path = os.path.join(OUTPUT_DIR, file.filename)
        #file_path = f"./uploads/{file.filename}"
        file.save(file_path)

        if file.filename.endswith(".mp3"):
            file_path = convert_mp3_to_wav(file_path)
            text = transcribe_audio_to_text(file_path)
        elif file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        summary = summarizer.summarize(text)
        os.remove(file_path)

    elif input_type == "youtube" and youtube_url:
        audio_url = extract_audio_from_youtube(youtube_url)
        if not audio_url:
            return jsonify({"error": "Could not extract audio from YouTube"}), 500

        wav_path = convert_audio_to_wav(audio_url)
        #if not wav_path:
         #   return jsonify({"error": "Could not convert audio to WAV"}), 500
    
        text = transcribe_audio_to_text(wav_path)
        os.remove(wav_path)

        summary = summarizer.summarize(text)

    else:
        return jsonify({"error": "Invalid input or missing parameters"}), 400

    # Translate summary if language is specified
    translated_summary = summary
    if target_language:
        translated_summary = translate_text(summary, target_language)

    # Convert to speech '''tts_path = f"summary.mp3"'''
    tts_path = os.path.join(OUTPUT_DIR, "summary.mp3")
    tts_engine.text_to_speech(translated_summary, tts_path, speaker_wav=tts_engine.speaker_wav_path)

    # Create BRF file
    brf_path = save_text_as_brf(summary)

    # Create PDF file
    pdf_path = create_pdf_from_text(translated_summary)

    return jsonify({
        "summary": summary,
        "translated_summary": translated_summary,
        "speech_file": tts_path,
        "brf_file": brf_path,
        "pdf_file": pdf_path
    })
#'''os.path.join(tts_engine.output_dir, tts_path)'''
@app.route("/download", methods=["GET"])
def download_file():
    file_path = request.args.get("file_path")
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(file_path, as_attachment=True, conditional=False)

if __name__ == "__main__":
     app.run(debug=True)

'''if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)'''


'''English: en (default if no language is specified)
Spanish: es
French: fr
German: de
Hindi: hi
Chinese (Simplified): zh
Japanese: ja
Korean: ko
Russian: ru
Portuguese: pt
Italian: it
Arabic: ar
Bengali: bn
Malayalam: ml
Tamil: ta
Telugu: te
Urdu: ur
Dutch: nl
Greek: el
Turkish: tr'''