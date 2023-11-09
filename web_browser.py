# python -m PyInstaller --onefile web_browser.py   to bild exe file


import base64
import os
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFontDatabase, QDesktopServices
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QLineEdit, QStatusBar, QMessageBox, \
    QFileDialog, QListWidget, QDialog, QVBoxLayout, QListWidgetItem, QAbstractItemView, QPushButton, QLabel
from pymongo import MongoClient


class RegistrationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Registration")
        layout = QVBoxLayout()
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_user)
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login_user)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.login_button)
        self.ID = None  # Initialize ID variable
        self.setLayout(layout)

    def register_user(self):
        username = self.username_input.text()
        email = self.email_input.text()

        if not (username and email):
            QMessageBox.warning(self, "Registration Error", "Both username and email are required.")
            return

        # Connect to MongoDB
        mongo_url = "mongodb+srv://otmanagement:otmanagement@otmanagement.prask0n.mongodb.net/"
        client = MongoClient(mongo_url)
        database = client['your_database_name']  # Replace 'your_database_name' with your actual database name
        collection = database['users']

        # Check if username or email already exists
        existing_user = collection.find_one({"$or": [{"username": username}, {"email": email}]})

        if existing_user:
            QMessageBox.warning(self, "Registration Error", "Username or email already exists.")
            client.close()
            return

        # Create a new document with an autogenerated ID
        user_data = {
            "username": username,
            "email": email
        }
        result = collection.insert_one(user_data)

        # Print the autogenerated ID
        print(f"User registered - Username: {username}, Email: {email}, ID: {result.inserted_id}")

        # Close the MongoDB connection
        client.close()

        self.accept()

    def login_user(self):
        username = self.username_input.text()
        email = self.email_input.text()

        if not (username and email):
            QMessageBox.warning(self, "Login Error", "Both username and email are required.")
            return

        # Connect to MongoDB
        mongo_url = "mongodb+srv://otmanagement:otmanagement@otmanagement.prask0n.mongodb.net/"
        client = MongoClient(mongo_url)
        database = client['your_database_name']  # Replace 'your_database_name' with your actual database name
        collection = database['users']

        # Check if the user exists
        existing_user = collection.find_one({"$or": [{"username": username}, {"email": email}]})

        if existing_user:
            # Store the _id in the ID variable
            self.ID = str(existing_user['_id'])
            print(f"User registered - Username: {username}, Email: {email}, ID: {self.ID}")
            QMessageBox.information(self, "Login Successful", f"Login successful! User ID: {self.ID}")
        else:
            QMessageBox.warning(self, "Login Error", "User not found. Please register first.")

        # Close the MongoDB connection
        client.close()

        self.accept()


class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        if not self.user_exists():
            registration_dialog = RegistrationDialog()
            if registration_dialog.exec_() != QDialog.Accepted:
                sys.exit()

        self.ID = registration_dialog.ID

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

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

        # Add a "View Downloads" button to the navigation toolbar
        view_downloads_btn = QAction("View Downloads", self)
        view_downloads_btn.setStatusTip("View downloaded files")
        view_downloads_btn.triggered.connect(self.view_downloads)
        nav_toolbar.addAction(view_downloads_btn)

        self.downloads_list = QListWidget()  # Create a list widget to display downloaded files
        self.downloads_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.downloads_list.itemDoubleClicked.connect(self.open_selected_download)

        self.downloads_list = QListWidget()  # Create a list widget to display downloaded files

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


    def user_exists(self):
        # You can check if a user exists by checking your storage method
        # In this example, we assume that if a user is registered, a file named "user.txt" exists.
        return os.path.exists("user.txt")

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
            QMessageBox.information(self, "Page Loaded", f"The page has finished loading. User ID: {self.ID}")

    def view_downloads(self):
        print("HEllo")
        # Create a dialog to display downloaded files
        dialog = QDialog(self)
        dialog.setWindowTitle("Downloads")

        layout = QVBoxLayout()
        layout.addWidget(self.downloads_list)
        dialog.setLayout(layout)

        # Populate the downloads list with downloaded files
        storage_dir = 'storage'
        if os.path.exists(storage_dir):
            downloaded_files = os.listdir(storage_dir)
            for file_name in downloaded_files:
                item = QListWidgetItem(file_name)
                self.downloads_list.addItem(item)

        dialog.exec_()

    def open_selected_download(self):
        selected_item = self.downloads_list.currentItem()
        if selected_item:
            file_name = selected_item.text()
            storage_dir = 'storage'
            file_path = os.path.join(storage_dir, file_name)

            if os.path.exists(file_path):
                # Use QDesktopServices to open the file with the default application
                if QDesktopServices.openUrl(QUrl.fromLocalFile(file_path)):
                    print(f"File opened successfully: {file_path}")
                else:
                    print(f"Failed to open file: {file_path}")
            else:
                print(f"File does not exist: {file_path}")

    def handle_download_request(self, download_item):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        # Specify the directory where you want to save downloaded files
        storage_dir = 'storage'

        # Check if the storage directory exists, and if not, create it
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        # Get the suggested file name from the download item
        suggested_name = download_item.suggestedFileName()

        # Construct the full path to save the file in the storage directory
        save_path = os.path.join(storage_dir, suggested_name)

        # Show a file dialog for choosing the download location (optional)
        # save_path, _ = QFileDialog.getSaveFileName(self, "Save File", save_path, options=options)

        if save_path:
            download_item.setPath(save_path)
            download_item.accept()

            # Show a success message when the download is complete
            QMessageBox.information(self, "Download Success", f"Downloaded file saved to:\n{save_path}")

    def file_to_base64(self, binary_data):
        try:
            base64_data = base64.b64encode(binary_data).decode("utf-8")
            return base64_data
        except Exception as e:
            return None
