import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFontDatabase  # Import QFontDatabase
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QLineEdit, QStatusBar, QMessageBox, \
    QFileDialog


class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

        nav_toolbar = QToolBar("Navigation")
        self.addToolBar(nav_toolbar)

        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Back to the previous page")
        back_btn.triggered.connect(self.browser.back)
        nav_toolbar.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.setStatusTip("Forward to the next page")
        forward_btn.triggered.connect(self.browser.forward)
        nav_toolbar.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        nav_toolbar.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go to the home page")
        home_btn.triggered.connect(self.navigate_home)
        nav_toolbar.addAction(home_btn)

        nav_toolbar.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        nav_toolbar.addWidget(self.urlbar)

        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading the current page")
        stop_btn.triggered.connect(self.browser.stop)
        nav_toolbar.addAction(stop_btn)

        self.browser.urlChanged.connect(self.update_urlbar)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Connect the loadFinished signal to show an alert when the page is loaded.
        self.browser.loadFinished.connect(self.page_loaded_alert)

        # Create a QWebEnginePage instance for handling downloads
        self.download_page = QWebEnginePage(self)
        self.download_page.profile().downloadRequested.connect(self.handle_download_request)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def page_loaded_alert(self, ok):
        if ok:
            QMessageBox.information(self, "Page Loaded", "The page has finished loading.")

    def handle_download_request(self, download_item):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File", download_item.path(), options=options)
        if save_path:
            QMessageBox.information(self, "save_path", save_path)
            download_item.setPath(save_path)
            download_item.accept()

def main():
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("path_to_font_file.ttf")  # Replace with the actual path to the font file
    window = WebBrowser()
    window.setWindowTitle("Python Web Browser")
    window.setGeometry(100, 100, 1024, 768)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


#
# import sys
# from qtpy.QtCore import *
# from qtpy.QtWidgets import *
# from qtpy.QtWebEngineWidgets import *
#
# class WebBrowser(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.browser = QWebEngineView()
#         self.browser.setUrl(QUrl("https://www.google.com/"))
#         self.setCentralWidget(self.browser)
#
#         nav_toolbar = QToolBar("Navigation")
#         self.addToolBar(nav_toolbar)
#
#         back_btn = QAction("Back", self)
#         back_btn.setStatusTip("Back to previous page")
#         back_btn.triggered.connect(self.browser.back)
#         nav_toolbar.addAction(back_btn)
#
#         forward_btn = QAction("Forward", self)
#         forward_btn.setStatusTip("Forward to next page")
#         forward_btn.triggered.connect(self.browser.forward)
#         nav_toolbar.addAction(forward_btn)
#
#         reload_btn = QAction("Reload", self)
#         reload_btn.setStatusTip("Reload page")
#         reload_btn.triggered.connect(self.browser.reload)
#         nav_toolbar.addAction(reload_btn)
#
#         home_btn = QAction("Home", self)
#         home_btn.setStatusTip("Go to the home page")
#         home_btn.triggered.connect(self.navigate_home)
#         nav_toolbar.addAction(home_btn)
#
#         nav_toolbar.addSeparator()
#
#         self.urlbar = QLineEdit()
#         self.urlbar.returnPressed.connect(self.navigate_to_url)
#         nav_toolbar.addWidget(self.urlbar)
#
#         stop_btn = QAction("Stop", self)
#         stop_btn.setStatusTip("Stop loading the current page")
#         stop_btn.triggered.connect(self.browser.stop)
#         nav_toolbar.addAction(stop_btn)
#
#         self.browser.urlChanged.connect(self.update_urlbar)
#         self.status = QStatusBar()
#         self.setStatusBar(self.status)
#
#         # Connect the loadFinished signal to show an alert when the page is loaded.
#         self.browser.loadFinished.connect(self.page_loaded_alert)
#
#     def navigate_home(self):
#         self.browser.setUrl(QUrl("https://www.google.com/"))
#
#     def navigate_to_url(self):
#         q = QUrl(self.urlbar.text())
#         if q.scheme() == "":
#             q.setScheme("http")
#         self.browser.setUrl(q)
#
#     def update_urlbar(self, q):
#         self.urlbar.setText(q.toString())
#         self.urlbar.setCursorPosition(0)
#
#     def page_loaded_alert(self, ok):
#         if ok:
#             QMessageBox.information(self, "Page Loaded", "The page has finished loading.")
#
# def main():
#     app = QApplication(sys.argv)
#     QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
#     window = WebBrowser()
#     window.setWindowTitle("Python Web Browser")
#     window.setGeometry(100, 100, 1024, 768)
#     window.show()
#     sys.exit(app.exec_())
#
# if __name__ == "__main__":
#     main()
#
