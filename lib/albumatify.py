from os.path import isdir, isfile
from rich.table import Table

from lib.utils.scan import scan_path
from lib.utils.check_for_existing_tracks import check_for_existing_track
from lib.utils.non_fatal_error import throw_non_fatal_error

discs = 1

def albumatify(raw_tracks_path, cover_art_path, getch, console, clear_screen):
    global discs
    tracks = scan_path(raw_tracks_path)
    
    while True:
        clear_screen()
        
        print("Albumatify\n----------\n")
        print("a - add disc\nr - remove disc\ne - edit a track\nw - save changes\nx - discard changes\n\n")

        tracks = dict(sorted(tracks.items(), key=lambda track: track[1]["Track"]))
        
        counter = 1
        for i in range(discs):
            print(f"Disc {i + 1}")
            table = Table(show_header=True)
            table.add_column("Track No.")
            table.add_column("Track")
           
            for track, properties in tracks.items():
                if properties["Disc"] == i + 1:
                    tracks[track]["Track"] = counter
                    counter += 1
                    table.add_row(str(properties["Track"]), track.replace(".mp3", ""))

            console.print(table)
            console.print("\n\n")
            counter = 1

        console.print("CMD > ", end="")

        char = getch()

        if char == "a":
            discs += 1

        if char == "r":
            if (discs - 1) == 0:
                throw_non_fatal_error("Can not have 0 discs!", console, getch)
                continue

            disc_active = False
            for track, properties in tracks.items():
                if properties["Disc"] == (discs):
                    disc_active = True

            if disc_active:
                throw_non_fatal_error("Can not remove disc with tracks!", console, getch)
                continue

            discs -= 1

        if char == "e":
            source_disc = console.input("What disc are you trying to edit? > ")
            source_track = console.input("What track no. are you trying to edit? > ")

            if int(source_disc) > discs or int(source_disc) < 1:
                throw_non_fatal_error("Source disc does not exist!", console, getch)
                continue

            if not check_for_existing_track(tracks, source_disc, source_track):
                throw_non_fatal_error("Source track does not exist!", console, getch)
                continue

            console.print("\n")

            target_disc = console.input("What disc should this track be moved to? > ")
            target_track = console.input("What track no. should this track be set to? > ")

            if int(target_disc) > discs or int(target_disc) < 1:
                throw_non_fatal_error("Target disc does not exist!", console, getch)
                continue


            console.print("\n")

            source_track_key = check_for_existing_track(tracks, source_disc, source_track)
            existing_track_key = check_for_existing_track(tracks, target_disc, target_track)

            if source_track_key == existing_track_key:
                continue

            if existing_track_key:

                tracks[existing_track_key]["Disc"] ^= tracks[source_track_key]["Disc"]
                tracks[source_track_key]["Disc"] ^= tracks[existing_track_key]["Disc"]
                tracks[existing_track_key]["Disc"] ^= tracks[source_track_key]["Disc"]

                tracks[existing_track_key]["Track"] ^= tracks[source_track_key]["Track"]
                tracks[source_track_key]["Track"] ^= tracks[existing_track_key]["Track"]
                tracks[existing_track_key]["Track"] ^= tracks[source_track_key]["Track"]

            else:
                
                tracks[source_track_key]["Disc"] = int(target_disc)
                tracks[source_track_key]["Track"] = int(target_track)

        if char == "x":
            console.print("Are you sure you want to exit? All changes will be lost! (y/n) > ", end="")
            if getch() == "y":
                clear_screen()
                exit()
