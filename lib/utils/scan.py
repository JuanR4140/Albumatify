from os import listdir

def scan_path(path):
    tracks = {}
    """
    tracks = {
        "Track": {
            "Disc": 1,
            "Track No": 1
        },
        "Other Track": {
            "Disc": 2,
            "Track No": 1
        }
    }
    """
    i = 1
    for track in listdir(path):
        if not track.endswith(".mp3"):
            continue
        tracks[track] = {
                    "Disc": 1,
                    "Track": i
                }
        i += 1
    return tracks

