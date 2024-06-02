import asyncio

from rezka_api_client import RezkaApiClient
import requests
import aiohttp
import ffmpeg


async def main():
    client = RezkaApiClient()
    urls = client.get_stream()
    url = urls[0]
    print(url)
    ffmpeg_instance = ffmpeg.input("pipe:", format='mp4').output(
        "pipe:",
        format="wav",
    )

    async with aiohttp.ClientSession() as session:
        response = await session.get(url, ssl=False)

    bytes = await response.read()
    # write a video file
    with open('video.mp4', 'wb') as f:
        f.write(bytes)

    # ffmpeg_process = ffmpeg_instance.run_async(pipe_stdin=True, pipe_stdout=True)

    # async def read_source():
    #     async for chunk in response.content.iter_chunked(1024):
    #         print('pushing chunk to ffmpeg')
    #         ffmpeg_process.stdin.write(chunk)
    #         await asyncio.sleep(1)
    # 
    # async def read_audio():
    #     while True:
    #         bytes = ffmpeg_process.stdout.read(1024)
    #         print('reading audio')
    #         print(type(bytes))
    #         await asyncio.sleep(1)
    # 
    # await asyncio.gather(read_source(), read_audio())


asyncio.run(main())
