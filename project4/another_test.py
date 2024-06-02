import asyncio
import whisperx
import json


async def main():
    device = "cpu"
    audio_file = "audio1.wav"
    batch_size = 16
    compute_type = "int8"

    model = whisperx.load_model("large-v2", device, compute_type=compute_type, language="en")

    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)

    with open("output.json", "w") as f:
        json.dump(result, f, indent=4)
    # print(result["segments"])

    # model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    # result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    # print(result["segments"])  # after alignment

    # delete model if low on GPU resources
    # import gc; gc.collect(); torch.cuda.empty_cache(); del model_a


asyncio.run(main())
