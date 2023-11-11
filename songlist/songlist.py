import os
import yaml
import time
import json
import re
from search import getArtist
from songlist.bg import getBgName
from server.getServerFiles import cleanTrash
from songlist.ratingClass import getRatingClass


def dumpSonglist(dir, offlineSide=False):
    combinedSonglist = {"songs": []}
    date = int(time.time())
    getChartDesigner = {}
    getJacketDesigners = {}
    for root, dirs, files in os.walk(dir):
        for filename in files:
            if filename.endswith(".arcproj"):
                filePath = os.path.join(root, filename)
                with open(filePath, "r", encoding="utf-8") as file:
                    arcproj_data = yaml.safe_load(file)
                chart = arcproj_data["charts"][0]
                artist = chart["composer"]
                title_localized = chart["title"]
                search_artist = getArtist.search_artist(artist)
                backgroundPath = chart.get("backgroundPath", "")
                bg, bg_inverse = getBgName(backgroundPath)
                bpmText = chart["bpmText"]
                audioPreview = chart.get("previewStart", 0)
                audioPreviewEnd = chart.get("previewEnd", 19666)
                side = {"light": 0, "conflict": 1, "colorless": 2}.get(
                    chart.get("skin", {}).get("side", ""), 0
                )
                if bg == "":
                    if side == 0:
                        bg = "base_light"
                        bg_inverse = "base_conflict"
                    elif side == 1:
                        bg = "base_conflict"
                        bg_inverse = "base_light"
                    elif side == 2:
                        bg = "epilogue"
                songlist = {
                    "id": cleanTrash(os.path.basename(root)),
                    "title_localized": {"en": title_localized},
                    "artist": artist,
                    "search_artist": search_artist if search_artist else None,
                    "bpm": f"{bpmText}",
                    "bpm_base": chart["baseBpm"],
                    "set": "base",
                    "purchase": "",
                    "audioPreview": audioPreview,
                    "audioPreviewEnd": audioPreviewEnd,
                    "side": side,
                    "bg": bg,
                    "bg_inverse": bg_inverse,
                    "remote_dl": offlineSide,
                    "version": "5.0",
                    "date": date,
                    "difficulties": [],
                }
                hasDifficulty = [False] * 4
                for chart in arcproj_data["charts"]:
                    chartPath = chart["chartPath"]
                    ratings = re.match(r"\d+", chartPath)
                    if ratings is None:
                        continue
                    ratings = int(ratings[0])
                    if ratings > 3:
                        continue
                    hasDifficulty[ratings] = True
                    getRatingClasses = getRatingClass(
                        chart, getChartDesigner, getJacketDesigners
                    )
                    songlist["difficulties"].append(getRatingClasses)
                for i in range(4):
                    if not hasDifficulty[i] and i != 3:
                        songlist["difficulties"].insert(
                            i,
                            {
                                "ratingClass": i,
                                "chartDesigner": "",
                                "jacketDesigner": "",
                                "rating": 0,
                            },
                        )
                if hasDifficulty[2] and not hasDifficulty[3]:
                    songlist["difficulties"] = [
                        difficulty
                        for difficulty in songlist["difficulties"]
                        if difficulty["ratingClass"] != 3
                    ]
                date += 1
                renameFolder = cleanTrash(os.path.basename(root)).lower()
                getRenamePath = os.path.join(os.path.dirname(root), renameFolder)
                os.rename(root, getRenamePath)
                if bg_inverse == "":
                    del songlist["bg_inverse"]
                if songlist["remote_dl"] == False:
                    del songlist["remote_dl"]
                combinedSonglist["songs"].append(songlist)
    for song in combinedSonglist["songs"]:
        if song["bg"] == "nijuusei_conflict":
            song["bg"] = "nijuusei-conflict-b"
            song["bg_inverse"] = "nijuusei-light-b"
        elif song["bg"] == "nijuusei_light":
            song["bg"] = "nijuusei-light-b"
            song["bg_inverse"] = "nijuusei-conflict-b"
        if not song["search_artist"]:
            del song["search_artist"] 
    if not offlineSide:
        dumpSonglist = os.path.join(dir, "songlist")
        with open(dumpSonglist, "w", encoding="utf-8") as combinedFile:
            json.dump(combinedSonglist, combinedFile, indent=2, ensure_ascii=False)
        print("Dumped.")
    elif offlineSide:
        dumpSonglist = os.path.join(dir, "songlist")
        with open(dumpSonglist, "w", encoding="utf-8") as combinedFile:
            json.dump(combinedSonglist, combinedFile, indent=2, ensure_ascii=False)
        print("Dumped.")
    return dumpSonglist
