from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from pydub import AudioSegment
from pydub.playback import play
import os

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.layout = QVBoxLayout()
        self.select_button = QPushButton("Select Directory")
        self.select_button.clicked.connect(self.select_directory)
        self.layout.addWidget(self.select_button)
        self.setLayout(self.layout)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.play_music_files(directory)

    def play_music_files(self, directory):
        music_files = []
        for file in os.listdir(directory):
            if file.endswith('.flac') or file.endswith('.mp3'):
                music_files.append(os.path.join(directory, file))
        for music_file in music_files:
            print(f"Playing {music_file}")
            audio = AudioSegment.from_file(music_file)
            play(audio)

if __name__ == "__main__":
    app = QApplication([])
    music_player = MusicPlayer()
    music_player.show()
    app.exec_()