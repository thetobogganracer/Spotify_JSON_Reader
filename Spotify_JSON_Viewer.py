"""
This program allows a user to view their extended Spotify streaming history in text format rather than JSON.
"""
import json
from tkinter import *
import os


def submit():
    """
    This function destroys the original text box and starts the next function.
    """
    global file_path
    file_path = entry.get()
    start.destroy()
    process_files()

def process_files():
    streams = []

    if len(file_path) > 0:
        for file_name in os.listdir(file_path):
            if not (file_name[-4:] == "json"):
                continue
            
            file_path_name = os.path.join(file_path, file_name) # Creates a complete directory.
            
            with open(file_path_name, encoding="utf8") as file:
                streaming_list = json.load(file) # Parses the JSON file as a dictionary.
                for stream in streaming_list:
                    if stream["master_metadata_track_name"] is None: continue # Skips tracks with no information.
                    if stream["reason_end"] != "trackdone": continue # Skips tracks that weren't finished.
                    date = stream["ts"][0:10] # These characters will always correspond to a date in YYYY-MM-DD format.
                    time = stream["ts"][11:16] # These characters will always correspond to a time in HH:MM format.
                    track = stream["master_metadata_track_name"]
                    artist = stream["master_metadata_album_artist_name"]
                    album = stream["master_metadata_album_album_name"]
                    finished = stream["reason_end"] == "trackdone"
                    streams.append({"Date": date,
                                    "Time": time,
                                    "Track": track,
                                    "Artist": artist,
                                    "Album": album})
    
    streams = sorted(streams, key=lambda k: k["Date"]) # Sorts the list based on date.
    display_results(streams)

def display_results(streams):
    """
    This function creates another window which displays the user's streaming information.
    """
    window = Tk()
    window.geometry("600x600")
    window.title("Spotify JSON Viewer")
    scrollbar = Scrollbar(window)
    scrollbar.pack(side=RIGHT, fill=Y)
    title = Label(window, text="Your streaming history:", font=("Arial", 20, "bold"))
    title.pack()
    stream_list = Listbox(window, yscrollcommand=scrollbar.set)

    for stream in streams:
        date = stream["Date"]
        time = stream["Time"]
        track = stream["Track"]
        artist = stream["Artist"]
        album = stream["Album"]
        stream_string = f"Date: {date}, Time: {time}, Track: {track}, Artist: {artist}, Album: {album}"
        stream_list.insert(END, stream_string)
        stream_list.pack(side=LEFT, fill="both", expand=True)
        scrollbar.config(command=stream_list.yview)
    
    window.mainloop()

start = Tk()
start.geometry("600x100")
start.title("Spotify JSON Viewer")
entry_label = Label(start, text="Enter file path:")
entry_label.pack()
entry = Entry()
entry.pack()
submit_button = Button(start, text="Submit", command=submit)
submit_button.pack()
start.mainloop()
