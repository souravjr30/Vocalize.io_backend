import os
import pygame
import torch
from TTS.api import TTS

class TTSEngine:
    def __init__(self, speaker_wav_path=None, output_dir="audio"):
        self.speaker_wav_path = speaker_wav_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        #self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=(device == "cuda"))
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        self.tts.to(device)
    
    def text_to_speech(self, text, filename="output.wav", speaker_wav=None, language="en"):
        filepath = os.path.join(self.output_dir, filename)
        if speaker_wav and not os.path.exists(speaker_wav):
            print(f"Error: File not found at {speaker_wav}")
            return None
        # Generate speech
        self.tts.tts_to_file(text=text, file_path=filepath, speaker_wav=speaker_wav, language=language)
        print(f"Speech generated and saved to {filepath}")
        return filepath
    
    def play_audio(self, filepath):
        self.play_sound(filepath)
    
    def play_sound(self, file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

'''import os
import pygame
import torch
import pickle
from TTS.api import TTS

class TTSEngine:
    def __init__(self, speaker_wav_path=None, output_dir="audio", use_gpu=True):
        self.speaker_wav_path = speaker_wav_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Enable GPU if available
        self.device = "cuda" if torch.cuda.is_available() and use_gpu else "cpu"
        
        # Load XTTS model
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=(self.device == "cuda"))
        self.tts.to(self.device)
        
        # Precompute speaker embedding (if provided)
        self.speaker_embedding = None
        if speaker_wav_path:
            self.precompute_speaker_embedding()

    def precompute_speaker_embedding(self):
        """Extracts speaker embedding once and saves it for reuse"""
        if os.path.exists(self.speaker_wav_path):
            gpt_cond_latent, self.speaker_embedding = self.tts.get_conditioning_latents(audio_path=[self.speaker_wav_path])


            with open("speaker_embedding.pkl", "wb") as f:
                pickle.dump(self.speaker_embedding, f)
            print("✅ Speaker embedding precomputed and saved!")
        else:
            print(f"⚠️ Speaker WAV file not found at {self.speaker_wav_path}")

    def text_to_speech(self, text, filename="output.wav", language="en"):
        """Generates speech using precomputed speaker embedding"""
        filepath = os.path.join(self.output_dir, filename)

        if self.speaker_embedding is None and self.speaker_wav_path:
            with open("speaker_embedding.pkl", "rb") as f:
                self.speaker_embedding = pickle.load(f)
        
        # Generate speech (optimized settings)
        self.tts.tts_to_file(
            text=text, 
            file_path=filepath,
            gpt_cond_latent=self.gpt_cond_latent, 
            speaker_embedding=self.speaker_embedding,
            language=language,
            sample_rate=16000  # Reduced sample rate for faster processing
        )

        print(f"🎤 Speech generated and saved to {filepath}")
        return filepath
    
    def play_audio(self, filepath):
        """Plays the generated audio"""
        self.play_sound(filepath)

    def play_sound(self, file_path):
        """Plays sound using pygame"""
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)'''

# Example Usage
'''if __name__ == "__main__":
    tts_engine = TTSEngine(speaker_wav_path="reference_voice.wav")
    audio_file = tts_engine.text_to_speech("Hello, this is a faster voice cloning test!", "cloned_voice.wav")
    tts_engine.play_audio(audio_file)'''
