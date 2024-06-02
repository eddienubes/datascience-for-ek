import asyncio
import aiofiles.os as aioos
import json

from project4.audio_editor import AudioEditor
from project4.ffmpeg_client import FfmpegClient
from project4.rezka_api_client import MediaApiClient
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image, ImageEnhance
from scipy.ndimage import gaussian_gradient_magnitude
import matplotlib.pyplot as plt
import numpy as np

from project4.whisperx_model import WhisperXModel

SOURCE_FILENAME = 'source.wav'
NO_SILENCE_FILENAME = 'no_silence.wav'
TRANSCRIPTION_FILENAME = 'transcription.json'
IMAGE_SOURCE = 'walter.png'


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

    if not await aioos.path.exists(NO_SILENCE_FILENAME):
        audio_editor = AudioEditor(SOURCE_FILENAME)
        audio_editor.remove_silence(NO_SILENCE_FILENAME)

    if not await aioos.path.exists(TRANSCRIPTION_FILENAME):
        transcription = WhisperXModel().transcribe(NO_SILENCE_FILENAME)
        with open(TRANSCRIPTION_FILENAME, "w") as f:
            json.dump(transcription, f, indent=4)

    with open(TRANSCRIPTION_FILENAME, "r") as json_file:
        transcription = json.load(json_file)['segments']

    text = ' '.join([item['text'].strip() for item in transcription])

    walter_image = Image.open(IMAGE_SOURCE)
    enhancer = ImageEnhance.Color(walter_image)
    walter_color = enhancer.enhance(1.5)  # Increase color saturation

    enhancer = ImageEnhance.Brightness(walter_color)
    walter_color = enhancer.enhance(1.2)  # Increase brightness

    walter_color = np.array(walter_color)

    walter_mask = walter_color.copy()
    walter_mask[walter_mask.sum(axis=2) == 0] = 255

    edges = np.mean([gaussian_gradient_magnitude(walter_color[:, :, i] / 255., 2) for i in range(3)], axis=0)
    walter_mask[edges > .06] = 255

    wc = WordCloud(max_words=2000, mask=walter_mask, max_font_size=40, random_state=42, relative_scaling=0)

    # generate word cloud
    wc.generate(text)
    plt.imshow(wc)

    # create coloring from image
    image_colors = ImageColorGenerator(walter_color)
    wc.recolor(color_func=image_colors)
    plt.figure(figsize=(10, 10))
    plt.imshow(wc, interpolation="bilinear")
    wc.to_file("walter_wordcloud.png")

    # plt.figure(figsize=(10, 10))
    # plt.title("Original Image")
    # plt.imshow(walter_color)

    plt.figure(figsize=(10, 10))
    plt.title("Edge map")
    plt.imshow(edges)
    plt.show()


asyncio.run(main())
