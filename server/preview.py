import os
import json
from pydub import AudioSegment

def getPreview(dir):
    songlistPath = os.path.join(dir, "songlist")
    with open(songlistPath, "r", encoding="utf-8") as songlist:
        getData = json.load(songlist)
    
    for song in getData["songs"]:
        id = song["id"]
        startTime = song["audioPreview"]
        endTime = song["audioPreviewEnd"]
        folderPath = os.path.join(dir, id)
        getBaseOgg = os.path.join(folderPath, "base.ogg")
        pvPath = os.path.join(folderPath, "preview.ogg")
        
        if os.path.exists(getBaseOgg) and not os.path.exists(pvPath):
            audio = AudioSegment.from_file(getBaseOgg, format="ogg")
            samplingRate = 44100
            channels = 2
            codec = "libvorbis"
            audio = audio.set_frame_rate(samplingRate)
            audio = audio.set_channels(channels)
            preview = audio[startTime:endTime]
            fadeIn = 1250
            fadeOut = 1750
            preview = preview.fade_in(fadeIn).fade_out(fadeOut)
            preview.export(pvPath, format="ogg", codec=codec, bitrate="192k")