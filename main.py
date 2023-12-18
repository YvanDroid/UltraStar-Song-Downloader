# This python file uses the following third party modules:
# PyTube

# To use, place this into the root folder of your albums or songs and run it.
# Tested working on playlists from usdb.animux.de

import os

from pytube import YouTube

cwd = os.getcwd()
print(cwd)

directory_list = [x[0] for x in os.walk(cwd)]
print(directory_list)


def song_download(folder):
    # This function should use the folder name as the song name
    current_folder = folder
    song_name = os.path.basename(current_folder)
    song_path = current_folder + "\\" + song_name
    song_text_file = song_path + ".txt"
    song_mp3 = song_path + ".mp3"
    song_mp4 = song_path + ".mp4"
    # This should be the song name
    if os.path.isfile(song_mp4) or os.path.isfile(song_mp3):
        print("Song files already downloaded")
        return

    try:
        text_file = open(song_text_file, "r")
    except OSError:
        print("No file was found for this folder")
        return

    # Search the file for the #VIDEO header and check for youtube url
    text_lines = text_file.readlines()
    video_line = 0
    for row in text_lines:
        if row.find("#VIDEO") != -1:
            video_line = row
            break

    # Should be the #VIDEO header. Hopefully no exceptions
    #video_id = video_line.split(",")[0][7:]
    needs_formatting = False # For when video exists but uses a= instead of v=
    url_pos = video_line.find("v=")
    if url_pos == -1:
        url_pos = video_line.find("a=")
        needs_formatting = True
    
    url_end = video_line.find(",", url_pos) # Find either the end of the line or next comma
    if url_end == -1:
        url_end = len(video_line)
    video_id = video_line[url_pos:url_end]
    print(video_id)
    if needs_formatting:
        video_id = video_id.replace("a=","v=")
    if video_id == "":
        print(f"No compatible url found for {song_name}")
        return
    
    yt_url = "http://youtube.com/watch?" + video_id
    try:
        yt = YouTube(yt_url)
    except:
        print(f"Song could not be found with the link for song {song_name} ")
        return

    # Get highest quality video out
    try:
        yt.streams.filter(progressive=True, file_extension="mp4").order_by(
            "resolution"
        ).desc().first().download(
            output_path=current_folder, filename=song_name + ".mp4"
        )
        # Get the audio from the youtube video
        yt.streams.filter(only_audio=True).first().download(
            output_path=current_folder, filename=song_name + ".mp3"
        )
    except Exception as ex:
        print(f"the following error has occured for {song_name} - {ex}")
    text_file.close()


for song in directory_list:
    song_download(song)

output_wait = input("Script done. Press enter to close the application")
