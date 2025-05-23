#code which uses speaker wav of our own ai.wav file (working)
'''import os
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
'''
#code which uses speaker of the model itself (working)
import os
import pygame
import torch
from TTS.api import TTS

class TTSEngine:
    def __init__(self, output_dir="audio", speaker_idx=None):
        #self.speaker_wav_path = speaker_wav_path
        self.output_dir = output_dir
        self.speaker_idx = speaker_idx
        os.makedirs(output_dir, exist_ok=True)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        self.tts.to(device)
    
    def text_to_speech(self, text, filename="output.wav", language='en', speaker=None):
        filepath = os.path.join(self.output_dir, filename)
        # Generate speech
        self.tts.tts_to_file(
            text=text, 
            file_path=filepath,
            speaker=speaker or self.speaker_idx, 
            #speaker_idx=self.speaker_idx, 
            language=language,
            #split_sentences=True
        )
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

