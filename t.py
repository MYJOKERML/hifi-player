import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QUrl
from mutagen.id3 import ID3
from mutagen.flac import FLAC

class LosslessMusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lossless Music Player")
        self.setGeometry(100, 100, 400, 300)

        self.player = QMediaPlayer(self)
        self.playlist = QMediaPlaylist(self.player)
        self.player.setPlaylist(self.playlist)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_music)

        self.open_button = QPushButton("Open Music File")
        self.open_button.clicked.connect(self.open_music_file)

        self.album_image_label = QLabel()
        self.album_image_label.setAlignment(Qt.AlignCenter)

        self.artist_label = QLabel()
        self.album_label = QLabel()

        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.play_button)
        layout.addWidget(self.open_button)
        layout.addWidget(self.album_image_label)
        layout.addWidget(self.artist_label)
        layout.addWidget(self.album_label)
        layout.addWidget(self.progress_slider)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.playing = False

        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(100)  # 每100毫秒更新一次进度条

    def open_music_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Music File", "", "Audio Files (*.flac *.mp3);;All Files (*)", options=options)
        if file_name:
            self.load_music(file_name)

    def load_music(self, file_name):
        self.playlist.clear()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
        self.play_button.setText("Play")
        self.playing = False
        self.progress_slider.setValue(0)
        self.progress_slider.setEnabled(True)
        self.load_album_image(file_name)
        self.load_metadata(file_name)

    def load_album_image(self, file_name):
        # Extract album image and display it using QPixmap and QLabel.
        _, file_extension = os.path.splitext(file_name)
        if file_extension.lower() == ".mp3":
            audio = ID3(file_name)
            if 'APIC:' in audio:
                image_data = audio['APIC:'].data
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.album_image_label.setPixmap(pixmap.scaled(200, 200))
        elif file_extension.lower() == ".flac":
            flac = FLAC(file_name)
            if 'METADATA_BLOCK_PICTURE' in flac:
                picture = flac['METADATA_BLOCK_PICTURE'][0]
                image_data = picture.data
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.album_image_label.setPixmap(pixmap.scaled(200, 200))
        else:
            self.album_image_label.clear()

    def load_metadata(self, file_name):
        # Extract and display artist and album metadata.
        _, file_extension = os.path.splitext(file_name)
        if file_extension.lower() == ".mp3":
            audio = ID3(file_name)
            artist = audio['TPE1'].text[0] if 'TPE1' in audio else 'Unknown Artist'
            album = audio['TALB'].text[0] if 'TALB' in audio else 'Unknown Album'
        elif file_extension.lower() == ".flac":
            flac = FLAC(file_name)
            artist = flac['artist'][0] if 'artist' in flac else 'Unknown Artist'
            album = flac['album'][0] if 'album' in flac else 'Unknown Album'
        else:
            artist = "Unknown Artist"
            album = "Unknown Album"
        self.artist_label.setText(f"Artist: {artist}")
        self.album_label.setText(f"Album: {album}")

    def play_music(self):
        if self.playing:
            self.player.pause()
        else:
            self.player.play()
        self.play_button.setText("Pause" if self.player.state() == QMediaPlayer.PlayingState else "Play")
        self.playing = not self.playing

    def update_progress(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            position = self.player.position()
            self.progress_slider.setValue(position)

    def closeEvent(self, event):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = LosslessMusicPlayer()
    player.show()
    sys.exit(app.exec_())
