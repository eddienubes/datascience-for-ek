import asyncio


class FfmpegClient:
    SAMPLE_RATE = 44100
    BUFFER_SIZE = 4000

    def __init__(self):
        self.process = None
        self.source = None
        self.destination = None

    async def start(self, source: str, destination: str):
        self.source = source
        self.destination = destination
        self.process = await asyncio.create_subprocess_exec(
            'ffmpeg',
            *[
                '-i',
                source,
                '-ar',
                str(FfmpegClient.SAMPLE_RATE),
                '-ac',
                '1',
                '-acodec',
                'pcm_s16le',
                '-f',
                'wav',
                destination
            ],
            stdin=asyncio.subprocess.PIPE if source == 'pipe:0' else None,
            stdout=asyncio.subprocess.PIPE if destination == 'pipe:1' else None,
            stderr=asyncio.subprocess.PIPE
        )

        return self

    async def write(self, chunk: bytes) -> None:
        if self.source != 'pipe:0':
            raise ValueError('Source must be pipe:0 to write')

        self.process.stdin.write(chunk)

    async def get_stream(self):
        if self.destination != 'pipe:1':
            raise ValueError('Destination must be pipe:1 to get stream')

        while True:
            wav_chunk = await self.process.stdout.read(FfmpegClient.BUFFER_SIZE)
            if not wav_chunk:
                return
            yield wav_chunk
