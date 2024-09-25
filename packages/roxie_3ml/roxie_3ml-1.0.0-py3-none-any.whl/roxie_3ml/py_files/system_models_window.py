# SPDX-FileCopyrightText: 2024 Konstantinos Diamantis <konstantinos.diamantis@cern.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import threading

from PyQt6 import uic
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPixmap
from PyQt6.QtWidgets import *

import mmbse_client.mmbse as mmbse
import roxie_3ml.py_files.mmbse_gui as mmbse_gui
import roxie_3ml.py_files.systems_window as systems_window
from roxie_3ml.py_files.post_model_window import PostModel
from roxie_3ml.py_files.styles import *
import subprocess


class SystemModelsWindow(QMainWindow):
    """
    This window shows all the models of a specified and selected System.
    Model can be downloaded locally and/or loaded to ROXIE if it's a ROXIE type model.
    """

    def __init__(self, id, token):
        """
        Init the ui.

        Args:
            id (int): The system_id
            token (string): Private token to gain access to the 3ML
        """
        super().__init__()
        ui_file = os.path.join(
            os.path.dirname(__file__), "./../ui_files/sys_models_win.ui"
        )
        uic.loadUi(
            ui_file, self
        )  # Define a list of numbers (assuming you have 3 items)
        self.models = uic.loadUi(ui_file, self)
        self.setMouseTracking(True)
        self.token = token
        self.client = mmbse.MMBSE(self.token)

        if not self.client.is_authenticated():
            raise TokenInvalidError("Token is invalid")

        self.user = self.client.get_user_details()
        self.label_ID.setText(f"ID {id}.")
        font = QFont()
        font.setBold(True)
        self.label_ID.setFont(font)
        self.button_close.clicked.connect(self.close)
        self.label_logged.setStyleSheet("color: green;")
        self.label_insert_user.setStyleSheet("color: green;")
        self.label_insert_user.setText((self.user["extra_data"]["preferred_username"]))
        self.label_insert_email.setText((self.user["extra_data"]["email"]))
        self.label_insert_cern_id.setText((self.user["extra_data"]["cern_person_id"]))
        self.button_post_model.clicked.connect(self.open_post_model)
        self.button_return_main.clicked.connect(self.return_to_main_window)
        self.button_return_systems.clicked.connect(self.return_to_systems)
        systems = self.client.get_system_models(id)
        self.system_ID = id
        self.setStyleSheet(GLOBAL_BUTTON_STYLE)
        if not systems:  # Check if data is not empty
            self.label_descr_ID.setText(
                f"System with ID {id} does not have any models yet."
            )
            self.label_descr_ID.setStyleSheet("color: red;")
            self.label_ID.setText("")

        self.models.tableModels.setMaximumHeight(len(systems) * 45)
        # Set font for the entire table
        font = QFont("MS Shell Dlg 2", 10)
        self.models.tableModels.setFont(font)
        self.models.tableModels.setStyleSheet(GLOBAL_TABLE_STYLE)
        columns_to_align = [
            0,
            1,
            4,
            5,
            6,
            7,
            8,
            9,
        ]  # Change this to the desired column indices
        cols = [
            "id",
            "type",
            "name",
            "description",
            "design_step",
            "inputs",
            "outputs",
            "created_at",
        ]
        for row, _ in enumerate(systems):
            self.models.tableModels.insertRow(row)
            for column, _ in enumerate(cols):
                self.models.tableModels.setItem(
                    row, column, QTableWidgetItem(str(systems[row][cols[column]]))
                )
            self.models.tableModels.setItem(
                row, len(cols), QTableWidgetItem("Download")
            )
            if self.models.tableModels.item(row, 1).text() == "ROXIE":
                self.models.tableModels.setItem(
                    row, len(cols) + 1, QTableWidgetItem("Load")
                )
            else:
                self.models.tableModels.setItem(
                    row, len(cols) + 1, QTableWidgetItem("---")
                )
            for column in columns_to_align:
                item = self.models.tableModels.item(row, column)
                if item is not None:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # Connect cellClicked signal to slot
        self.tableModels.cellClicked.connect(self.handleCellClicked)
        self.doHeadersBold()
        self.doLastColumnFont()
        self.clean_dates()
        self.tableModels.setColumnWidth(0, 70)
        self.tableModels.setColumnWidth(1, 85)
        self.tableModels.setColumnWidth(2, 150)
        self.tableModels.setColumnWidth(3, 220)

    def applyFormatting(self, item):
        """
        Formatting for items in the table

        Args:
            item (_type_): _description_
        """
        if item:
            font = QFont("MS Shell Dlg 2", 10)
            font.setUnderline(True)
            cern_blue = QColor(7, 68, 250)  # RGB values for CERN blue
            item.setForeground(cern_blue)
            item.setFont(font)

    def doLastColumnFont(self):
        """
        Apply formatting to Last columns
        """
        for row in range(self.tableModels.rowCount()):
            if self.models.tableModels.item(row, 1).text() == "ROXIE":
                item = self.tableModels.item(
                    row, self.tableModels.columnCount() - 1
                )  # Last column
                self.applyFormatting(item)

            item = self.tableModels.item(
                row, self.tableModels.columnCount() - 2
            )  # 2nd to last column
            self.applyFormatting(item)

    def clean_dates(self):
        for row in range(self.models.tableModels.rowCount()):
            date_item = self.tableModels.item(row, 7)
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

    def write_to_pipe(self, filename):
        """
        Create FIFO pipe for IPC with TCL. The signal that is sent is the path of
        the local file from the roxiedb path and should always have a
        line breaker at the end.
        """
        if not os.path.exists(".pipe"):
            os.mkfifo(".pipe")
            os.chmod(".pipe", 0o777)
        with open(".pipe", "w") as pipe_file:
            pipe_file.write(filename + "\n")  # NEEDS LINE BREAK!!
            # print("Message sent successfully")
            # pipe_file.close()
        # except Exception as e:
        #     print("Error:", e)

    def show_waiting_box(self):
        """Wait while files are downloaded"""
        self.message_box = QMessageBox()
        self.message_box.setWindowTitle("Please Wait...")
        self.message_box.setText("Model is downloaded from Database..")
        self.message_box.show()
        QApplication.instance().setOverrideCursor(Qt.CursorShape.WaitCursor)
        # Create a QTimer to close the message box after x seconds
        self.timer = QTimer()
        self.timer.setInterval(3000)  # 4000 milliseconds = 4 seconds
        self.timer.timeout.connect(self.close_message_box)
        self.timer.start()
        # Show the message box
        self.message_box.exec()

    def close_message_box(self):
        """Closes the waiting box message and restores the WaitCursor"""
        # Close the message box
        self.message_box.close()
        # Restore the cursor to its default state
        QApplication.instance().restoreOverrideCursor()
        # Stop the timer
        self.timer.stop()

    def handleCellClicked(self, row, column):
        # Check if the clicked cell is the last cell
        item = self.tableModels.item(row, column)
        action_text = item.text()
        # print(action_text)
        # Dictionary mapping selection action_text
        actions = {"Download": self.action_download, "Load": self.action_load}

        # Get the corresponding action based on item text
        action = actions.get(action_text)
        if action:
            action(row)

    def action_download(self, row):
        """
        Download the model files specified by the given row index.

        Args:
            row (int): The index of the row in the tableModels where the action was triggered.

        Returns:
            None
        """

        # Retrieve IDs
        item = self.models.tableModels.item(row, 0)
        self.model_id = item.text()
        sys_id = self.system_ID
        model_id = self.model_id
        # Construct the directory path with variables
        path_manager = mmbse_gui.PathManager()
        db_path = path_manager.get_path()
        id_path = f"{db_path}sys_{sys_id}/model_{model_id}"
        answer = QMessageBox.warning(
            self,
            "Warning",
            f'This action might overwrite local changes under the model in the database path "{id_path}".\n\n Would you like to proceed?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
        )
        if answer is QMessageBox.StandardButton.Yes:
            os.makedirs(id_path, exist_ok=True)
            # Store the current working directory
            original_path = os.getcwd()
            try:
                # Change the current working directory to id_path
                os.chdir(id_path)
                files = self.client.download_model_input_files(model_id)
                if not files:
                    QMessageBox.warning(
                        self,
                        "Empty Model",
                        f"No files to download for this Model ID {model_id}.",
                    )
                else:
                    # Downloaded - Give success
                    self.success_downlaod(model_id, files)
                    # print(files)
            finally:
                # Restore the original working directory
                os.chdir(original_path)

    def action_load(self, row):
        """
        Load a ROXIE model specified by the given row index.

        Args:
            row (int): The index of the row in the tableModels where the action was triggered.

        Returns:
            None
        """
        item = self.models.tableModels.item(row, 0)
        model_id = item.text()
        sys_id = self.system_ID
        self.load_roxie_model(sys_id, model_id)

    def load_roxie_model(self, sys_id, model_id: str):
        self.show_waiting_box()
        # # This commented-out section  is for Xroxie running in parallel
        # Create a thread to write to the named pipe
        # if roxie_filename is not None:
        #     write_thread = threading.Thread(target=self.write_to_pipe(roxie_filename))
        #     write_thread.start()
        #     self.close()
        # else:
        #     QMessageBox.warning(
        #         self,
        #         "ROXIE Datafile non-existent",
        #         f"The model ID {id} does not have a ROXIE datafile to be loaded.",
        #     )
        # Store the current working directory
        original_path = os.getcwd()
        path_manager = mmbse_gui.PathManager()
        db_path = path_manager.get_path()
        try:
            id_path = f"{db_path}sys_{sys_id}/model_{model_id}"
            # Create the directory if it doesn't exist
            if not os.path.exists(id_path):
                os.makedirs(id_path)

            # Change the current working directory
            os.chdir(id_path)
            self.client.download_model_input_files(model_id)
            roxie_filename = self.client.get_model_roxie_data_filename(model_id)
            # Use subprocess.Popen to run the command in the background
            process = subprocess.Popen(
                ["Xroxie", " --db", roxie_filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            print(
                f"'Xroxie {roxie_filename}' is now running in the background with PID {process.pid}"
            )
        except Exception:
            QMessageBox.warning(
                self,
                "ROXIE Datafile non-existent",
                f"The model ID {model_id} does not have a ROXIE datafile to be loaded. Please check the Database.",
            )
        finally:
            # Restore the original working directory
            os.chdir(original_path)

    def success_downlaod(self, model_id, files):
        """
        Appears if files have been downloaded successfully. Shows the downloaded files.

        Args:
            model_id (str): The ID of the model that was successfully downloaded.
            files (list): A list of files that were downloaded.

        Returns:
            None
        """
        self.success_box = QMessageBox()
        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icons/icon-success.png")
        icon_pixmap = QPixmap(icon_path)
        self.success_box.setIconPixmap(icon_pixmap)
        self.success_box.setText(
            f"Files of Model ID {model_id} were downloaded succesfully.\n\nThese are: \n{files}"
        )
        ok_button = self.success_box.addButton(QMessageBox.StandardButton.Ok)
        ok_button.setStyleSheet(GLOBAL_BUTTON_STYLE)
        self.success_box.setWindowTitle("Successful request")
        timer = QTimer()
        timer.timeout.connect(self.success_box.accept)
        timer.start(2000)
        self.success_box.show()

    def return_to_main_window(self):
        self.w = mmbse_gui.ROXIE_Gui(self.token)
        self.w.show()
        self.hide()

    def return_to_systems(self):
        self.w = systems_window.SystemsWindow(self.token)
        self.w.show()
        self.hide()

    def open_post_model(self):
        self.w = PostModel(self.token, self.system_ID)
        self.w.show()
        self.hide()


class TokenInvalidError(Exception):
    pass
