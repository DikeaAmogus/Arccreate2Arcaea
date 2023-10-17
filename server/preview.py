import os
import json
from pydub import AudioSegment

directory = "" #filepath
for folder in os.listdir(directory):
    folder_path = os.path.join(directory, folder)
    if os.path.isdir(folder_path):
        base_file = os.path.join(folder_path, "base.ogg")
        audio = AudioSegment.from_file(base_file, format="ogg")
        json_file = os.path.join(folder_path, "songlist")
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)
        audio_preview_start = data["audioPreview"]
        audio_preview_end = data["audioPreviewEnd"]
        preview_audio = audio[audio_preview_start:audio_preview_end]
        preview_audio = preview_audio.fade_in(1250).fade_out(1750)
        preview_audio = preview_audio.set_frame_rate(44100)
        preview_audio = preview_audio.set_channels(2)
        preview_audio = preview_audio.set_sample_width(2)
        preview_file = os.path.join(folder_path, "preview.ogg")
        preview_audio.export(preview_file, format="ogg", bitrate="192k")
