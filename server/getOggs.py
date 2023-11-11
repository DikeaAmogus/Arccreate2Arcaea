import os
from pydub import AudioSegment
from pydub.exceptions import PydubException
from search.blacklistFolder import checkFolders


def getOggs(dir):
    getErrorFiles = []
    for root, dirs, files in os.walk(dir):
        dirs[:] = [d for d in dirs if d not in checkFolders()]
        for file in files:
            if file == "base.ogg":
                file_path = os.path.join(root, file)
                placeholderFile = os.path.join(root, "base-1.ogg")
                try:
                    ogg_file = AudioSegment.from_ogg(file_path)
                    sample_rate = 44100
                    channels = 2
                    bitrate = "192k"
                    resampled = ogg_file.set_frame_rate(sample_rate).set_channels(
                        channels
                    )
                    resampled.export(placeholderFile, format="ogg", bitrate=bitrate)
                    os.remove(file_path)
                    os.rename(placeholderFile, file_path)
                except PydubException as e:
                    print(f"Error processing file: {file_path}")
                    print(f"Error message: {str(e)}")
                    getErrorFiles.append(file_path)
            elif (
                file.endswith(".ogg")
                and file.split(".")[0].isdigit()
                and int(file.split(".")[0]) in range(4)
            ):
                file_path = os.path.join(root, file)
                placeholderFile = os.path.join(root, f"{file.split('.')[0]}-1.ogg")
                try:
                    ogg_file = AudioSegment.from_ogg(file_path)
                    sample_rate = 44100
                    channels = 2
                    bitrate = "192k"
                    resized_ogg = ogg_file.set_frame_rate(sample_rate).set_channels(
                        channels
                    )
                    resized_ogg.export(placeholderFile, format="ogg", bitrate=bitrate)
                    os.remove(file_path)
                    os.rename(placeholderFile, file_path)
                except PydubException as e:
                    print(f"Error processing file: {file_path}")
                    print(f"Error message: {str(e)}")
                    getErrorFiles.append(file_path)

    print("Files that couldn't be processed:")
    for file_path in getErrorFiles:
        print(file_path)
    print(
        "\nFor oggs that gave errors during process, please seek for audio conversion webs."
    )
