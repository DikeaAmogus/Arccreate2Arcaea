import os

def loschen(folderDir):
    for entry in os.scandir(folderDir):
        if entry.is_file():
            file_path = entry.path
            if (
                entry.name != "base.ogg"
                and entry.name != "0.ogg"
                and entry.name != "1.ogg"
                and entry.name != "2.ogg"
                and entry.name != "3.ogg"
                and entry.name != "0.aff"
                and entry.name != "1.aff"
                and entry.name != "2.aff"
                and entry.name != "3.aff"
                and entry.name != "1080_base.jpg"
                and entry.name != "1080_base_256.jpg"
                and entry.name != "1080_0.jpg"
                and entry.name != "1080_0_256.jpg"
                and entry.name != "1080_1.jpg"
                and entry.name != "1080_1_256.jpg"
                and entry.name != "1080_2.jpg"
                and entry.name != "1080_2_256.jpg"
                and entry.name != "1080_3.jpg"
                and entry.name != "1080_3_256.jpg"
            ):
                loschen = [
                    ".jpg",
                    ".arcproj",
                    ".txt",
                    ".json",
                    ".arcpkg",
                    ".aff",
                    ".ogg",
                    ".DS_Store",
                    ".png",
                ]
                if any(entry.name.lower().endswith(ext) for ext in loschen):
                    if os.path.exists(file_path):
                        aff_file_path = os.path.join(folderDir, entry.name.split(".")[0] + ".aff")
                        aff_number = entry.name.split(".")[0]
                        if aff_number in ["0", "1", "2", "3"]:
                            if os.path.exists(aff_file_path):
                                with open(aff_file_path, "r") as aff_file:
                                    aff_content = aff_file.read()
                                    if (
                                        "_wav" in aff_content
                                        or "_ogg" in aff_content
                                    ):
                                        continue
                            os.remove(file_path)