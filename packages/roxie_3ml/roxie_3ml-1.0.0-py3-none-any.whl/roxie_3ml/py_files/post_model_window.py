# SPDX-FileCopyrightText: 2024 Konstantinos Diamantis <konstantinos.diamantis@cern.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import *

import mmbse_client.mmbse as mmbse
import roxie_3ml.py_files.mmbse_gui as mmbse_gui
import roxie_3ml.py_files.system_models_window as system_models_window
from roxie_3ml.py_files.styles import *


class PostModel(QMainWindow):
    def __init__(self, token, system_id):
        super().__init__()
        ui_file = os.path.join(os.path.dirname(__file__), "./../ui_files/post_model.ui")
        uic.loadUi(ui_file, self)
        self.token = token
        self.system_ID = system_id
        self.button_close.clicked.connect(self.close)
        self.button_create_model.clicked.connect(self.create_model)
        self.button_return_main.clicked.connect(self.return_to_main_window)
        self.client = mmbse.MMBSE(self.token)
        self.user = self.client.get_user_details()
        self.systems = self.client.get_systems()
        # Set font for the entire table
        # font = QFont("MS Shell Dlg 2", 10)  # Specify the font family and size
        # self.models.tableModels.setFont(font)
        self.label_logged.setStyleSheet("color: green;")
        self.label_insert_user.setStyleSheet("color: green;")
        self.label_insert_user.setText((self.user["extra_data"]["preferred_username"]))
        self.label_insert_email.setText((self.user["extra_data"]["email"]))
        self.label_insert_cern_id.setText((self.user["extra_data"]["cern_person_id"]))
        self.label_top.setText(
            f"You are going to create a model for System with ID {system_id}:\n"
        )
        self.button_back_system.clicked.connect(self.retrun2systemID)
        self.button_back_system.setText(f"Return to System with ID {system_id}")
        self.populateBoxes()
        self.setStyleSheet(GLOBAL_BUTTON_STYLE)
        self.label_name_error.hide()
        self.label_descr_error.hide()

    def populateBoxes(self):
        TYPitems = ["ROXIE", "ANSYS"]
        DSitems = ["3D", "2D", "QUENCH", "IRON"]
        self.comboBox_Des_Step.addItems(DSitems)
        self.comboBox_Type.addItems(TYPitems)

    def return_to_main_window(self):
        self.w = mmbse_gui.ROXIE_Gui(self.token)
        self.w.show()
        self.hide()

    def retrun2systemID(self):
        self.w = system_models_window.SystemModelsWindow(self.system_ID, self.token)
        self.w.show()
        self.hide()

    def create_model(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.hideLabel)
        if self.lineName.text() == "":
            self.label_name_error.show()
            self.timer.start(2200)
            self.label_name_error.setStyleSheet("color: red;")
        elif self.lineDescr.text() == "":
            self.label_descr_error.show()
            self.timer.start(2200)
            self.label_descr_error.setStyleSheet("color: red;")
        else:
            try:
                self.client.create_model(
                    system=self.system_ID,
                    name=self.lineName.text(),
                    description=self.lineDescr.text(),
                    design_step=self.comboBox_Des_Step.currentText(),
                    type=self.comboBox_Type.currentText(),
                )
                QMessageBox.information(
                    self,
                    "Success",
                    f"You created a new model for system {self.system_ID} successfully.",
                )
                self.lineDescr.clear()
                self.lineName.clear()
            except Exception:
                QMessageBox.critical(
                    self,
                    "Error",
                    "An unexpected error occurred and the model was not created successfully. Check the remote database.",
                )

    def hideLabel(
        self,
    ):
        self.label_name_error.hide()
        self.label_descr_error.hide()
