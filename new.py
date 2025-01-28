from TTS.api import TTS
import os

# Initialize the TTS model
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

# File paths
speaker_wav_path = r"C:\Users\soura\Demo\AI.wav"  # Use raw string to avoid escaping issues
output_path = "output.wav"

# Check if the speaker_wav file exists
if not os.path.exists(speaker_wav_path):
    print(f"Error: File not found at {speaker_wav_path}")
else:
    print(f"Using speaker file: {speaker_wav_path}")

    # Generate speech
    tts.tts_to_file(
        text="It took me quite a long time to develop a voice, and now that I have it I'm not going to be silent.",
        file_path=output_path,
        speaker_wav=speaker_wav_path,
        language="en"
    )
    print(f"Speech generated and saved to {output_path}")
