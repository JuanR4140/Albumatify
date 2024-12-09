from os.path import isdir, isfile
from rich.table import Table

from lib.utils.scan import scan_path
from lib.utils.check_for_existing_tracks import check_for_existing_track

discs = 1

def albumatify(raw_tracks_path, cover_art_path, getch, console, clear_screen):
    global discs
    tracks = scan_path(raw_tracks_path)
    
    while True:
        clear_screen()
        
        print("Albumatify\n----------\n")
        print("a - add disc\nr - remove disc\ne - edit a track\nw - save changes\nx - discard changes\n\n")

        for i in range(discs):
            print(f"Disc {i + 1}")
            table = Table(show_header=True)
            table.add_column("Track No.")
            table.add_column("Track")
           
            for track, properties in tracks.items():
                if properties["Disc"] == i + 1:
                    table.add_row(str(properties["Track"]), track.replace(".mp3", ""))

            console.print(table)
            console.print("\n\n")

        console.print("CMD > ", end="")

        char = getch()

        if char == "a":
            discs += 1

        if char == "r":
            if (discs - 1) == 0:
                console.print("\n\nCan not have 0 discs!\nPress 'k' to continue.\n\n")
                while True:
                    if getch() == "k":
                        break
                continue
            discs -= 1

        if char == "e":
            source_disc = console.input("What disc are you trying to edit? > ")
            source_track = console.input("What track no. are you trying to edit? > ")

            if int(source_disc) > discs or int(source_disc) < 1:
                console.print("\n\nSource disc does not exist!\nPress 'k' to continue.\n\n")
                while True:
                    if getch() == "k":
                        break
                continue

            if not check_for_existing_track(tracks, source_disc, source_track):
                console.print("\n\nSource track does not exist!\nPress 'k' to continue\n\n")
                while True:
                    if getch() == "k":
                        break
                continue

            console.print("\n")

            target_disc = console.input("What disc should this track be moved to? > ")
            target_track = console.input("What track no. should this track be set to? > ")

            if int(target_disc) > discs or int(target_disc) < 1:
                console.print("\n\nTarget disc does not exist!\nPress 'k' to continue.\n\n")
                while True:
                    if getch() == "k":
                        break
                continue


            console.print("\n")

            existing_track = check_for_existing_track(tracks, target_disc, target_track)
            if existing_track:
                console.print("Track exists.")
            else:
                console.print("Track does not exist.")

            while True:
                if getch() == "k":
                    break
                continue

            # TODO - If track exists, shift it downwards and place source track in its place.

        if char == "x":
            console.print("Are you sure you want to exit? All changes will be lost! (y/n) > ", end="")
            if getch() == "y":
                console.print("\n")
                exit()
