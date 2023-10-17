import os

def rename_folders(directory, option):
    blacklist = [
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
    for folder in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, folder)):
            if folder not in blacklist:
                if option == "1" and not folder.startswith("dl_"):
                    add = "dl_" + folder
                    os.rename(
                        os.path.join(directory, folder),
                        os.path.join(directory, add),
                    )
                elif option == "2" and folder.startswith("dl_"):
                    add = folder[3:]
                    os.rename(
                        os.path.join(directory, folder),
                        os.path.join(directory, add),
                    )


dir = "C:\\Users\\DELL\\Downloads\\wdl"

option = input("1. Add dl_\n2. Remove dl_\nChoose: ")

rename_folders(dir, option)
