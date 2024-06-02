import asyncio
import aiofiles
import json
from vosk import Model, KaldiRecognizer, SetLogLevel


async def main():
    SAMPLE_RATE = 44100
    BUFFER_SIZE = 4000

    model = Model(lang="en-us", model_path="../models/vosk-model-en-us-0.22")
    rec = KaldiRecognizer(model, SAMPLE_RATE)

    process = await asyncio.create_subprocess_exec(
        'ffmpeg',
        *[
            '-i',
            'clean_test.wav',
            '-ar',
            str(SAMPLE_RATE),
            '-ac',
            '1',
            '-acodec',
            'pcm_s16le',
            '-f',
            'wav',
            'pipe:1'
        ],
        # stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    while True:
        wav_chunk = await process.stdout.read(BUFFER_SIZE)
        while wav_chunk:
            if rec.AcceptWaveform(wav_chunk):
                result = json.loads(rec.Result())

                print(result.get('text'))
            else:
                raw = rec.PartialResult()
                result = json.loads(raw)
                print(result)
            wav_chunk = await process.stdout.read(BUFFER_SIZE)



asyncio.run(main())
