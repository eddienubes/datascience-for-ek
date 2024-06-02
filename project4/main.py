import asyncio

import aiofiles
import aiofiles.os as aioos

from project4.ffmpeg_client import FfmpegClient
from project4.rezka_api_client import MediaApiClient
from project4.vosk_model import VoskModel
from pydub import AudioSegment
from pydub.silence import split_on_silence

SOURCE_FILENAME = 'audio1.wav'
CLEAN_FILENAME = 'clean.wav'


async def main():
    client = MediaApiClient()
    # urls = client.get_stream()
    # url = urls[0]
    url = 'https://stream.voidboost.cc/7c9970e77e144225f2ffbe049f817a97:2024060305:UTRTUlRKZklmenZ0dkR5bDV6SzlqZHF3R0dyQ0UrVVUwSXNRNyswUCtURURyTTVMRzBibm03djVTaE1qUHgvaGxPaVZNbWFCbFJ2SGQ4cDI0UVBDMFhOMnR5TG1wT3lXankyc1FoaUZpVnc9/9/1/6/2/4/4/47zhg.mp4'
    mp4_stream = client.get_mp4_stream(url)

    ffmpeg = FfmpegClient()

    if not await aioos.path.exists(SOURCE_FILENAME):
        await ffmpeg.start('pipe:0', SOURCE_FILENAME)
        async for chunk in client.get_mp4_stream(url):
            await ffmpeg.write(chunk)

    # Load the audio file
    print('analysing audio')
    audio = AudioSegment.from_file(SOURCE_FILENAME, format='wav')

    # Split audio where silence is 1000ms or more and get chunks
    chunks = split_on_silence(audio,
                              min_silence_len=1000,
                              silence_thresh=-40)

    # Concatenate chunks
    concatenated_audio = AudioSegment.empty()

    for chunk in chunks:
        concatenated_audio += chunk

    # Export concatenated audio to a file
    concatenated_audio.export("output_audio.wav", format="wav")

    # vosk_model = VoskModel(FfmpegClient.SAMPLE_RATE)
    # 
    # # For simplicity let's just read from the file
    # async def write() -> None:
    #     async for chunk in mp4_stream:
    #         await ffmpeg.write(chunk)
    # 
    # async def read():
    #     async for wav_chunk in ffmpeg.get_stream():
    #         result = vosk_model.transcribe(wav_chunk, partial=False)
    #         if result:
    #             print(result)

    # await asyncio.gather(read())


asyncio.run(main())
