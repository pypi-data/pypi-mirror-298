import os
import sys

default_dl_dir = os.path.expanduser("~")

ytdlp_cmd = os.path.join(os.path.dirname(sys.executable), "yt-dlp")

ytdlp_args = {}
# cookies = "--cookies-from-browser firefox"
ytdlp_args["music"] = "--extract-audio --audio-format mp3 --ignore-errors --restrict-filenames"
ytdlp_args["video"] = "--ignore-errors --restrict-filenames"
ytdlp_args["playlist"] = "--extract-audio --audio-format mp3 --ignore-errors --restrict-filenames -o '%(playlist)s/%(playlist_index)s-%(title)s.%(ext)s'"
