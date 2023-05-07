import tidalapi
import datetime
import yaml
import argparse
import os
import logging
import subprocess

<<<<<<< HEAD
down_path =  os.path.join(os.path.expanduser("~"), "Music\\tidal\\")
=======
down_path =  os.path.join(os.path.expanduser("~"), "\\Music\\tidal\\")
>>>>>>> 7697f2a312d1943e6724a91ceba04f7e150bdd89

parser = argparse.ArgumentParser(
                    prog='Convert rekordbox to tidal')
parser.add_argument('-f', '--file')      # option that takes a value
args = parser.parse_args()

login_details = {"token_type": None, "access_token": None, "refresh_token": None, "expiry_time": None}

try:
    with open(r'C:\Users\yuval\tidal_creds.yaml') as file:
        login_details_temp = yaml.full_load(file)
        if(login_details_temp):
            login_details = login_details_temp

except:
    pass

session = tidalapi.Session()

if login_details["access_token"]:
    session.load_oauth_session(login_details["token_type"], login_details["access_token"], login_details["refresh_token"], datetime.datetime.fromtimestamp(login_details["expiry_time"]))
else:
    # Will run until you visit the printed url and link your account
    session.login_oauth_simple()



login_details['token_type'] = session.token_type
login_details['access_token'] = session.access_token
login_details['refresh_token'] = session.refresh_token # Not needed if you don't care about refreshing
login_details['expiry_time'] = session.expiry_time.timestamp()

print(login_details)
with open(r'C:\Users\yuval\tidal_creds.yaml', 'w') as file:
    documents = yaml.dump(login_details, file)

<<<<<<< HEAD
=======
url = r"C:\Users\yuval\Downloads\2023-04-25.m3u8"

>>>>>>> 7697f2a312d1943e6724a91ceba04f7e150bdd89
tidal_tracks = []

with open(args.file, "rb") as f:
    lines = f.readlines()

def download_track(track_id):
    result = subprocess.run(["tidal-dl", "-l", str(track_id), "-o", down_path], text=True)
    with open(f"{down_path}/path.txt", "rb") as f:
        path = f.read(2000)

    return os.path.abspath(path.decode("utf-8")) + "\r\n"


print(lines)
print((len(lines) - 1) / 2)

output = [lines[0]]

for i in range(int((len(lines) - 1) / 2)):
    track = [lines[1 + (2*i)], lines[2 + (2*i)].decode("utf-8")]
    print(track)
    output.append(track[0])
    if track[1].startswith("tidal:tracks:"):
        tidal_track_name = track[0].decode("utf-8").split(",", 1)[1].rstrip()
        # This is a tidal track
        # tidal_tracks.append(int(line.decode("utf-8").split(":")[2]))
        track_id = int(track[1].split(':')[2])
        track_path = download_track(track_id)
        if not track_path:
            logging.warning("Failed to download", track)
            continue
        try:
            track_obj = session.track(track_id)
        except:
            logging.warning("Track missing, not found on tidal", track)
            continue
        print(track_obj.artist)
        artists = [artist.name for artist in track_obj.album.artists]
        track[1] = track_path
        output.append(track[1].encode("utf-8"))
    else:
        output.append(track[1].encode("utf-8"))


print(output)
with open("output.m3u8", "wb") as f:
    for line in output:
        print(line)
        f.write(line)