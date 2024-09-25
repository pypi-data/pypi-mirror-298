# SPDX-FileCopyrightText: 2024 Konstantinos Diamantis <konstantinos.diamantis@cern.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os

from PyQt6 import uic
from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtGui import QDesktopServices, QIcon
from PyQt6.QtWidgets import *

import mmbse_client.mmbse as mmbse
from roxie_3ml.py_files.push_files_db_window import PushFileDB
from roxie_3ml.py_files.styles import *
from roxie_3ml.py_files.systems_window import SystemsWindow
from roxie_3ml.py_files.token_window import TokenLoginWindow, TokenManager
from PyQt6.QtCore import QSettings





class ROXIE_Gui(QMainWindow):
    def __init__(self, token, base_url=None):
        super(ROXIE_Gui, self).__init__()
        ui_file = os.path.join(os.path.dirname(__file__), "./../ui_files/main_mmbse.ui")
        uic.loadUi(ui_file, self)
        self.show()
        self.token = token
        self.base_url = base_url if base_url else "https://mmbse.app.cern.ch/api" 
        self.client = mmbse.MMBSE(self.token, self.base_url)
        self.button_cancel.clicked.connect(self.close)
        self.button_open_db.clicked.connect(self.open_db)
        self.button_models.clicked.connect(self.open_models_ui)
        self.button_login.clicked.connect(self.login_logout)
        self.button_push_model.clicked.connect(self.push_local_model)
        self.label_systems_error.setText("")
        self.actionSet_Path.triggered.connect(self.set_path_action_triggered)
        self.actionShow_Path.triggered.connect(self.show_path_action_triggered)
        # Set global stylesheet for all QPushButton widgets
        self.setStyleSheet(GLOBAL_BUTTON_STYLE)
        self.center_window()  # Center the window
        self.path_manager = PathManager()

    def set_path_action_triggered(self):
        # Open a window to create a path
        db_path = QFileDialog.getExistingDirectory(
            self, "Select Local Database Path", ""
        )
        self.path_manager.set_path(db_path)

    def show_path_action_triggered(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("Local Database Path")
        message_box.setText(
            f'All your models will be downlaoded under the path:\n\n "{self.path_manager.get_path()}"'
        )
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.setIcon(QMessageBox.Icon.Information)  # Set the information icon
        message_box.move(self.pos())
        message_box.exec()

    def center_window(self):
        # centerPoint = QScreen.availableGeometry(QApplication.primaryScreen().geometry().center())
        # fg = widget.frameGeometry()
        # fg.moveCenter(centerPoint)
        # widget.move(fg.topLeft())
        # # Get the frame geometry of the window
        # window_frame = self.frameGeometry()

        # # Get the center point of the screen geometry
        # # center_point = QDesktopWidget().screenGeometry().center()
        # center_point = QApplication.primaryScreen().geometry().center()

        # # Move the window center to the screen center
        # window_frame.moveCenter(center_point)
        # print(center_point)
        # Set the top-left position of the window frame

        # self.move(window_frame.topLeft().x, window_frame.topLeft().y)

        # Get the geometry of the screen
        screen_geometry = QApplication.primaryScreen().geometry()
        # Get the center point of the screen
        center_point = screen_geometry.center()
        # Calculate the new position of the window
        new_x = center_point.x() - self.width() // 2
        new_y = center_point.y() - self.height() // 2
        # Set the new position
        self.move(new_x, new_y)
        #         # Move the window to the center of the screen
        # window_geometry = self.frameGeometry()
        # center_point = QApplication.primaryScreen().geometry().center()
        # window_geometry.moveCenter(center_point)
        # self.move(window_geometry.topLeft())

        #         # Get the size of the window
        # window_geometry = self.frameGeometry()

        # # Get the center point of the screen
        # center_point = QApplication.primaryScreen().geometry().center()

        # # Move the window to the center of the screen
        # window_geometry.moveCenter(center_point)
        # self.move(window_geometry.topLeft())

        if self.client.is_authenticated():
            user = self.client.get_user_details()
            self.label_login.setText(
                f"You are logged in as \n{user['extra_data']['preferred_username']}."
            )
            self.label_login.setStyleSheet("color: green;")
            self.label_welcome.setText(
                f"Hello {user['extra_data']['given_name']}! Welcome to ROXIE Database."
            )
            self.button_login.setText("Log Out")
            icon_path = os.path.join(
                os.path.dirname(__file__), "../assets/icons/log-out.svg"
            )

            self.button_login.setIcon(QIcon(icon_path))

    def login_logout(self):
        if self.client.is_authenticated():
            self.logout()
        else:
            self.openLoginWindow()

    def logout(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("Logging Out")
        message_box.setText("Logging out... Please wait...")
        message_box.setStandardButtons(QMessageBox.StandardButton.Cancel)
        QTimer.singleShot(1500, message_box.close)
        message_box.move(self.pos())
        message_box.exec()
        self.main_window = ROXIE_Gui("")  # Pass username to the MainWindow
        self.main_window.move(self.pos())
        # Clean up token
        token_manager = TokenManager()
        token_manager.clear_token()
        self.close()

    def push_local_model(self):
        if self.client.is_authenticated():
            # Open a file dialog to select a file
            # QMessageBox.information(
            #     self,
            #     "ROXIE Model Selection",
            #     "If you would like to push a ROXIE model, please select only the .data file. "
            #     "If applicable, the dependencies will be pushed automatically.",
            # )
            # TODO Chaneg the button to Select, and .data files*s
            file_path = " "
            # if file_path:
            #    print("Selected file:", file_path)
            self.w = PushFileDB(self.token, file_path)
            self.w.show()
        else:
            self.label_login.setStyleSheet("color: red;")
            self.label_systems_error.setText(" You are logged out.")
            self.label_systems_error.setStyleSheet("color: red;")

    def openLoginWindow(self):
        self.new_window = TokenLoginWindow(self)
        self.new_window.move(self.pos())
        self.new_window.show()

    def open_db(self):
        QDesktopServices.openUrl(QUrl("https://mmbse.app.cern.ch/"))

    def open_models_ui(self):
        if self.client.is_authenticated():
            self.w = SystemsWindow(self.token)
            self.w.show()
            self.hide()
        else:
            self.label_login.setStyleSheet("color: red;")
            self.label_systems_error.setText(" You are logged out.")
            self.label_systems_error.setStyleSheet("color: red;")

    def reopenWithSession(self, new_session):
        self.close()
        new_main_window = ROXIE_Gui(new_session)
        new_main_window.show()


class PathManager:
    """A class to manage the storage of a global path."""

    def __init__(self):
        self.settings = QSettings("CERN", "3ML")
        self.set_default_path()

    def set_default_path(self):
        """Set a default path if it doesn't exist."""
        if (
            not self.settings.contains("database_path")
            or self.settings.value("database_path") == ""
        ):
            self.settings.setValue("database_path", "/tmp/roxie_db/")

    def set_path(self, path):
        """Set the global db path."""
        self.settings.setValue("database_path", path)

    def get_path(self):
        """Retrieve the global path."""
        return self.settings.value("database_path")
