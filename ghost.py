# Program that syncs a file between two directories.

import json
import os
import sys
import time
import shutil

datafile = "data.json"

def main(args):
    make_datafile()
    print(find_track(args[1]))
    add_track(args[1], args[2:])

def make_datafile():
    if not os.path.exists(datafile):
        with open(datafile, "w") as file:
            data = {}
            data["tracks"] = []
            json.dump(data, file)

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
                data["tracks"].append(newtrack)
                with open(datafile, "w") as file:
                    json.dump(data, file)
                    print(f"Added track '{track}' to '{datafile}'!")
            else:
                print(f"Track '{track}' already exists in '{datafile}'!")

if __name__ == "__main__":
    main(sys.argv)