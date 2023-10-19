import os
import shutil
from server.preview import getPreview
from server.getServerFiles import dl_
from songlist.songlist import dumpSonglist
from server.getServerFiles import moveFilesToDatabase

def main():
    dir = "/path/to/dir/"
    copyDir = "/path/for/database/" #just fall back by 1 folder at the dir var
    options = {
        "1": ("Dump songlist for non-server", dumpSonglist, (dir, False)),
        "2": (
            "Dump songlist for server (will move some necessary files. 66.67% done)",
            dumpSonglist,
            (dir, True),
        ),
        "3": ("Move existing files for server (Arcaea-side) (Not yet completed cuz lazy)"),
    }
    while True:
        print("\n".join(f"{key}. {option[0]}" for key, option in options.items()))
        option = input("Please choose an option: ")
        if option in options:
            options[option][1](*options[option][2])
            if option == "2":
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
            break
        else:
            print("Choose.")

if __name__ == "__main__":
    main()
    
