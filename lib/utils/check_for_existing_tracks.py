def check_for_existing_track(tracks, disc, track_no):
    for track, properties in tracks.items():
        if int(properties["Disc"]) == int(disc) and int(properties["Track"]) == int(track_no):
            return track

    return None
