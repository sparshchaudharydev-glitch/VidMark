import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QShortcut,QMainWindow, QWidget,QComboBox,QFrame, QVBoxLayout,QLabel, QHBoxLayout, QPushButton, QSlider,QFileDialog
from PyQt5.QtMultimediaWidgets import QVideoWidget
from bookmark_seeker import BookmarkSeeker
from bookmark_manager import BookmarkManager
from bookmark import Bookmark
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt ,QUrl,QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        
        super().__init__()
        self.setWindowIcon(QIcon("logo.ico"))
        self.setWindowTitle("VLCBook")
        self.resize(800, 600)
        self.init_ui()
        
    def init_ui(self):
        self.central_Widget = QWidget()
        
        self.setCentralWidget(self.central_Widget)

        

        self.main_layout = QVBoxLayout()
        self.central_Widget.setLayout(self.main_layout)
        
        self.video_widget = QVideoWidget()
        self.main_layout.addWidget(self.video_widget)
        self.main_layout.setStretchFactor(self.video_widget, 1)


        
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video_widget)

        self.slider = BookmarkSeeker()
        self.main_layout.addWidget(self.slider)

        self.current_time_label = QLabel("0:00")
        self.total_time_label = QLabel("0:00")
        self.time_layout = QHBoxLayout()
        self.time_layout.addWidget(self.current_time_label)
        self.time_layout.addStretch()
        self.time_layout.addWidget(self.total_time_label)
        self.main_layout.addLayout(self.time_layout)


        self.btn_layout = QHBoxLayout()
        self.open_btn = QPushButton("Open")
        self.play_btn = QPushButton("Play")
        self.add_bookmark_btn = QPushButton("Add Bookmark")
        self.delete_bookmark_btn = QPushButton("Delete Bookmark")
        self.bookmark_manager = BookmarkManager()
        

        
        self.btn_layout.addWidget(self.open_btn)
        self.btn_layout.addWidget(self.play_btn)
        self.btn_layout.addWidget(self.add_bookmark_btn)
        self.btn_layout.addWidget(self.delete_bookmark_btn)
        

        
        
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Dark Grey" , "Pure Black" , "Light"])
        self.btn_layout.addWidget(self.theme_selector)

        self.main_layout.addLayout(self.btn_layout)
        self.connect_slider()
        
        
        self.change_theme("Dark Grey")

        self.shortcut = QShortcut(QKeySequence(Qt.Key_Space),self)
        self.shortcut.activated.connect(self.space_key)

        self.shortcut = QShortcut(QKeySequence(Qt.Key_Right),self)
        self.shortcut.activated.connect(self.fast_forward)

        self.shortcut = QShortcut(QKeySequence(Qt.Key_Left),self)
        self.shortcut.activated.connect(self.slow_down)       
               
    def open(self):
        opening_file,_ = QFileDialog.getOpenFileName(self, "Open Video")
        
        if opening_file:
            self.current_filepath = opening_file
            url = QUrl.fromLocalFile(opening_file)
            self.player.setMedia(QMediaContent(url))
            self.player.play()
            loaded = self.bookmark_manager.load(self.current_filepath)
            self.slider.set_bookmark(loaded)
        
    def play_pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_btn.setText("Play")
            
        else:
            self.player.play()
            self.play_btn.setText("Pause")
                 
    def connect_slider(self):
        self.player.positionChanged.connect(self.update_slider)
        self.player.durationChanged.connect(self.set_duration)
        self.slider.sliderMoved.connect(self.seek)
        self.open_btn.clicked.connect(self.open)
        self.play_btn.clicked.connect(self.play_pause)
        self.add_bookmark_btn.clicked.connect(self.add_bookmark)
        self.delete_bookmark_btn.clicked.connect(self.delete_bookmark)
        self.theme_selector.currentTextChanged.connect(self.change_theme)
             
    def add_bookmark(self):
        adbo = self.player.position()
        
        label, ok = QInputDialog.getText(self, "Add Bookmark", "Enter label:")
        if ok and label:
            bm = Bookmark(label=label, timestamp=adbo, filepath=self.current_filepath)
            self.bookmark_manager.add_bookmark(bm)
            self.slider.set_bookmark(self.bookmark_manager.load(self.current_filepath))

    def delete_bookmark(self):
        debo = self.player.position()
        bookmarks = self.bookmark_manager.load(self.current_filepath)
        if not bookmarks:
            return
        closest = min(bookmarks, key=lambda b: abs(b.timestamp - debo))
        self.bookmark_manager.delete_bookmark(self.current_filepath,closest.timestamp)
        self.slider.set_bookmark(self.bookmark_manager.load(self.current_filepath))

    def change_theme(self,theme):
        if theme == "Dark Grey":
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; }
                QPushButton { font-weight: bold }                
                QPushButton { background-color: #3c3f41; color: white; }
                QPushButton:hover { background-color: #4c5052; }
                QSlider::groove:horizontal { background-color: #ff8c00; height: 16px; }
                QSlider::handle:horizontal { background-color: white;}
                QSlider::handle:horizontal {width: 32px; height: 16px; border-radius: 8px;}
                QComboBox { background-color: white; color: black; }
                QComboBox {font-weight: bold}
                QInputDialog { background-color: #111111; color: white; }
                QLineEdit { background-color: #222222; color: white; border: 1px solid #555; }
                QLabel { color: white; }
                QComboBox QAbstractItemView{background-color:white; color-black}
                QComboBox { outline: none; border: 1px solid #555; }
                
            """)
            self.slider.set_marker_color("white")
        

        elif theme == "Pure Black":
            self.setStyleSheet("""
                QWidget { background-color: #000000;  }
                QPushButton { font-weight: bold }     
                QPushButton { background-color: white; color: black;}
                QPushButton:hover { background-color: #868686; }
                QSlider::groove:horizontal { background-color: #1CC5E3; height: 16px; }
                QSlider::handle:horizontal { background-color: white;}
                QSlider::handle:horizontal {width: 32px; height: 16px; border-radius: 8px;}
                QComboBox { background-color: white; color: black; }
                QComboBox {font-weight: bold}
                QInputDialog { background-color: #111111; color: white; }
                QLineEdit { background-color: #222222; color: white; border: 1px solid #555; }
                QLabel { color: white; }
                QComboBox QAbstractItemView{background-color:white; color-black}
                QComboBox { outline: none; border: 1px solid #555; }
                                 
            """)
            self.slider.set_marker_color("orange")
        else:
            self.setStyleSheet("""
                QWidget { background-color: #FFFFFF; }
                QPushButton { font-weight: bold }          
                QPushButton { background-color: #E7E7E7; color: black; }
                QPushButton:hover { background-color: #FFFFFF; }
                QSlider::groove:horizontal { background-color: black; height: 16px; }
                QSlider::handle:horizontal { background-color: #EC1313;  }
                QSlider::handle:horizontal {width: 32px; height: 16px; border-radius: 8px;}
                QComboBox { background-color: white; color: black; }
                QComboBox {font-weight: bold}
                QComboBox QAbstractItemView{background-color:white; color-black}  
                QComboBox { outline: none; border: 1px solid #555; }        
            """)
            self.slider.set_marker_color("orange")
        
    def format_time(self,ms):
        seconds = ms// 1000
        minutes = seconds//60
        remaining = seconds % 60
        return f"{minutes}:{remaining:02d}"
        
    def update_slider(self,position):
        if not hasattr(self, 'duration'): return
        
        self.slider.setValue(position)
        x = self.format_time(position)
        y = self.format_time(self.duration)
        self.current_time_label.setText(x)
        self.total_time_label.setText(y)
        
    def set_duration(self,duration):
        self.slider.setMaximum(duration)
        self.duration = duration 

    def seek(self, position):
        self.player.setPosition(position)

    def space_key(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()
            
    def fast_forward(self):
        
        new_position = self.player.position() + 5000
        
        self.player.setPosition(new_position)

    def slow_down(self):
        
        new_position = self.player.position() - 5000
        
        self.player.setPosition(new_position)


        
