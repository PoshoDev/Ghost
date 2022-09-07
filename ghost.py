# Program that syncs a file between two directories.

import json
import os
import sys
import time
import shutil
from win10toast import ToastNotifier
import pystray
from PIL import Image

datafile = "data.json"

def main(args):
    make_datafile()
    if len(args) == 1:
        default()
    elif args[1] == "help":
        show_help()
    elif args[1] == "add":
        if len(args) >= 4:
            add_track(args[2], args[3:])
        else:
            print("Invalid arguments!")
    elif args[1] == "remove":
        if len(args) == 3:
            remove_track(args[2])
        else:
            print("Invalid arguments!")
    elif args[1] == "sync":
        if len(args) == 3:
            sync_track(args[2])
        elif len(args) == 2:
            sync_all()
        else:
            print("Invalid arguments!")
    elif args[1] == "show":
        if len(args) == 2:
            show_tracks()
        elif len(args) == 3:
            show_track(args[2])
        else:
            print("Invalid arguments!")
    elif args[1] == "addpath":
        if len(args) == 4:
            add_paths(args[2], args[3].split(","))
        else:
            print("Invalid arguments!")
    elif args[1] == "auto":
        if len(args) == 3:
            auto_sync(int(args[2]))
        else:
            print("Invalid arguments!")

def make_datafile():
    if not os.path.exists(datafile):
        with open(datafile, "w") as file:
            data = {}
            data["tracks"] = []
            json.dump(data, file)

def show_help():
    print("Ghost.py - Syncs files between directories.")
    print("Usage:")
    print("ghost.py help")
    print("ghost.py add <name> <paths>")
    print("ghost.py remove <name>")
    print("ghost.py sync <name>")
    print("ghost.py sync")
    print("ghost.py show <name>")
    print("ghost.py show")
    print("ghost.py addpath <name> <paths>")
    print("ghost.py auto <secs>")
    
# Finds if the track exists in a JSON file.
def find_track(track):
    if os.path.exists(datafile):
        with open(datafile, "r") as file:
            data = json.load(file)
            for t in data["tracks"]:
                if t["name"] == track:
                    return True
    return False

# Adds a track to the JSON file.
def add_track(track, paths):
    if os.path.exists(datafile):
        with open(datafile, "r") as file:
            data = json.load(file)
            if not find_track(track):
                newtrack = {}
                newtrack["name"] = track
                newtrack["type"] = "file"
                newtrack["paths"] = paths
                newtrack["updated"] = time.time()
                data["tracks"].append(newtrack)
                with open(datafile, "w") as file:
                    json.dump(data, file)
                    print(f"Added track '{track}' to '{datafile}'!")
            else:
                print(f"Track '{track}' already exists in '{datafile}'!")

# Adds paths to existing track.
def add_paths(track, paths):
    if os.path.exists(datafile):
        with open(datafile, "r") as file:
            data = json.load(file)
            if find_track(track):
                for t in data["tracks"]:
                    if t["name"] == track:
                        for path in paths:
                            if path not in t["paths"]:
                                t["paths"].append(path)
                with open(datafile, "w") as file:
                    json.dump(data, file)
                    print(f"Added paths to track '{track}'!")

# Removes a track from the JSON file.
def remove_track(track):
    if os.path.exists(datafile):
        with open(datafile, "r") as file:
            data = json.load(file)
            if find_track(track):
                for t in data["tracks"]:
                    if t["name"] == track:
                        data["tracks"].remove(t)
                with open(datafile, "w") as file:
                    json.dump(data, file)
                    print(f"Removed track '{track}' from '{datafile}'!")
            else:
                print(f"Track '{track}' does not exist in '{datafile}'!")

# Syncs the last modified file in a track's paths to all other paths if the file is newer than the last sync time of the track in the JSON file.
def sync_track(name):
    if os.path.exists(datafile):
        with open(datafile, "r") as file:
            data = json.load(file)
            for track in data["tracks"]:
                if track["name"] == name:
                    lastmod = 0
                    lastmodpath = ""
                    for path in track["paths"]:
                        if os.path.exists(path):
                            if os.path.getmtime(path) > lastmod:
                                lastmod = os.path.getmtime(path)
                                lastmodpath = path
                    if lastmod > track["updated"]:
                        for path in track["paths"]:
                            if path != lastmodpath:
                                if os.path.exists(path):
                                    shutil.copy(lastmodpath, path)
                                    print(f"Synced '{lastmodpath}' to '{path}'!")
                                else:
                                    print(f"Path '{path}' does not exist!")
                        track["updated"] = time.time()
                        with open(datafile, "w") as file:
                            json.dump(data, file)
                            print(f"Synced track '{track['name']}'!")
                            return True
                    else:
                        print(f"Track '{track['name']}' is up to date!")
    return False

# Shows all the track names.
def show_tracks():
    if os.path.exists(datafile):
        with open(datafile, "r") as file:
            data = json.load(file)
            for track in data["tracks"]:
                print(track["name"])

# Gets a list of all track names.
def get_tracks():
    if os.path.exists(datafile):
        with open(datafile, "r") as file:
            data = json.load(file)
            tracks = []
            for track in data["tracks"]:
                tracks.append(track["name"])
            return tracks
    return []

# Shows the info for a given track.
def show_track(name):
    if os.path.exists(datafile):
        with open(datafile, "r") as file:
            data = json.load(file)
            for track in data["tracks"]:
                if track["name"] == name:
                    print(f"Name: {track['name']}")
                    print(f"Type: {track['type']}")
                    print(f"Updated: {track['updated']}")
                    print("Paths:")
                    for path in track["paths"]:
                        print(path)

# Syncs all tracks and returns a list of the updated track names.
def sync_all():
    if os.path.exists(datafile):
        with open(datafile, "r") as file:
            data = json.load(file)
            updated = []
            for track in data["tracks"]:
                if sync_track(track["name"]):
                    updated.append(track["name"])
            return updated

# Automatically syncs all tracks every given seconds and shows a notification when a track is synced.
def auto_sync(secs, notifications=False):
    while True:
        notify("ses", "SES!")
        print("SES!!")
        synced = sync_all()
        if notifications:
            for track in synced:
                notify(track, "just finished syncing!")
        time.sleep(secs)

# Notifies the user of a synced track.
def notify(text, subtext):
    toast = ToastNotifier()
    toast.show_toast(text, subtext, icon_path="icon.ico", duration=5, threaded=True)

def tray_clicked(icon, item):
    opt = str(item)
    if opt == "Sync All":
        sync_all()
    elif opt == "Quit":
        icon.stop()
    elif opt in get_tracks():
        sync_track(opt)


# Default function.
def default():
    print("G H O S T")
    image = Image.open("icon.png")
    submenus = []
    tracks = get_tracks()
    for track in tracks:
        submenus.append(pystray.MenuItem(track, tray_clicked))
    icon = pystray.Icon("Ghost", image, menu=pystray.Menu(
        pystray.MenuItem("Sync All", tray_clicked),
        pystray.MenuItem("Sync Track", pystray.Menu(*submenus)),
        pystray.MenuItem("Quit", tray_clicked)))
    icon.run()
    notify("Ghost", "is running!")
    #auto_sync(5, True)

# Runs the program.
if __name__ == "__main__":
    main(sys.argv)