def main():
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("path_to_font_file.ttf")
    window = WebBrowser()
    window.setWindowTitle("Python Web Browser")
    window.setGeometry(100, 100, 1024, 768)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()







# import base64
# import os
# import sys
# from PyQt5.QtCore import QUrl
# from PyQt5.QtGui import QFontDatabase, QDesktopServices  # Import QFontDatabase
# from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
# from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QLineEdit, QStatusBar, QMessageBox, \
#     QFileDialog, QListWidget, QDialog, QVBoxLayout, QListWidgetItem, QAbstractItemView
#
#
# class WebBrowser(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.browser = QWebEngineView()
#         self.browser.setUrl(QUrl("https://www.google.com"))
#         self.setCentralWidget(self.browser)
#
#         nav_toolbar = QToolBar("Navigation")
#         self.addToolBar(nav_toolbar)
#
#         back_btn = QAction("Back", self)
#         back_btn.setStatusTip("Back to the previous page")
#         back_btn.triggered.connect(self.browser.back)
#         nav_toolbar.addAction(back_btn)
#
#         forward_btn = QAction("Forward", self)
#         forward_btn.setStatusTip("Forward to the next page")
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
#         # Add a "View Downloads" button to the navigation toolbar
#         view_downloads_btn = QAction("View Downloads", self)
#         view_downloads_btn.setStatusTip("View downloaded files")
#         view_downloads_btn.triggered.connect(self.view_downloads)
#         nav_toolbar.addAction(view_downloads_btn)
#
#         self.downloads_list = QListWidget()  # Create a list widget to display downloaded files
#         self.downloads_list.setSelectionMode(QAbstractItemView.SingleSelection)
#         self.downloads_list.itemDoubleClicked.connect(self.open_selected_download)
#
#         self.downloads_list = QListWidget()  # Create a list widget to display downloaded files
#
#         self.browser.urlChanged.connect(self.update_urlbar)
#         self.status = QStatusBar()
#         self.setStatusBar(self.status)
#
#         # Connect the loadFinished signal to show an alert when the page is loaded.
#         self.browser.loadFinished.connect(self.page_loaded_alert)
#
#         # Create a QWebEnginePage instance for handling downloads
#         self.download_page = QWebEnginePage(self)
#         self.download_page.profile().downloadRequested.connect(self.handle_download_request)
#
#     def navigate_home(self):
#         self.browser.setUrl(QUrl("https://www.google.com"))
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
#     def view_downloads(self):
#         print("HEllo")
#         # Create a dialog to display downloaded files
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Downloads")
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.downloads_list)
#         dialog.setLayout(layout)
#
#         # Populate the downloads list with downloaded files
#         storage_dir = 'storage'
#         if os.path.exists(storage_dir):
#             downloaded_files = os.listdir(storage_dir)
#             for file_name in downloaded_files:
#                 item = QListWidgetItem(file_name)
#                 self.downloads_list.addItem(item)
#
#         dialog.exec_()
#
#     def open_selected_download(self):
#         selected_item = self.downloads_list.currentItem()
#         if selected_item:
#             file_name = selected_item.text()
#             storage_dir = 'storage'
#             file_path = os.path.join(storage_dir, file_name)
#
#             if os.path.exists(file_path):
#                 # Use QDesktopServices to open the file with the default application
#                 if QDesktopServices.openUrl(QUrl.fromLocalFile(file_path)):
#                     print(f"File opened successfully: {file_path}")
#                 else:
#                     print(f"Failed to open file: {file_path}")
#             else:
#                 print(f"File does not exist: {file_path}")
#
#     def handle_download_request(self, download_item):
#         options = QFileDialog.Options()
#         options |= QFileDialog.ReadOnly
#
#         # Specify the directory where you want to save downloaded files
#         storage_dir = 'storage'
#
#         # Check if the storage directory exists, and if not, create it
#         if not os.path.exists(storage_dir):
#             os.makedirs(storage_dir)
#
#         # Get the suggested file name from the download item
#         suggested_name = download_item.suggestedFileName()
#
#         # Construct the full path to save the file in the storage directory
#         save_path = os.path.join(storage_dir, suggested_name)
#
#         # Show a file dialog for choosing the download location (optional)
#         # save_path, _ = QFileDialog.getSaveFileName(self, "Save File", save_path, options=options)
#
#         if save_path:
#             download_item.setPath(save_path)
#             download_item.accept()
#
#             # Show a success message when the download is complete
#             QMessageBox.information(self, "Download Success", f"Downloaded file saved to:\n{save_path}")
#
#     def file_to_base64(self, binary_data):
#         try:
#             base64_data = base64.b64encode(binary_data).decode("utf-8")
#             return base64_data
#         except Exception as e:
#             return None
# def main():
#     app = QApplication(sys.argv)
#     QFontDatabase.addApplicationFont("path_to_font_file.ttf")  # Replace with the actual path to the font file
#     window = WebBrowser()
#     window.setWindowTitle("Python Web Browser")
#     window.setGeometry(100, 100, 1024, 768)
#     window.show()
#     sys.exit(app.exec_())
#
# if __name__ == "__main__":
#     main()