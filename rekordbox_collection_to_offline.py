import tidalapi
import datetime
import yaml
import argparse
import os
import logging
import sys
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import subprocess

parser = argparse.ArgumentParser(
                    prog='Convert rekordbox to tidal')
parser.add_argument('-f', '--file')
args = parser.parse_args()

down_path =  os.path.join(os.path.expanduser("~"), "Music\\tidal\\")

def download_track(track_id):
    try:
        os.remove(f"{down_path}/path.txt")
    except:
        pass
    result = subprocess.run(["tidal-dl", "-l", str(track_id), "-o", down_path], text=True)
    try:
        with open(f"{down_path}/path.txt", "rb") as f:
            path = f.read(2000)
        if path:
            return os.path.abspath(path.decode("utf-8"))
    except:
        return None

tree = ET.parse(args.file)
root = tree.getroot()

tracks = root.findall("COLLECTION")[0].findall("TRACK")

def find_duplicates(new_track, track_path):
    duplicates = []
    # Search for tracks with the same file path in the collection
    for track in tracks:
        try:
            if os.path.samefile(unquote(track.get("Location").replace("file://localhost/", "")), track_path):
                print("found duplicate", track, new_track)
                duplicates.append(track)
        except:
            pass

    output_track = new_track
    num_children = len({t for t in new_track})

    # Find the duplicate track with the most children (hotcues, beatgrid adjustments)
    for duplicate in duplicates:
        if len({t for t in duplicate}) > num_children:
            num_children = len({t for t in duplicate})
            output_track = duplicate

    return (duplicates, output_track)

def merge_tracks(duplicates, target):
    # Delete all of the unrelevatnt
    # for playlist in root.findall("PLAYLISTS")[0].findall("NODE").iter("NODE"):
    relevant_ids = {duplicate.get("TrackID") for duplicate in duplicates}
    target_id = target.get("TrackID")

    print(relevant_ids, "target", target_id)
    for duplicate in duplicates:
        if duplicate != target:
            root.findall("COLLECTION")[0].remove(duplicate)

    for track in root.findall("PLAYLISTS")[0].iter("TRACK"):
        # print(track.get("Key"))
        if track.get("Key") in relevant_ids:
            print("relevant", track.get("Key"))
            track.set("Key", target_id)


# Iterate over all tracks, download TIDAL ones and merge duplicates
# Duplciates will happen when importing an offline TIDAL track the collection. 
for track in root.findall("COLLECTION")[0].iter("TRACK"):
    if track.get("Location").startswith("file://localhost/tidal:tracks:"):
        track_id = track.get("Location").split(":", 3)[3]
        print(track.get("Name"))
        track_path = download_track(int(track_id))
        if track_path:
            track.set("Location", "file://localhost/" + track_path)
            duplicates, target_track = find_duplicates(track, track_path)
            merge_tracks(duplicates, target_track)


tree.write("collection_offline.xml", encoding="utf-8", xml_declaration=True)
