import os
import shutil
from server.getOggs import getOggs
from server.preview import getPreview, getImg_1080, getBgs
from songlist.songlist import dumpSonglist
from server.getServerFiles import dl_, moveFilesToDatabase
from search.getBgs import resizeBgs

# dir = input("Path to process: ")

def main():
    dir = "f:/test/mcr"
    copyDir = os.path.dirname(dir)
    options = {
        "1": ("Dump songlist for non-server (Arccreate-side)", dumpSonglist, (dir, False)),
        "2": (
            "Dump songlist for server (Arccreate-side)",
            dumpSonglist,
            (dir, True),
        ),
        "3": (
            """Get existing files for server (Arcaea-side).
 Please include songlist when choosing this option""",
            (),
        ),
        "4": (
            "Get existing files for non-server (Arcaea-side)",
            (),
        ),
    }
    while True:
        print("\n".join(f"{key}. {option[0]}" for key, option in options.items()))
        option = input("Please choose an option: ")
        if option in options:
            if len(options[option]) > 2:
                options[option][1](*options[option][2])
            if option == "1":
                getOggs(dir)
                getBgs(dir)
                getImg_1080(dir)
                resizeBgs(dir)
                print("You might want to double check the folders and songlist.")
            elif option == "2":
                getOggs(dir)
                getBgs(dir)
                getImg_1080(dir)
                resizeBgs(dir)
                getPreview(dir)
                moveFolder = os.path.join(copyDir, "database", "songs")
                os.makedirs(moveFolder, exist_ok=True)
                for folder in os.listdir(dir):
                    folderPath = os.path.join(dir, folder)
                    if os.path.isdir(folderPath):
                        shutil.copytree(folderPath, os.path.join(moveFolder, folder))
                moveFilesToDatabase(
                    moveFolder, [".jpg", ".arcproj", ".txt", ".json", ".arcpkg"]
                )
                dl_(dir)
                print("You might want to double check the folders and songlist.")
            elif option == "3":
                getOggs(dir)
                getBgs(dir)
                getImg_1080(dir)
                resizeBgs(dir)
                getPreview(dir)
                moveFolder = os.path.join(copyDir, "database", "songs")
                os.makedirs(moveFolder, exist_ok=True)
                for folder in os.listdir(dir):
                    folderPath = os.path.join(dir, folder)
                    if os.path.isdir(folderPath):
                        shutil.copytree(folderPath, os.path.join(moveFolder, folder))
                moveFilesToDatabase(
                    moveFolder, [".jpg", ".arcproj", ".txt", ".json", ".arcpkg"]
                )
                dl_(dir)
            elif option == "4":
                getOggs(dir)
                getBgs(dir)
                getImg_1080(dir)
                resizeBgs(dir)
            break
        else:
            print("Choose.")


if __name__ == "__main__":
    main()
