import json
import whisperx


class WhisperXModel:
    def __init__(self):
        # Optimized for macbook pro m1 max
        self.device = "cpu"
        self.faudio_file = "audio1.wav"
        self.batch_size = 16
        self.compute_type = "int8"

        self.model = whisperx.load_model("large-v2", self.device, compute_type=self.compute_type, language="en")

    def transcribe(self, audio_file: str) -> str | None:
        audio = whisperx.load_audio(audio_file)
        result = self.model.transcribe(audio, batch_size=self.batch_size)

        return result
