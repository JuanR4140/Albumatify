from os.path import isdir, isfile
from rich.table import Table
from mutagen.mp3 import MP3
from mutagen.id3 import APIC, ID3, TIT2, TPE1, TALB, TCON, TDRC, TRCK, TPOS, error

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

        if char == "w":
            clear_screen()
            print("Albumatify\n----------\n")
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

            console.print("\nAre you sure you want to write these changes to disk? (y/n) > ", end="")
            if getch() == "y":
                console.print("\n\nSweet! Let's get some more information about your album...")
                album = console.input("Enter name of album > ")
                artist = console.input("Enter name of artist > ")
                genre = console.input("Enter name of genre > ")
                release = console.input("Enter release date > ")

                print("\nWriting changes to disk, please wait....\n")

                progress = 1
                progress_total = len(tracks)

                for track, properties in tracks.items():
                    print(f"Writing metadata for {track}.... ({progress}/{progress_total})")
                    mp3 = raw_tracks_path + track
                    audio = MP3(mp3, ID3=ID3)

                    try:
                        audio.add_tags()
                    except error:
                        pass

                    with open(cover_art_path, "rb") as cover_art:
                        audio.tags.add(
                            APIC(
                                encoding=3,
                                mime="image/jpeg",
                                type=3,
                                desc="Cover",
                                data=cover_art.read(),
                            )
                        )

                    audio["TIT2"] = TIT2(encoding=3, text=track)
                    audio["TPE1"] = TPE1(encoding=3, text=artist)
                    audio["TALB"] = TALB(encoding=3, text=album)
                    audio["TCON"] = TCON(encoding=3, text=genre)
                    audio["TDRC"] = TDRC(encoding=3, text=release)
                    audio["TPOS"] = TPOS(encoding=3, text=f"{properties['Disc']}/{discs}")
                    audio["TRCK"] = TRCK(encoding=3, text=str(properties["Track"]).replace(".mp3", ""))

                    audio.save()
                    progress += 1

                print("\nChanges written to disk successfully!")
                exit()

        if char == "x":
            console.print("Are you sure you want to exit? All changes will be lost! (y/n) > ", end="")
            if getch() == "y":
                clear_screen()
                exit()
