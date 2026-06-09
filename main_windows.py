import os
os.environ["QT_MULTIMEDIA_PREFERRED_PLUGINS"] = "windowsmediafoundation"

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QShortcut,QMainWindow,
QWidget,QComboBox, QVBoxLayout,QLabel, QHBoxLayout, 
QPushButton, QSlider,QFileDialog,QInputDialog , QListWidget,QListWidgetItem )
from PyQt5.QtMultimediaWidgets import QVideoWidget
from bookmark_seeker import BookmarkSeeker
from bookmark_manager import BookmarkManager
from bookmark import Bookmark
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt ,QUrl,QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        
        super().__init__()
        self.setWindowIcon(QIcon("logo.ico"))  
        self.setWindowTitle("VidMark")
        self.resize(800, 600)
        self.init_ui()
        
    def init_ui(self):
        
        self.central_Widget = QWidget()
        self.setCentralWidget(self.central_Widget)


        self.main_layout = QVBoxLayout()
        self.central_Widget.setLayout(self.main_layout)
        
        self.video_widget = QVideoWidget()
        


        self.bookmark_list = QListWidget()
        self.bookmark_list.setFixedWidth(200)
        self.bookmark_list.hide()


        self.content_layout = QHBoxLayout()
        self.content_layout.addWidget(self.video_widget)
        self.content_layout.addWidget(self.bookmark_list)
        self.content_layout.setStretchFactor(self.video_widget, 1)
        self.main_layout.addLayout(self.content_layout)
        self.main_layout.setStretchFactor(self.content_layout, 1)
      
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
        self.bookmark_list_btn = QPushButton("📋")
        
        self.bookmark_manager = BookmarkManager()



        self.btn_layout.addWidget(self.open_btn)
        self.btn_layout.addWidget(self.play_btn)
        self.btn_layout.addWidget(self.add_bookmark_btn)
        self.btn_layout.addWidget(self.delete_bookmark_btn)
        self.btn_layout.addWidget(self.bookmark_list_btn)
    
        self.volume_label = QLabel("🔊")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.btn_layout.addWidget(self.volume_label)
        self.volume_slider.setRange(0,100)
        self.volume_slider.setValue(50)
        
        self.btn_layout.addWidget(self.volume_slider)
        

        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Dark Grey" , "Pure Black" , "Light"])
        self.btn_layout.addWidget(self.theme_selector)

        self.main_layout.addLayout(self.btn_layout)
        self.connect_slider()
        

        
        self.change_theme("Dark Grey")

        self.shortcut_play = QShortcut(QKeySequence(Qt.Key_Space),self)
        self.shortcut_play.activated.connect(self.space_key)

        self.shortcut_forward = QShortcut(QKeySequence(Qt.Key_Right),self)
        self.shortcut_forward.activated.connect(self.fast_forward)

        self.shortcut_backward = QShortcut(QKeySequence(Qt.Key_Left),self)
        self.shortcut_backward.activated.connect(self.slow_down)

        self.shortcut_open_file = QShortcut(QKeySequence("Ctrl+O"),self)
        self.shortcut_open_file.activated.connect(self.open_explorer)

        self.shortcut_addbookmark = QShortcut(QKeySequence("Ctrl+B"),self)
        self.shortcut_addbookmark.activated.connect(self.new_bookmarkshot)

        self.shortcut_delete_bookmark = QShortcut(QKeySequence("Ctrl+D"),self)
        self.shortcut_delete_bookmark.activated.connect(self.delete_bookmarkshot)


        self.btn_layout.setStretch(0, 1)
        self.btn_layout.setStretch(1, 1)
        self.btn_layout.setStretch(2, 1)
        self.btn_layout.setStretch(3, 1)
        self.btn_layout.setStretch(4, 1)
        self.btn_layout.setStretch(6, 1)
        

        
        

        self.control_autohide()
             
    def open_file(self):
        opening_file,_ = QFileDialog.getOpenFileName(self, "Open Video")
        
        if opening_file:
            self.current_filepath = opening_file
            url = QUrl.fromLocalFile(opening_file)
            self.player.setMedia(QMediaContent(url))
            self.player.play()
            load_bookmarkpath = self.bookmark_manager.load(self.current_filepath)
            self.slider.set_bookmark(load_bookmarkpath)
            self.update_bookmark_list()
        
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
        self.open_btn.clicked.connect(self.open_file)
        self.play_btn.clicked.connect(self.play_pause)
        self.add_bookmark_btn.clicked.connect(self.add_bookmark)
        self.delete_bookmark_btn.clicked.connect(self.delete_bookmark)
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        self.volume_slider.valueChanged.connect(self.change_volume)  
        self.bookmark_list_btn.clicked.connect(self.bookmark_panel)    
        self.bookmark_list.itemClicked.connect(self.seek_from_list)
        self.bookmark_list.itemClicked.connect(self.seek_from_list)

    def add_bookmark(self):
        fetch_timestamp = self.player.position()
        
        label, ok = QInputDialog.getText(self, "Add Bookmark", "Enter label:")
        if ok and label:
            bm = Bookmark(label=label, timestamp=fetch_timestamp, filepath=self.current_filepath)
            self.bookmark_manager.add_bookmark(bm)
            self.slider.set_bookmark(self.bookmark_manager.load(self.current_filepath))
            self.update_bookmark_list()

    def delete_bookmark(self):
        fetch_position = self.player.position()
        bookmarks = self.bookmark_manager.load(self.current_filepath)
        if not bookmarks:
            return
        delete_closestbookmark = min(bookmarks, key=lambda b: abs(b.timestamp - fetch_position))
        self.bookmark_manager.delete_bookmark(self.current_filepath,delete_closestbookmark.timestamp)
        self.slider.set_bookmark(self.bookmark_manager.load(self.current_filepath))
        self.update_bookmark_list()

    def change_theme(self,theme):
        if theme == "Dark Grey":
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; }
                QPushButton { font-weight: bold ; background-color: #3c3f41; color: white; }                
                QPushButton { background-color: #3c3f41; color: white; }
                QPushButton:hover { background-color: #4c5052; }
                QSlider::groove:horizontal { background-color: #ff8c00; height: 10px;    }
                QSlider::handle:horizontal { background-color: white;}
                QSlider::handle:horizontal {border-radius: 8px; width: 20px; height: 16px;}
                QComboBox { background-color: white; color: black; }
                QComboBox {font-weight: bold}
                QInputDialog { background-color: #111111; color: white; }
                QLineEdit { background-color: #222222; color: white; border: 1px solid #555; }
                QLabel { color: white; }
                QComboBox QAbstractItemView{background-color:white; color-black}
                QComboBox { outline: none; border: 1px solid #555; }
                QListWidget { background-color: #3c3f41; color: white; }
                QListWidget::item:selected { background-color: #555555; }
            """)
            self.slider.set_marker_color("white")
        

        elif theme == "Pure Black":
            self.setStyleSheet("""
                QWidget { background-color: #000000;  }
                QPushButton { font-weight: bold }     
                QPushButton { background-color: white; color: black;}
                QPushButton:hover { background-color: #868686; }
                QSlider::groove:horizontal { background-color: #ff8c00; height: 10px;  }
                QSlider::handle:horizontal { background-color: white;}
                QSlider::handle:horizontal {border-radius: 8px; width: 20px; height: 16px;}
                QComboBox { background-color: white; color: black; }
                QComboBox {font-weight: bold}
                QInputDialog { background-color: #111111; color: white; }
                QLineEdit { background-color: #222222; color: white; border: 1px solid #555; }
                QLabel { color: white; }
                QComboBox QAbstractItemView{background-color:white; color-black}
                QComboBox { outline: none; border: 1px solid #555; }
                QListWidget { background-color: #111111; color: white; }
                QListWidget::item:selected { background-color: #333333; }                 
            """)
            self.slider.set_marker_color("orange")
        else:
            self.setStyleSheet("""
                QWidget { background-color: #FFFFFF; }
                QPushButton { font-weight: bold }          
                QPushButton { background-color: #E7E7E7; color: black; }
                QPushButton:hover { background-color: #FFFFFF; }
                QSlider::groove:horizontal { background-color: #ff8c00; height: 10px;  }
                QSlider::handle:horizontal { background-color: white;}
                QSlider::handle:horizontal {border-radius: 8px; width: 20px; height: 16px;}
                QComboBox { background-color: white; color: black; }
                QComboBox {font-weight: bold}
                QComboBox QAbstractItemView{background-color:white; color-black}  
                QComboBox { outline: none; border: 1px solid #555; }
                QListWidget { background-color: #f0f0f0; color: black; }
                QListWidget::item:selected { background-color: #0078d4; color: white; }        
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

    def open_explorer(self):
        self.open_file()
        
    def new_bookmarkshot(self):
        self.add_bookmark()

    def delete_bookmarkshot(self):
        self.delete_bookmark()

    def control_autohide(self):

        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide_controls)
        self.setMouseTracking(True)
        self.central_Widget.setMouseTracking(True)
        self.hide_timer.start(3000)
        self.video_widget.setMouseTracking(True)
        self.slider.setMouseTracking(True)
        self.open_btn.setMouseTracking(True)
        self.play_btn.setMouseTracking(True)
        self.add_bookmark_btn.setMouseTracking(True)
        self.delete_bookmark_btn.setMouseTracking(True)
        self.theme_selector.setMouseTracking(True)
        self.current_time_label.setMouseTracking(True)
        self.total_time_label.setMouseTracking(True)
        
    def hide_controls(self):

        self.slider.hide()
        self.current_time_label.hide()
        self.total_time_label.hide()
        self.open_btn.hide()
        self.play_btn.hide()
        self.add_bookmark_btn.hide()
        self.delete_bookmark_btn.hide()
        self.theme_selector.hide()
        self.volume_label.hide()
        self.volume_slider.hide()
        self.bookmark_list_btn.hide()
       
    def show_controls(self):

        self.slider.show()
        self.current_time_label.show()
        self.total_time_label.show()
        self.open_btn.show()
        self.play_btn.show()
        self.add_bookmark_btn.show()
        self.delete_bookmark_btn.show()
        self.theme_selector.show()
        self.volume_label.show()
        self.volume_slider.show()
        self.bookmark_list_btn.show()

    def mouseMoveEvent(self,ev):

        self.show_controls()
        self.hide_timer.start(2000)
        super().mouseMoveEvent(ev)

    def change_volume(self,value):
        self.player.setVolume(value)

    def bookmark_panel(self):
        if self.bookmark_list.isVisible():
            self.bookmark_list.hide()
        else:
            self.bookmark_list.show()

    def update_bookmark_list(self):
        check_book = self.bookmark_manager.load(self.current_filepath)
        print(check_book)
        self.bookmark_list.clear()
        for i in check_book:
            items  = QListWidgetItem(f"{self.format_time(i.timestamp)} - {i.label}")
            items.setData(Qt.UserRole , i.timestamp)
            self.bookmark_list.addItem(items)

    def seek_from_list(self,item):
        timestamp = item.data(Qt.UserRole)
        self.player.setPosition(timestamp)

