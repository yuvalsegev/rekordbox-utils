# rekordbox-utils
A bunch of small scripts which help converting an online TIDAL based collection to an offline enviroment.


- `rekordbox_to_tidal.py` is designed to convert a rekordbox-exported .m3u8 playlist containing tidal tracks to an offline playlist, it uses `tidal-dl` to donwload the tracks locally
- `rekordbox_collection_to_offline.py` will convert an entire rekordbox `collection.xml` file to offline. It will downlaod each tidal track using `tidal-dl` and will export a new `collection_offline.xml` file which will redirect every TIDAL track to the local file, this is really cool because it preserves hotcues & beatgrids.