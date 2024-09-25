# SPDX-FileCopyrightText: 2024 Konstantinos Diamantis <konstantinos.diamantis@cern.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

from PyQt6 import uic
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QColor, QDesktopServices, QFont
from PyQt6.QtWidgets import *

import mmbse_client.mmbse as mmbse
import roxie_3ml.py_files.mmbse_gui as mmbse_gui
import roxie_3ml.py_files.system_models_window as system_models_window
from roxie_3ml.py_files.post_system_window import PostSystem
from roxie_3ml.py_files.styles import *


class SystemsWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        ui_file = os.path.join(os.path.dirname(__file__), "./../ui_files/systems.ui")
        uic.loadUi(ui_file, self)
        # self.showMaximized()
        self.cols = ["id", "name", "description", "owner", "created_at"]
        self.models = uic.loadUi(ui_file, self)
        self.setMouseTracking(True)
        self.token = token
        # self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.tableModels.cellClicked.connect(self.handleCellClicked)
        self.button_close.clicked.connect(self.close)
        self.button_return_main.clicked.connect(self.return_to_main_window)
        self.button_post_system.clicked.connect(self.open_create_systemWin)
        self.client = mmbse.MMBSE(self.token)
        self.user = self.client.get_user_details()
        self.systems = self.client.get_systems()
        self.models.tableModels.setMaximumHeight(len(self.systems) * 45)
        # Set font for the entire table
        font = QFont("MS Shell Dlg 2", 10)  # Specify the font family and size
        self.models.tableModels.setFont(font)
        self.label_logged.setStyleSheet("color: green;")
        self.label_insert_user.setStyleSheet("color: green;")
        self.label_insert_user.setText((self.user["extra_data"]["preferred_username"]))
        self.label_insert_email.setText((self.user["extra_data"]["email"]))
        self.label_insert_cern_id.setText((self.user["extra_data"]["cern_person_id"]))
        self.tableModels.setStyleSheet(GLOBAL_TABLE_STYLE)
        self.doAddViewButtons()
        self.doAlignColumns()
        self.setStyleSheet(GLOBAL_BUTTON_STYLE)
        self.doHeadersBold()
        self.doColumnsFont()
        self.doCleanDates()
        self.doColumnWidth()

    def doColumnWidth(self):
        self.tableModels.resizeColumnToContents(3)
        self.tableModels.setColumnWidth(0, 80)
        self.tableModels.setColumnWidth(5, 120)
        self.tableModels.setColumnWidth(6, 120)
        self.tableModels.setColumnWidth(2, 290)

    def applyFormatting(self, item):
        if item:
            font = QFont("MS Shell Dlg 2", 10)
            font.setUnderline(True)
            cern_blue = QColor(7, 68, 250)  # RGB values for CERN blue
            item.setForeground(cern_blue)
            item.setFont(font)

    def doColumnsFont(self):
        for row in range(self.tableModels.rowCount()):
            item = self.tableModels.item(
                row, self.tableModels.columnCount() - 1
            )  # Last column
            self.applyFormatting(item)
            item = self.tableModels.item(
                row, self.tableModels.columnCount() - 2
            )  # 2nd to last column
            self.applyFormatting(item)

    def doCleanDates(self):
        for row in range(self.models.tableModels.rowCount()):
            date_item = self.tableModels.item(row, 4)
            original_text = date_item.text()
            cleaned_text = (
                original_text.split("T")[0] if "T" in original_text else original_text
            )
            date_item.setText(cleaned_text)

    def doHeadersBold(self):
        font = QFont()
        font.setBold(True)
        for col in range(self.tableModels.columnCount()):
            item = self.tableModels.horizontalHeaderItem(col)
            if item:
                item.setFont(font)

    def doAlignColumns(self):
        columns_to_align = [0, 4, 5, 6]  # Change this to the desired column indices
        for row, _ in enumerate(self.systems):
            for column in columns_to_align:
                item = self.models.tableModels.item(row, column)
                if item is not None:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def doAddViewButtons(self):
        # View Models
        for row, _ in enumerate(self.systems):
            self.models.tableModels.insertRow(row)
            for column, _ in enumerate(self.cols):
                self.models.tableModels.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(self.systems[row][self.cols[column]])),
                )
            # item_icon = QTableWidgetItem("View Model")
            # item_icon.setIcon(QIcon("/workspaces/roxie/mmbse-client/mmbse_gui/icons/monitor.svg"))
            self.models.tableModels.setItem(
                row, len(self.cols), QTableWidgetItem("View Models")
            )
            self.models.tableModels.setItem(
                row, len(self.cols) + 1, QTableWidgetItem("View Report")
            )

    def handleCellClicked(self, row, column):
        # Check if the clicked cell is the last cell
        if column == self.tableModels.columnCount() - 1:
            item = self.tableModels.item(row, column)
            if item.text() == "View Report":
                item = self.models.tableModels.item(row, 0)
                id = item.text()
                # QMessageBox.information(
                #     self,
                #     "Cell Clicked",
                #     f"Last cell clicked! Row: {row}, Column: {column}, ID: {id}.",
                # )
                report_url = "https://mmbse.app.cern.ch/"
                QDesktopServices.openUrl(QUrl(report_url))

        # Check if the clicked cell is the View Models cell
        if column == self.tableModels.columnCount() - 2:
            item = self.tableModels.item(row, column)
            if item.text() == "View Models":
                item = self.models.tableModels.item(row, 0)
                id = item.text()
                # QMessageBox.information(
                #     self,
                #     "Cell Clicked",
                #     f"Last cell clicked! Row: {row}, Column: {column}, ID: {id}.",
                # )
                self.open_system_models_win(id)

    def open_system_models_win(self, id):
        self.w = system_models_window.SystemModelsWindow(id, self.token)
        self.w.show()
        self.hide()

    def return_to_main_window(self):
        self.w = mmbse_gui.ROXIE_Gui(self.token)
        self.w.show()
        self.hide()

    def open_create_systemWin(self):
        self.w = PostSystem(self.token)
        self.w.show()
        self.hide()
