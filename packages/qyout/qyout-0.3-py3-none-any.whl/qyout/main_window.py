from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from .config import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Youtube downloader")
        # self.setFixedSize(QSize(800, 600))
        self.setMinimumSize(QSize(800, 600))
        self.setStyleSheet("QMainWindow { border: 2px solid black; }")

        self.url = ""

        self.input = QLineEdit()
        self.input.textChanged.connect(self.set_url)

        self.button = QPushButton("Download it!")
        # self.button.setCheckable(True)
        self.button.clicked.connect(self.fire_url)

        self.combo = QComboBox(self)
        self.combo.addItem("music")
        self.combo.addItem("video")
        self.combo.addItem("playlist")

        self.label = QLabel()
        self.output = QTextEdit()
        self.output.ensureCursorVisible()

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.combo)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.addWidget(self.output)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

        # QProcess object for external app
        self.process = QProcess(self)
        # self.process.readyRead.connect(self.dataReady)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

    def set_url(self, url):
        self.url = url

    def fire_url(self):
        if len(self.url):
            self.button.setEnabled(False)
            self.url = self.url.split('&')[0]
            print("Processing ", self.url)
            self.label.setText("Processing "+ self.url + " ...")
            print("Binary " + ytdlp_cmd)
            self.process.start(ytdlp_cmd,
                               ytdlp_args[self.combo.currentText()].split(' ') +
                               [self.url, '-P', default_dl_dir])

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output.append(data)
        self.output.ensureCursorVisible()

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output.append("<span style='color:red;'>"+data+"</span>")
        self.output.ensureCursorVisible()

    def process_finished(self, exit_code, exit_status):
        self.output.append("Process finished with exit code "+str(exit_code))
        self.button.setEnabled(True)
        self.output.ensureCursorVisible()
