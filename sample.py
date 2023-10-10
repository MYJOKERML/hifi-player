import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from pydub import AudioSegment
from pydub.playback import play

class LosslessMusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lossless Music Player")
        self.setGeometry(100, 100, 400, 200)

        self.player = None
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_music)

        self.open_button = QPushButton("Open Music File")
        self.open_button.clicked.connect(self.open_music_file)

        layout = QVBoxLayout()
        layout.addWidget(self.play_button)
        layout.addWidget(self.open_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def open_music_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Music File", "", "Audio Files (*.flac *.mp3);;All Files (*)", options=options)
        if file_name:
            self.load_music(file_name)

    def load_music(self, file_name):
        if self.player:
            self.player.stop()
        audio = AudioSegment.from_file(file_name)
        self.player = play(audio)

    def play_music(self):
        if self.player and self.player.is_playing():
            self.player.stop()
            self.play_button.setText("Play")
        elif self.player:
            self.player.resume()
            self.play_button.setText("Pause")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = LosslessMusicPlayer()
    player.show()
    sys.exit(app.exec_())
