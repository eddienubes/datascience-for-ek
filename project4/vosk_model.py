from vosk import Model, KaldiRecognizer
import json


class VoskModel:
    def __init__(self, sample_rate: int):
        self.model = Model(lang="en-us", model_path="../models/vosk-model-en-us-0.22")
        self.rec = KaldiRecognizer(self.model, sample_rate)

    def transcribe(self, wav_chunk: bytes, partial: bool = False) -> str | None:
        if self.rec.AcceptWaveform(wav_chunk):
            result = json.loads(self.rec.Result())
            return result['text']

        if partial:
            result = json.loads(self.rec.PartialResult())
            return result['partial']

        return None
