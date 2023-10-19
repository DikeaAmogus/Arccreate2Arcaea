import os
import re
import shutil


def cleanTrash(string):
    return re.sub(r"['_\s()-]", "", string.strip()).lower()


def moveFilesToDatabase(dir, extensions):
    for root, dirs, files in os.walk(dir):
        for filename in files:
            if any(filename.endswith(ext) for ext in extensions) or filename in [
                "songlist",
                "remote.aff",
                "preview.ogg",
            ]:
                filePath = os.path.join(root, filename)
                os.remove(filePath)
        if root != dir:
            getAffs = [
                filename
                for filename in files
                if filename.endswith(".aff") and filename != "remote.aff"
            ]
            if len(getAffs) >= 1:
                getRating = int(getAffs[0].split(".")[0])
                for ratingClass in range(getRating):
                    affPath = os.path.join(root, f"{ratingClass}.aff")
                    if not os.path.exists(affPath):
                        with open(affPath, "w", encoding="utf-8") as fillerAff:
                            fillerAff.write(
                                "AudioOffset:0\n-\ntiming(0,128.00,4.00);\n(15000,4);\n(16875,3);\n(18750,2);\n(20625,1);\nhold(30000,31875,3);\nhold(33750,35625,2);\nhold(37500,38437,4);\nhold(39375,40312,1);\narc(52500,54375,1.00,1.00,s,1.00,1.00,1,none,false);\narc(56250,60000,0.00,0.00,s,1.00,1.00,0,none,false);\narc(67500,69375,1.00,0.00,s,1.00,1.00,1,none,false);\narc(71250,73125,0.00,1.00,b,1.00,1.00,0,none,false);\narc(75000,76875,0.00,1.00,so,1.00,1.00,0,none,false);\narc(76875,77812,1.00,0.50,s,1.00,1.00,0,none,false);\narc(78750,80625,1.00,0.00,s,1.00,1.00,1,none,false);\narc(80625,82500,0.00,1.00,si,1.00,1.00,1,none,false);\narc(90000,91875,0.00,0.00,s,1.00,1.00,0,none,false);\narc(90000,91875,1.00,0.50,s,1.00,1.00,1,none,false);\narc(91875,93750,0.00,0.50,s,1.00,1.00,0,none,false);\narc(91875,93750,0.50,1.00,s,1.00,1.00,1,none,false);\narc(93750,95625,0.50,0.00,s,1.00,1.00,0,none,false);\narc(93750,95625,1.00,1.00,s,1.00,1.00,1,none,false);\narc(95625,97500,1.00,0.50,s,1.00,1.00,1,none,false);\narc(95625,97500,0.00,0.50,s,1.00,1.00,0,none,false);\n(105000,4);\n(105937,4);"
                            )
        if root != dir:
            rmAdeFolder = os.path.join(root, "Arcade")
            if os.path.exists(rmAdeFolder):
                shutil.rmtree(rmAdeFolder)
            else:
                rmAdeFolder = os.path.join(root, "arcade")
                if os.path.exists(rmAdeFolder):
                    shutil.rmtree(rmAdeFolder)
    renameFolders = [
        os.path.join(dir, d.lower())
        for d in os.listdir(dir)
        if os.path.isdir(os.path.join(dir, d))
    ]
    for folder in renameFolders:
        os.rename(folder, os.path.join(dir, cleanTrash(os.path.basename(folder))))
    return moveFilesToDatabase


def dl_(dir):
    whitelist = [".jpg", ".arcproj", ".txt", ".json", ".arcpkg", ".aff", ".ogg"]
    blacklist = ["base.jpg", "base_256.jpg", "preview.ogg"]
    blacklistFolder = [
        "sayonarahatsukoi",
        "pack",
        "random",
        "dl_arcanaeden",
        "dl_tempestissimo",
        "dl_testify",
        "dl_fractureray",
        "dl_grievouslady",
        "dl_defection",
        "dl_infinitestrife",
        "dl_last",
        "dl_lasteternity",
        "dl_lovelessdress",
        "dl_pentiment",
        "dl_worldender",
    ]
    for folder in os.listdir(dir):
        folderPath = os.path.join(dir, folder)
        if os.path.isdir(folderPath) and not folder.startswith("dl_"):
            if folder not in blacklistFolder:
                dlFolder = "dl_" + folder
                smthPath = os.path.join(dir, dlFolder)
                os.rename(folderPath, smthPath)
                for root, dirs, files in os.walk(smthPath):
                    for file in files:
                        file_Path = os.path.join(root, file)
                        file_extension = os.path.splitext(file)[1]
                        if file_extension in whitelist and file not in blacklist:
                            os.remove(file_Path)
    return dl_