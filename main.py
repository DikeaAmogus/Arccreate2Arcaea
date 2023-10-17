import os
import re
import yaml
import json
import time
import shutil
from search import getArtist
from server.getServerFiles import moveFilesToDatabase
from server.getServerFiles import cleanTrash

def get_ratingClass(chart, getChartDesigner, getJacketDesigners):
    alias = (
        re.sub(r"<.*?>", "", chart.get("alias", chart.get("charter", "")))
        .split("\n", 1)[0]
        .replace(">-", "")
        .replace("\u000b", "")
        .strip()
    )
    chartDesigner = getChartDesigner[chart["chartPath"]] = alias
    jacketDesigner = getJacketDesigners[chart["chartPath"]] = chart.get(
        "illustrator", ""
    ).replace("\u000b", "")
    if jacketDesigner == "-":
        jacketDesigner = ""
    rating = int(chart.get("chartConstant", 0))
    rating_decimal = rating % 1
    ratingPlus = rating_decimal >= 0.7 and not (
        int(rating) <= 9 and float(rating) <= 9.6
    )
    getRatingClasses = {
        "ratingClass": int(chart["chartPath"][0]),
        "chartDesigner": chartDesigner,
        "jacketDesigner": jacketDesigner,
        "rating": rating,
    }
    if ratingPlus:
        getRatingClasses["ratingPlus"] = True
    audioPath = chart.get("audioPath", "")
    jacketPath = chart.get("jacketPath", "")
    audioOverride = f"{chart['chartPath'][0]}.ogg"
    jacketOverride = f"{chart['chartPath'][0]}.jpg"
    if audioOverride in audioPath:
        getRatingClasses["audioOverride"] = True
    if jacketOverride in jacketPath:
        getRatingClasses["jacketOverride"] = True
    return getRatingClasses

def get_bgName(backgroundPath):
    bgName = os.path.splitext(backgroundPath)[0]
    patterns = [r"_?simple", r"arccreate_+", r" \(1\)", r"\s+"]
    replace = ["", "", "", "_"]
    for pattern, replacement in zip(patterns, replace):
        bgName = re.sub(pattern, replacement, bgName)
    bg = bgName.lower()
    bg_inverse = (
        bg.replace("light", "conflict")
        if "light" in bg
        else bg.replace("conflict", "light")
        if "conflict" in bg
        else ""
    )
    if bg == "yugamu":
        bg_inverse = "rei"
    elif bg == "rei":
        bg_inverse = "yugamu"
    elif bg == "zettai":
        bg_inverse = "zettai_light"
    elif bg == "zettai_light":
        bg_inverse = "zettai"
    return bgName, bg_inverse

def dump_songlist(dir, serverSide=True, offlineSide=False, copy_dir=None):
    combined_songlist = {"songs": []}
    date = int(time.time())
    getChartDesigner = {}
    getJacketDesigners = {}
    copy_folder = None
    if serverSide and copy_dir:
        copy_folder = os.path.join(copy_dir, "database", "songs")
        os.makedirs(copy_folder, exist_ok=True)
        print(
            "Moved folders to database/songs outside the directory and deleted some files."
        )
    for root, dirs, files in os.walk(dir):
        for filename in files:
            if filename.endswith(".arcproj"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    arcproj_data = yaml.safe_load(file)
                chart = arcproj_data["charts"][0]
                artist = chart["composer"]
                title_localized = chart["title"]
                search_artist = getArtist.search_artist(artist)
                backgroundPath = chart.get("backgroundPath", "")
                bg, bg_inverse = get_bgName(backgroundPath)
                bpm_text = chart["bpmText"]
                audioPreview = chart.get("previewStart", 0)
                audioPreviewEnd = chart.get("previewEnd", 19666)
                side = {"light": 0, "conflict": 1, "colorless": 2}.get(
                    chart.get("skin", {}).get("side", ""), 0
                )
                songlist = {
                    "id": cleanTrash(os.path.basename(root)),
                    "title_localized": {"en": title_localized},
                    "artist": artist,
                    "search_artist": search_artist if search_artist else None,
                    "bpm": f"{bpm_text}",
                    "bpm_base": chart["baseBpm"],
                    "set": "base",
                    "purchase": "",
                    "audioPreview": audioPreview,
                    "audioPreviewEnd": audioPreviewEnd,
                    "side": side,
                    "bg": bg,
                    "bg_inverse": bg_inverse,
                    "version": "5.0",
                    "date": date,
                    "difficulties": [],
                }
                has_difficulty = [False] * 4
                for chart in arcproj_data["charts"]:
                    chart_path = chart["chartPath"]
                    ratings = re.match(r"\d+", chart_path)
                    if ratings is None:
                        continue
                    ratings = int(ratings[0])
                    if ratings > 3:
                        continue
                    has_difficulty[ratings] = True
                    getRatingClasses = get_ratingClass(
                        chart, getChartDesigner, getJacketDesigners
                    )
                    songlist["difficulties"].append(getRatingClasses)
                for i in range(4):
                    if not has_difficulty[i] and i != 3:
                        songlist["difficulties"].insert(
                            i,
                            {
                                "ratingClass": i,
                                "chartDesigner": "",
                                "jacketDesigner": "",
                                "rating": 0,
                            },
                        )
                if has_difficulty[2] and not has_difficulty[3]:
                    songlist["difficulties"] = [
                        difficulty
                        for difficulty in songlist["difficulties"]
                        if difficulty["ratingClass"] != 3
                    ]
                date += 1
                if bg_inverse == "":
                    del songlist["bg_inverse"]
                combined_songlist["songs"].append(songlist)
                if serverSide and copy_folder:
                    for folder in os.listdir(dir):
                        folder_path = os.path.join(dir, folder)
                        if os.path.isdir(folder_path):
                            shutil.move(folder_path, copy_folder)
                    moveFilesToDatabase(
                        copy_folder, [".jpg", ".arcproj", ".txt", ".json", ".arcpkg"]
                    )
    for song in combined_songlist["songs"]:
        if song["bg"] == "nijuusei_conflict":
            song["bg"] = "nijuusei-conflict-b"
            song["bg_inverse"] = "nijuusei-light-b"
        elif song["bg"] == "nijuusei_light":
            song["bg"] = "nijuusei-light-b"
            song["bg_inverse"] = "nijuusei-conflict-b"
        if not song["search_artist"]:
            del song["search_artist"]
    if not offlineSide:
        dump_songlist = os.path.join(dir, "songlist")
        with open(dump_songlist, "w", encoding="utf-8") as combined_file:
            json.dump(combined_songlist, combined_file, indent=2, ensure_ascii=False)
        print("Dumped.")

def main():
    dir = "f:/test/mcr"  #Set your dir here
    copy_dir = "f:/test"
    options = {
        "1": ("Dump songlist for non-server", dump_songlist, (dir, False, False)),
        "2": (
            "Dump songlist for server (will move some necessary files. 25% done)",
            dump_songlist,
            (dir, True, True, copy_dir),
        ),
    }
    while True:
        print("\n".join(f"{key}. {option[0]}" for key, option in options.items()))
        option = input("Please choose an option: ")
        if option in options:
            options[option][1](*options[option][2])
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()