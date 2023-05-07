import tidalapi
import datetime
import yaml
import argparse
import os
import logging

parser = argparse.ArgumentParser(
                    prog='Convert rekordbox to tidal')
parser.add_argument('-f', '--file')      # option that takes a value
args = parser.parse_args()

# login_details = {"token_type": None, "access_token": None, "refresh_token": None, "expiry_time": None}

# try:
#     with open(r'C:\Users\yuval\tidal_creds.yaml') as file:
#         login_details_temp = yaml.full_load(file)
#         if(login_details_temp):
#             login_details = login_details_temp

# except:
#     pass

# session = tidalapi.Session()

# if login_details["access_token"]:
#     session.load_oauth_session(login_details["token_type"], login_details["access_token"], login_details["refresh_token"], datetime.datetime.fromtimestamp(login_details["expiry_time"]))
# else:
#     # Will run until you visit the printed url and link your account
#     session.login_oauth_simple()



# login_details['token_type'] = session.token_type
# login_details['access_token'] = session.access_token
# login_details['refresh_token'] = session.refresh_token # Not needed if you don't care about refreshing
# login_details['expiry_time'] = session.expiry_time.timestamp()

# print(login_details)
# with open(r'C:\Users\yuval\tidal_creds.yaml', 'w') as file:
#     documents = yaml.dump(login_details, file)

tidal_tracks = []

# for line in open(args.file, "rb"):
#     print(line)

import xml.etree.ElementTree as ET

# down_path = "C:/users/yuval/Music/tidal/"
down_path =  os.path.join(os.path.expanduser("~"), "\\Music\\tidal\\")

import subprocess

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

for track in root.findall("COLLECTION")[0].iter("TRACK"):
    # track = tracks[i]
    print(track.get("Location"))
    if track.get("Location").startswith("file://localhost/tidal:tracks:"):
        track_id = track.get("Location").split(":", 3)[3]
        print(track.get("Name"))
        track_path = download_track(int(track_id))
        if track_path:
            track.set("Location", "file://localhost/" + track_path)
        # print(track.get("Location"))

tree.write("collection_offline.xml", encoding="utf-8", xml_declaration=True)
