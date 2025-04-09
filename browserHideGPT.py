import sys
from PyQt6.QtCore import QUrl, Qt, QPoint
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar,
    QLineEdit, QSystemTrayIcon, QMenu, QFrame
)
from PyQt6.QtGui import QAction, QIcon, QShortcut, QKeySequence
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
import ctypes

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Browser")
        self.setFixedSize(500, 700)
        self.setGeometry(950, 50, 500, 500)

        # Initial opacity settings
        self.normal_opacity = 0.8  # Normal opacity (80%)
        self.transparent_opacity = 0.3  # Transparent opacity (30%)
        self.setWindowOpacity(self.normal_opacity)

        # Hide the taskbar icon and make the window frameless
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)

        # WebEngine View
        self.browser = QWebEngineView()
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.browser.setUrl(QUrl("https://deepai.org/chat"))  # Run ChatGPT
        self.setCentralWidget(self.browser)
        hwnd = int(self.winId())
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 17) # 17 = 0x00000011 , 1 = 0x00000001

        # Navigation Bar
        nav_bar = QToolBar()

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        # Update URL bar on URL change
        self.browser.urlChanged.connect(self.update_url)

        tray_menu = QMenu()
        toggle_visibility_action = QAction("Toggle Visibility", self)
        quit_action = QAction("Quit", self)
        toggle_visibility_action.triggered.connect(self.toggle_window_visibility)
        quit_action.triggered.connect(app.quit)
        tray_menu.addAction(toggle_visibility_action)
        tray_menu.addAction(quit_action)

        self.shortcut_toggle_visibility = QShortcut(QKeySequence("Ctrl+H"), self)
        self.shortcut_quit = QShortcut(QKeySequence("Ctrl+Q"), self)

        self.shortcut_toggle_visibility.activated.connect(self.toggle_window_visibility)
        self.shortcut_quit.activated.connect(app.quit)

        # Shortcut for toggling the draggable border with Ctrl+B
        self.shortcut_toggle_border = QShortcut(QKeySequence("Ctrl+B"), self)
        self.shortcut_toggle_border.activated.connect(self.toggle_border_visibility)

        # Variables for window movement and resizing
        self.dragging = False
        self.resizing = False
        self.offset = QPoint()
        self.resize_direction = None

        # Add a draggable border
        self.border_width = 10  # Width of the draggable border
        self.container = self.create_draggable_border()

        # Initially, hide the border
        self.container.setVisible(False)

    def create_draggable_border(self):
        """Create a draggable border around the window."""
        container = QFrame(self)
        container.setObjectName("BorderContainer")
        container.setStyleSheet("""
            QFrame#BorderContainer {
                background-color: rgba(0, 0, 0, 50);  
                border: 2px solid #FF69B4;           /* Red border */
                border-radius: 10px;
            }
        """)
        container.setGeometry(0, 0, self.width(), self.height())

        # Make the entire border draggable
        container.mousePressEvent = self.mousePressEvent
        container.mouseMoveEvent = self.mouseMoveEvent
        container.mouseReleaseEvent = self.mouseReleaseEvent

        return container

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def toggle_window_visibility(self):
        """Toggle between normal opacity and transparent opacity."""
        current_opacity = self.windowOpacity()
        if current_opacity == self.normal_opacity:
            self.setWindowOpacity(self.transparent_opacity)
            print("Window made transparent.")
        else:
            self.setWindowOpacity(self.normal_opacity)
            self.activateWindow()  # Bring the window to the foreground
            self.raise_()          # Raise the window above others
            print("Window restored to normal opacity.")

    def toggle_border_visibility(self):
        """Toggle the visibility of the draggable border."""
        current_visibility = self.container.isVisible()
        self.container.setVisible(not current_visibility)
        if not current_visibility:
            print("Draggable border enabled.")
        else:
            print("Draggable border disabled.")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Detect resizing area
            if event.pos().x() < self.border_width:  # Left border
                self.resizing = True
                self.resize_direction = 'left'
            elif event.pos().x() > self.width() - self.border_width:  # Right border
                self.resizing = True
                self.resize_direction = 'right'
            elif event.pos().y() < self.border_width:  # Top border
                self.resizing = True
                self.resize_direction = 'top'
            elif event.pos().y() > self.height() - self.border_width:  # Bottom border
                self.resizing = True
                self.resize_direction = 'bottom'
            else:
                self.dragging = True
                self.offset = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self.dragging:
            # Calculate the new position for moving the window
            new_position = self.mapToGlobal(event.position().toPoint() - self.offset)
            self.move(new_position)

        elif self.resizing:
            if self.resize_direction == 'left':
                delta = event.position().x() - self.offset.x()
                self.setGeometry(self.x() + delta, self.y(), self.width() - delta, self.height())
            elif self.resize_direction == 'right':
                delta = event.position().x() - self.offset.x()
                self.setGeometry(self.x(), self.y(), self.width() + delta, self.height())
            elif self.resize_direction == 'top':
                delta = event.position().y() - self.offset.y()
                self.setGeometry(self.x(), self.y() + delta, self.width(), self.height() - delta)
            elif self.resize_direction == 'bottom':
                delta = event.position().y() - self.offset.y()
                self.setGeometry(self.x(), self.y(), self.width(), self.height() + delta)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.resizing = False

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Application has a system tray
    if not QSystemTrayIcon.isSystemTrayAvailable():
        sys.exit(1)
    app.setQuitOnLastWindowClosed(False)  # Prevent the app from quitting when the window is closed
    window = Browser()
    window.show()
    sys.exit(app.exec())
