import os
import sys

default_dl_dir = os.path.expanduser("~")

ytdlp_cmd = os.path.dirname(sys.executable) + "/yt-dlp"

ytdlp_args = {}
ytdlp_args["music"] = "--cookies-from-browser firefox --extract-audio --audio-format mp3 --ignore-errors --restrict-filenames"
ytdlp_args["video"] = "--cookies-from-browser firefox --ignore-errors --restrict-filenames"
ytdlp_args["playlist"] = "--cookies-from-browser firefox --extract-audio --audio-format mp3 --ignore-errors --restrict-filenames -o '%(playlist)s/%(playlist_index)s-%(title)s.%(ext)s'"
