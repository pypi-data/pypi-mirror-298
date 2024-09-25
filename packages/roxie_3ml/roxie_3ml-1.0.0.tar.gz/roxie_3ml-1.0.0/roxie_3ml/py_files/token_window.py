# SPDX-FileCopyrightText: 2024 Konstantinos Diamantis <konstantinos.diamantis@cern.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

from PyQt6 import uic
from PyQt6.QtCore import QSettings, QTimer, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import *

import mmbse_client.mmbse as mmbse
import roxie_3ml.py_files.mmbse_gui as mmbse_gui
from roxie_3ml.py_files.styles import *


class TokenLoginWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        ui_file = os.path.join(os.path.dirname(__file__), "./../ui_files/login.ui")
        uic.loadUi(ui_file, self)
        self.button_cancel.clicked.connect(self.close)
        self.button_open_db.clicked.connect(self.open_db)
        self.button_login.clicked.connect(self.login)
        # self.center_window()
        self.setStyleSheet(GLOBAL_BUTTON_STYLE)
        # self.lineEdit.editingFinished.connect(self.fill_API)
        self.lineEdit.setPlaceholderText("API Token")
        self.lineEdit.setStyleSheet(GLOBAL_LINE_STYLESHEET)
        self.label.setStyleSheet(GLOBAL_LABEL_STYLESHEET)
        self.setStyleSheet(GLOBAL_BUTTON_STYLE)
        self.label_wrong_input.hide()

    def open_db(self):
        QDesktopServices.openUrl(QUrl("https://mmbse.app.cern.ch/"))

    def login(self):
        token_text = self.lineEdit.text()
        client = mmbse.MMBSE(token_text)
        if not token_text:
            self.timer = QTimer()
            self.timer.timeout.connect(self.hideLabel)
            self.timer.start(2200)
            self.label_wrong_input.show()
            self.label_wrong_input.setText("Token cannot be blank")
            self.label_wrong_input.setStyleSheet("color: red;")
        else:
            if client.is_authenticated():
                # Display a message box for 3 seconds
                self.label_wrong_input.setText("Correct Token.")
                self.label_wrong_input.setStyleSheet("color: green;")
                self.label_wrong_input.show()
                message_box = QMessageBox()
                message_box.setWindowTitle("Logging In")
                message_box.setText("Logging in... Please wait...")
                message_box.setStandardButtons(QMessageBox.StandardButton.Cancel)
                QTimer.singleShot(1500, message_box.close)
                message_box.move(self.pos())
                message_box.exec()
                self.main_window.close()
                # Token Manager - save the token
                if self.cache_checkBox.isChecked():
                    token_manager = TokenManager()
                    token_manager.save_token(token_text)
                self.main_window = mmbse_gui.ROXIE_Gui(token_text)
                self.main_window.move(self.pos())
                self.close()
            else:
                self.timer = QTimer()
                self.timer.timeout.connect(self.hideLabel)
                self.timer.start(2200)
                self.label_wrong_input.show()
                self.label_wrong_input.setText("Wrong Token. Please try again.")
                self.label_wrong_input.setStyleSheet("color: red;")

    def hideLabel(
        self,
    ):
        self.label_wrong_input.hide()


class TokenManager:
    """A class to manage the storage of personal tokens."""

    def __init__(self):
        self.settings = QSettings("CERN", "ROXIE-MMBSE")

    def save_token(self, token):
        self.settings.setValue("personal_token", token)

    def load_token(self):
        return self.settings.value("personal_token")

    def clear_token(self):
        self.settings.remove("personal_token")
