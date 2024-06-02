from pydub import AudioSegment
from pydub.silence import split_on_silence


class AudioEditor:
    def __init__(self, audio_file: str, format: str = "wav"):
        self.audio_file = audio_file
        self.format = format
        self.source = AudioSegment.from_file(audio_file, format=format)

    def remove_silence(self, export_path: str, min_silence_len: int = 1000, silence_thresh: int = -45,
                       keep_silence: int = 150):
        chunks = split_on_silence(self.source,
                                  min_silence_len=min_silence_len,
                                  silence_thresh=silence_thresh,
                                  keep_silence=keep_silence)
        concatenated_audio = AudioSegment.empty()
        for chunk in chunks:
            concatenated_audio += chunk
        # Export concatenated audio to a file
        concatenated_audio.export(export_path, format="wav")
