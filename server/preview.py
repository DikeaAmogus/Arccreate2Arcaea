import os
import json
import shutil
from PIL import Image
from pydub import AudioSegment
from classes.getClasses import Resolution
from search.getFiles import loschen


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
            audio = audio.set_frame_rate(samplingRate)
            audio = audio.set_channels(channels)
            audio = audio.set_sample_width(2)
            preview = audio[startTime:endTime]
            fadeIn = 1250
            fadeOut = 1750
            preview = preview.fade_in(fadeIn).fade_out(fadeOut)
            preview.export(pvPath, format="ogg", codec="libvorbis", bitrate="192k")
        for i in range(4):
            oggPath = os.path.join(folderPath, f"{i}.ogg")
            previewPath = os.path.join(folderPath, f"{i}_preview.ogg")
            if os.path.exists(oggPath) and not os.path.exists(previewPath):
                audio = AudioSegment.from_file(oggPath, format="ogg")
                preview = audio[startTime:endTime]
                fadeIn = 1250
                fadeOut = 1750
                preview = preview.fade_in(fadeIn).fade_out(fadeOut)
                preview.export(previewPath, format="ogg", codec="libvorbis", bitrate="192k")

def getImg_1080(dir):
    if Resolution.if_1080:
        folderPath = os.path.join(dir)
        for entry in os.scandir(folderPath):
            if entry.is_dir():
                folderDir = entry.path
                baseImg = os.path.join(folderDir, "base.jpg")
                if not os.path.exists(baseImg):
                    baseImg = os.path.join(folderDir, "base.png")
                if os.path.exists(baseImg):
                    getResizePath = os.path.join(folderDir, "1080_base.jpg")
                    image = Image.open(baseImg).convert("RGB")
                    image = image.resize((768, 768), Image.LANCZOS)
                    image.save(getResizePath, quality=100)
                    getResizePath_256 = os.path.join(folderDir, "1080_base_256.jpg")
                    image = Image.open(getResizePath).convert("RGB")
                    image = image.resize((384, 384), Image.LANCZOS)
                    image.save(getResizePath_256, quality=100)
                for entry in os.scandir(folderDir):
                    if entry.is_file():
                        file_path = entry.path
                        if (
                            entry.name == "0.jpg"
                            or entry.name == "1.jpg"
                            or entry.name == "2.jpg"
                            or entry.name == "3.jpg"
                            or entry.name == "0.png"
                            or entry.name == "1.png"
                            or entry.name == "2.png"
                            or entry.name == "3.png"
                        ):
                            new_name = f"1080_{entry.name}"
                            getFolder = os.path.join(folderDir, new_name)
                            image = Image.open(file_path).convert("RGB")
                            image = image.resize((768, 768), Image.LANCZOS)
                            image.save(getFolder, quality=100)
                            if os.path.exists(file_path):
                                os.remove(file_path)
                            getResizePath_256 = os.path.join(
                                folderDir, f"1080_{entry.name[:-4]}_256.jpg"
                            )
                            image = Image.open(getFolder).convert("RGB")
                            image = image.resize((384, 384), Image.LANCZOS)
                            image.save(getResizePath_256, quality=100)
                loschen(folderDir)


def getBgs(dir):
    bgFolder = os.path.join(os.path.dirname(dir), "bg")
    os.makedirs(bgFolder, exist_ok=True)
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.lower().endswith(("jpg", "png")):
                file_path = os.path.join(root, file)
                with Image.open(file_path) as img:
                    width, height = img.size
                    if width > 1270 and height > 950 and width != height:
                        shutil.copy2(file_path, os.path.join(bgFolder, file))
