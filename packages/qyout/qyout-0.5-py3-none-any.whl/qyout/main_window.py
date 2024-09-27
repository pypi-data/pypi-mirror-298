from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from qyout.config import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Youtube downloader")
        # self.setFixedSize(QSize(800, 600))
        self.setMinimumSize(QSize(800, 600))
        self.setStyleSheet("QMainWindow { border: 1px solid black; }")

        self.info_url = QLabel()
        self.info_url.setText("Copy/past Youtube link...")

        self.url = ""
        self.input_url = QLineEdit()
        self.input_url.textChanged.connect(self.set_url)

        self.info_mode = QLabel()
        self.info_mode.setText("Select mode (convert to music, just keep video, music playlist)")

        self.combo_mode = QComboBox(self)
        self.combo_mode.addItem("music")
        self.combo_mode.addItem("video")
        self.combo_mode.addItem("playlist")

        self.dl_dir = default_dl_dir
        self.dl_dir_button = QPushButton("Download directory: "+self.dl_dir)
        self.dl_dir_button.clicked.connect(self.change_dir)

        self.fire_button = QPushButton("Download it!")
        self.fire_button.clicked.connect(self.fire_url)

        self.info_fire = QLabel()

        self.progress = QProgressBar(self)
        # self.progress.setGeometry(30, 40, 200, 25)
        self.progress.setMaximum(100)

        self.output = QTextEdit()
        self.output.ensureCursorVisible()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.info_url)
        self.layout.addWidget(self.input_url)
        self.layout.addWidget(self.info_mode)
        self.layout.addWidget(self.combo_mode)
        self.layout.addWidget(self.dl_dir_button)
        self.layout.addWidget(self.fire_button)
        self.layout.addWidget(self.info_fire)
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.output)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

    def set_url(self, url):
        self.url = url

    def change_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Select download directory", self.dl_dir)
        if folder:
            self.dl_dir = folder
            self.dl_dir_button.setText("Download directory: " + self.dl_dir)

    def fire_url(self):
        if len(self.url):
            self.progress.setValue(0)
            self.fire_button.setEnabled(False)
            self.url = self.url.split('&')[0]
            self.info_fire.setText("Processing "+ self.url + " ...")
            self.process.start(ytdlp_cmd,
                               ytdlp_args[self.combo_mode.currentText()].split(' ') +
                               [self.url, '-P', self.dl_dir])

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        if "[download] " in data:
            try:
                step = data.split()[1]
                if "%" in step:
                    step = int(step.split(".")[0].replace("%", ""))
                    if step > self.progress.value() or step < 4:
                        self.progress.setValue(step)
            except IndexError:
                pass
            except ValueError:
                pass
        else:
            self.output.append(data)
        self.output.ensureCursorVisible()

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output.append("<span style='color:red;'>"+data+"</span>")
        self.output.ensureCursorVisible()

    def process_finished(self, exit_code, exit_status):
        self.output.append("Process finished with exit code "+str(exit_code))
        self.fire_button.setEnabled(True)
        self.output.ensureCursorVisible()
