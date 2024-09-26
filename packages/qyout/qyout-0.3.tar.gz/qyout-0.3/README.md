# Qyout (say "cute") : Qt YOUTube Downloader GUI

Linux application to download Youtube. Just copy/paste Youtube URL. 3 modes are available:
* music: download and convert to mp3
* video: download video and reduce it
* playlist: download all musics of a playlist (convert to mp3) ==> be careful to copy a Youtube playlist URL: the URL shall contain "playlist" keyword (clic on "view full playlist" to get the correct URL)

Files are downloaded in your user directory.

Dependencies:
* yt-dlp
* pyqt6

Install:
``` bash
# create a venv
python3 -m venv venv
. activate venv/bin/activate
pip install --upgrade pip
pip install qyout
```

Run:
``` bash
. venv/bin/activate
qyout

# Or
./venv/bin/qyout

# Or you can create a Launcher - with gnome3, you can use Alacarte GUI
# install:
sudo dnf install alacarte
# use
alacarte
# clic "new item"
# Name: Qyout
# Command: browse and select path to .../venv/bin/qyout
# Do not check "launch in terminal"
# Validate
# Now go to gnome applications list, search "qyout", it exists, you can run it, you can attach it in your favorite dock/menu !
```

Enjoy :)


# For developers

Todo list:
* Add a logger
* Use a config parser and allow user config
* Beautifully the GUI
* Add download options


Build wheel from sources:
``` bash
# clone repository
git clone https://github.com/Guitouu31/qyout.git

./deliver.sh
```


Test:
``` bash
# deliver and install
./test.sh
```
