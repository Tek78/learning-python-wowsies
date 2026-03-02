import sys
from yt_dlp import YoutubeDL, DownloadError
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

class ytConverter(QWidget):
    def __init__(self):
        QWidget.__init__()
        self.title_label, self.top_label, self.bottom_label = QLabel("Youtube to Audio Download", self), QLabel("Paste the url below and click the button.", self), QLabel(self)
        self.info_button, self.download_button, self.file_button = QPushButton("Search", self), QPushButton("Download", self), QPushButton("📂", self)
        self.url_input = QLineEdit(self)
        self.path = 'C:/Users/aeugh/Desktop/python file testing/downloaded songs/%(title)s.%(ext)s'
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Youtube to Audio Download"), self.setGeometry(650, 200, 400, 200)
        self.url_input.setPlaceholderText("Paste url here...")

        vbox = QVBoxLayout()
        #top layout
        top_vbox = QVBoxLayout()
        top_vbox.setSpacing(0)
        top_vbox.addWidget(self.title_label), top_vbox.addWidget(self.top_label)
        #search box
        s_hbox = QHBoxLayout()
        s_hbox.setSpacing(0), s_hbox.setContentsMargins(0, 0, 0, 0)
        s_hbox.addWidget(self.url_input), s_hbox.addWidget(self.file_button)
        #horizontal for interface
        hbox = QHBoxLayout()
        hbox.addWidget(self.download_button), hbox.addWidget(self.info_button)
        #bottom layout
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.bottom_label)

        s_hbox.addLayout(hbox)
        vbox.addLayout(top_vbox)
        vbox.addLayout(s_hbox)
        vbox.addLayout(vbox2)
        self.setLayout(vbox)

        self.top_label.setObjectName("top_label"), self.title_label.setObjectName("title_label"), self.bottom_label.setObjectName("bottom_label")
        self.file_button.setFixedWidth(25), self.file_button.setObjectName("file_button")

        self.setStyleSheet("""
            QLabel#title_label{
                font-size: 20px;
                font-weight: bold;
            }
            QLabel#top_label{
                font-size: 12px;
            }
            QLineEdit{
                height: 17px;
                font-size: 12px;
            }
            QPushButton#file_button{
                height: 15px;
            }
        """)

        self.file_button.clicked.connect(self.select_destination), self.download_button.clicked.connect(self.download_audio), self.info_button.clicked.connect(self.search_url)

    def display_info(self, data):
        vals, text = ["title", "duration", "view_count", "channel", "like_count", "filesize", "filesize_approx"], ""
        for key in vals: text += f"\n{key.title()}: {data[key]}"
        self.bottom_label.setText(text)

    def search_url(self):
        url = self.url_input.text()
        if not self.url_is_valid(url):
            self.display_error()
        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{self.path}/%(title)s.%(ext)s',
            }
            with YoutubeDL(ydl_opts) as ydl:
                data = ydl.extract_info(url, download=False)
            self.display_info(data)

    def download_audio(self):
        url = self.url_input.text()
        if not self.url_is_valid(url):
            self.display_error()
        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{self.path}',
                'ffmpeg_location': r'C:\Users\aeugh\ffmpeg\bin',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            QMessageBox.information(
                self,
                "Download Complete",
                "Your file was downloaded successfully!"
            )

    def select_destination(self):
        folder = QFileDialog.getExistingDirectory(
            None,
            "Select File Destination",
            f"{self.path}",
        )
        if folder: self.path = f"{folder}/%(title)s.%(ext)s"

    def display_error(self):
        QMessageBox.information(
            self,
            "An error has occurred!",
            "Make sure your url is valid."
        )
        self.url_input.clear()

    @staticmethod
    def url_is_valid(url):
        try:
            ydl_opts = {'quiet': True}
            with YoutubeDL(ydl_opts) as ydl:
                data = ydl.extract_info(url, download=False)
            return True
        except Exception:
            return False


def main():
    app = QApplication(sys.argv)
    converter = ytConverter()
    converter.show()
    sys.exit(app.exec_())

if __name__ == '__main__': main()
