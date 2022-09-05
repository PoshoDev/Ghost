# Program that syncs a file between two directories.

import json
import os
import sys
import time
import shutil

datafile = "data.json"

def main(args):
    make_datafile()
    if len(args) == 1:
        show_help()
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

# Syncs the last modified file from a track's list of paths.
def sync_track(track):
    if os.path.exists(datafile):
        with open(datafile, "r") as file:
            data = json.load(file)
            for track in data["tracks"]:
                if track["type"] == "file":
                    last_modified = 0
                    last_modified_path = ""
                    for path in track["paths"]:
                        if os.path.exists(path):
                            if os.path.getmtime(path) > last_modified:
                                last_modified = os.path.getmtime(path)
                                last_modified_path = path
                        else:
                            print(f"Aborting sync for track '{track['name']}': path '{path}' does not exist!")
                            return
                    if last_modified_path != "":
                        for path in track["paths"]:
                            if path != last_modified_path:
                                shutil.copyfile(last_modified_path, path)
                        track["updated"] = time.time()
                        with open(datafile, "w") as file:
                            json.dump(data, file)
                        print(f"Synced track '{track['name']}'!")
                        return True
    return False

# Shows all the track names.
def show_tracks():
    if os.path.exists(datafile):
        with open(datafile, "r") as file:
            data = json.load(file)
            for track in data["tracks"]:
                print(track["name"])


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

# Syncs all tracks.
def sync_all():
    if os.path.exists(datafile):
        with open(datafile, "r") as file:
            data = json.load(file)
            for track in data["tracks"]:
                sync_track(track["name"])

if __name__ == "__main__":
    main(sys.argv)