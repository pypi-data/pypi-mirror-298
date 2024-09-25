# SPDX-FileCopyrightText: 2024 Konstantinos Diamantis <konstantinos.diamantis@cern.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re
from typing import Optional

from PyQt6 import uic
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import *
from requests.exceptions import RequestException

import mmbse_client.mmbse as mmbse
import roxie_3ml.py_files.mmbse_gui as mmbse_gui
from roxie_3ml.py_files.styles import *


class PushFileDB(QMainWindow):
    def __init__(
        self,
        token,
        file_path: Optional[str] = None,
        opt_sys_id: Optional[int] = None,
        opt_model_id: Optional[int] = None,
    ):
        super().__init__()
        ui_file = os.path.join(
            os.path.dirname(__file__), "./../ui_files/push_select_model.ui"
        )
        uic.loadUi(ui_file, self)
        self.token = token
        self.opt_sys_id = opt_sys_id
        self.opt_model_id = opt_model_id
        self.client = mmbse.MMBSE(self.token)

        if not self.client.is_authenticated():
            #     # def openLoginWindow(self):
            # self.close()
            # self.new_window = TokenLoginWindow(self)
            # self.new_window.move(self.pos())
            # self.new_window.show()
            raise TokenInvalidError("Token is invalid")

        self.systems = self.client.get_systems()
        self.combo_systems.activated.connect(
            self.on_combo_systems
        )  # Combobox is dropped down and Item has been selected
        self.combo_models.activated.connect(self.on_combo_models)
        self.setStyleSheet(GLOBAL_BUTTON_STYLE)
        self.textEditInput.adjustSize()
        for row, _ in enumerate(self.systems):
            self.combo_systems.addItem(
                str(self.systems[row]["id"]) + ", " + str(self.systems[row]["name"])
            )

        self.cols = ["id", "name", "description", "owner", "created_at"]
        self.model_cols = [
            "id",
            "type",
            "name",
            "description",
            "design_step",
            "inputs",
            "outputs",
            "created_at",
        ]

        self.droped_down_flag = False
        self.add_extra_file.clicked.connect(self.dropdown_output_files)
        self.toolButton_2.clicked.connect(self.dropdown_output_files)

        self.textEditOutput.hide()
        self.label_path_3.hide()
        self.combo_fileType_Out.hide()
        self.toolButton_2.hide()
        self.button_file_select_2.hide()
        self.label_path_3.hide()
        self.label_8.hide()
        self.remove_button_output.hide()

        self.tableSystems.insertRow(0)
        self.tableModels.insertRow(0)
        self.tableSystems.hide()
        self.tableModels.hide()
        self.label_empty_models.hide()
        self.label_empty_models.setStyleSheet("color: red;")
        self.button_push.clicked.connect(self.push_to_db)
        self.button_close.clicked.connect(self.close)
        self.button_back_main.clicked.connect(self.return_to_main_window)
        self.roxie_files_toolButton.clicked.connect(self.add_roxie_files_clicked)
        # self.label_path.setText(f'You selected the file(s):  ')
        # if file_path is not None:
        # self.textEditInput.addItem(f"{file_path}")
        self.label_blank.hide()
        self.label_provide_descr.hide()
        self.label_provide_descr2.hide()
        self.label_provide_descr3.hide()
        self.lineModelID.hide()
        self.lineSysID.hide()
        # self.label_file_type.hide()
        # Set font for the entire table
        self.user = self.client.get_user_details()
        font = QFont("MS Shell Dlg 2", 10)  # Specify the font family and size
        self.tableSystems.setFont(font)
        self.label_logged.setStyleSheet("color: green;")
        self.label_insert_user.setStyleSheet("color: green;")
        self.label_insert_user.setText((self.user["extra_data"]["preferred_username"]))
        self.label_insert_email.setText((self.user["extra_data"]["email"]))
        self.label_insert_cern_id.setText((self.user["extra_data"]["cern_person_id"]))
        self.add_extra_file.setToolTip("Add output file(s)")
        self.button_file_select.setToolTip("Add extra file")
        self.toolButton_2.setToolTip("Close output files")
        # icon_path = os.path.join(
        #     os.path.dirname(__file__), "../assets/icons/plus.svg"
        #     )
        # icon = QIcon(icon_path)
        # self.button_file_select.setIcon(icon)
        self.remove_button_input.setEnabled(False)
        self.remove_button_output.setEnabled(False)

        self.textEditInput.itemClicked.connect(self.enable_remove_input_button)
        self.textEditOutput.itemClicked.connect(self.enable_remove_output_button)
        self.button_file_select.clicked.connect(self.input_file_select)
        self.remove_button_input.clicked.connect(self.remove_item_input)
        self.remove_button_output.clicked.connect(self.remove_item_output)
        self.button_file_select_2.clicked.connect(self.output_file_select)
        self.roxie_files_toolButton.setEnabled(False)
        self.system_sel_flag = 0
        self.system_mod_flag = 0
        self.filetype_flag = 0
        self.combo_fileType_Out.setEnabled(False)
        self.tableModels.setStyleSheet(GLOBAL_TABLE_STYLE)
        self.tableSystems.setStyleSheet(GLOBAL_TABLE_STYLE)

        if self.opt_sys_id is not None and self.opt_model_id is not None:
            self.combo_systems.setCurrentText(str(self.opt_sys_id))
            self.combo_models.addItem(str(self.opt_model_id))
            self.combo_models.setCurrentText(str(self.opt_model_id))
            self.combo_systems.setEnabled(False)
            self.combo_models.setEnabled(False)
            self.path_populate_system_table(self.opt_sys_id)
            self.path_populate_model_table(self.opt_model_id)
            self.lineModelID.setText(f"{self.opt_model_id}")
            self.lineSysID.setText(f"{self.opt_sys_id}")

    def enable_remove_input_button(self):
        # Enable the remove button when an item is clicked
        self.remove_button_input.setEnabled(True)

    def enable_remove_output_button(self):
        # Enable the remove button when an item is clicked
        self.remove_button_output.setEnabled(True)

    def remove_item_output(self):
        # Remove the currently selected item from the list widget
        selected_item = self.textEditOutput.currentItem()
        if selected_item:
            self.textEditOutput.takeItem(self.textEditOutput.row(selected_item))

        # Disable the remove button if no items are selected or if the list is empty
        if self.textEditOutput.count() == 0:
            self.remove_button_output.setEnabled(False)
        else:
            self.textEditOutput.clearSelection()
            self.remove_button_output.setEnabled(False)

    def remove_item_input(self):
        # Remove the currently selected item from the list widget
        selected_item = self.textEditInput.currentItem()
        if selected_item:
            self.textEditInput.takeItem(self.textEditInput.row(selected_item))

        # Disable the remove button if no items are selected or if the list is empty
        if self.textEditInput.count() == 0:
            self.remove_button_input.setEnabled(False)
        else:
            self.textEditInput.clearSelection()
            self.remove_button_input.setEnabled(False)

        # Appear the roxie files button if needed
        self.appear_roxie_files()

    def input_file_select(self):
        """Select Input files and display them in textEditInput"""
        self.input_file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select files",
            "",
            "ROXIE datafiles (*.data);;Iron files (*.iron);;BH files (*.bh);;Cable datafiles (*.cadata);;PDF files (*.pdf);;Text files (*.txt);;All Files (*)",
        )

        if self.input_file_paths:
            for file in self.input_file_paths:
                if not self.item_input_exists(file):
                    self.textEditInput.addItem(f"{file}")
                else:
                    QMessageBox.critical(
                        self, "Warning", f"File '{file}' has already been added."
                    )
        self.appear_roxie_files()

    def item_input_exists(self, file_path):
        # Check if the item already exists in the list widget
        for index in range(self.textEditInput.count()):
            if self.textEditInput.item(index).text() == file_path:
                return True
        return False

    def item_output_exists(self, file_path):
        # Check if the item already exists in the list widget
        for index in range(self.textEditOutput.count()):
            if self.textEditOutput.item(index).text() == file_path:
                return True
        return False

    def output_file_select(self):
        """Select Output files and display them in textEditOutput"""
        self.output_file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select files",
            "",
            "PDF files (*.pdf);;Text files (*.txt);;All Files (*)",
        )

        if self.output_file_paths:
            for file in self.output_file_paths:
                if not self.item_output_exists(file):
                    self.textEditOutput.addItem(f"{file}")
                else:
                    QMessageBox.critical(
                        self, "Warning", f"File '{file}' has already been added."
                    )

    def dropdown_output_files(self):
        """Clicked when either of the 2 buttons are clikced. Reverses the icons and handles the comboBoxes"""

        if not self.droped_down_flag:
            self.textEditOutput.show()
            self.label_path_3.show()
            self.combo_fileType_Out.show()
            self.toolButton_2.show()
            self.remove_button_output.show()
            self.button_file_select_2.show()
            self.label_path_3.show()
            self.label_8.show()
            icon_path = os.path.join(
                os.path.dirname(__file__), "../assets/icons/chevrons-up.svg"
            )
            icon = QIcon(icon_path)
            self.add_extra_file.setIcon(icon)
            self.combo_fileType.setEnabled(False)
            self.combo_fileType.setCurrentText("Input")
            self.droped_down_flag = True
        else:
            self.textEditOutput.hide()
            self.label_path_3.hide()
            self.remove_button_output.hide()
            self.combo_fileType_Out.hide()
            self.toolButton_2.hide()
            self.button_file_select_2.hide()
            self.label_path_3.hide()
            self.label_8.hide()
            icon_path = os.path.join(
                os.path.dirname(__file__), "../assets/icons/chevrons-down.svg"
            )
            icon = QIcon(icon_path)
            self.add_extra_file.setIcon(icon)
            self.combo_fileType.setEnabled(True)
            self.droped_down_flag = False

    def path_populate_system_table(self, sys_id):
        """Populate the system table with the information of the specified system ID."
        "This method takes a system ID as input, finds the corresponding row in the systems data, and populates the table with the system information.
        It sets the 'system_sel_flag' to 1 to indicate that the system has been selected.
        """
        self.row_num = self.find_row_by_id(str(sys_id))
        # Populate the table accordingly
        for column, _ in enumerate(self.cols):
            self.tableSystems.setItem(
                0,
                column,
                QTableWidgetItem(str(self.systems[self.row_num][self.cols[column]])),
            )

        self.tableSystems.show()
        self.style_system_table()
        self.system_sel_flag = 1

    def path_populate_model_table(self, model_id):
        self.models = self.client.get_system_models(self.opt_sys_id)
        self.row_num = self.find_row_by_model_id(str(model_id))
        # Populate the table accordingly
        for column, _ in enumerate(self.model_cols):
            self.tableModels.setItem(
                0,
                column,
                QTableWidgetItem(
                    str(self.models[self.row_num][self.model_cols[column]])
                ),
            )

        self.tableModels.show()
        self.style_model_table()
        self.system_mod_flag = 1

    def style_system_table(self):
        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icons/monitor.svg")
        icon_pixmap = QPixmap(icon_path)
        self.tableSystems.setItem(
            0,
            len(self.cols),
            QTableWidgetItem().setIcon(QIcon(icon_pixmap)),
        )

        self.tableSystems.setItem(0, len(self.cols), QTableWidgetItem("View Report"))
        self.doHeadersBold(self.tableSystems)
        self.doLastColumnFont(self.tableSystems)
        self.clean_dates(self.tableSystems, 4)
        self.doAlignColumns(self.tableSystems, [0, 4, 5])
        self.doColumnWidthSystems()
        self.tableSystems.setColumnWidth(3, 200)
        # self.tableSystems.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)

    def style_model_table(self):
        font = QFont("MS Shell Dlg 2", 10)  # Specify the font family and size
        self.tableModels.setFont(font)
        self.label_provide_descr.show()
        self.label_provide_descr2.show()
        self.label_provide_descr3.show()
        self.label_provide_descr.setStyleSheet("color: green;")
        self.label_provide_descr2.setStyleSheet("color: green;")
        self.label_provide_descr3.setStyleSheet("color: green;")
        self.lineModelID.show()
        self.lineSysID.show()
        self.doHeadersBold(self.tableModels)
        self.clean_dates(self.tableModels, 7)
        self.doColumnWidthModel()
        self.doColumnsFont()
        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icons/failure.svg")
        self.tableModels.setItem(
            0,
            len(self.model_cols),
            QTableWidgetItem().setIcon(QIcon(icon_path)),
        )
        self.tableModels.setItem(
            0, len(self.model_cols), QTableWidgetItem("View Report")
        )
        self.doAlignColumns(self.tableModels, [0, 1, 4, 5, 6, 7, 8])
        # self.tableModels.setItem(0, len(self.model_cols), QTableWidgetItem("View Report"))
        self.doLastColumnFont(self.tableModels)
        # self.label_provide_descr.setText(f"You are going to publish your changes
        # of System {self.sys_ID} and Model {selected_model}. Please provi

    def push_to_db(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.hideLabel)
        self.timer.start(2500)
        print(self.texts_empty())

        if (self.system_sel_flag) and (self.system_mod_flag):
            if self.texts_empty():
                self.label_blank.setText("Please select the model file(s).")
                self.label_blank.setStyleSheet("color: red;")
                self.label_blank.show()
            elif not self.texts_empty() and self.combo_fileType.currentText() == "":
                self.label_blank.setText("Please specify the type of file(s).")
                self.label_blank.setStyleSheet("color: red;")
                self.label_blank.show()
            elif (
                not self.texts_empty()
                and self.combo_fileType.currentText() == "Output"
                and self.droped_down_flag
            ):
                self.label_blank.setText("Please split the files to Input and Output.")
                self.label_blank.setStyleSheet("color: red;")
                self.label_blank.show()
            elif self.line_comment.toPlainText() == "":
                self.label_blank.setText("Comment cannot be blank.")
                self.label_blank.setStyleSheet("color: red;")
                self.label_blank.show()
            elif len(self.line_comment.toPlainText().strip()) < 9:
                self.label_blank.setText("Please provide a more descriptive comment.")
                self.label_blank.setStyleSheet("color: red;")
                self.label_blank.show()
            else:
                # print("Pushing to Database")
                self.label_blank.setText("Pushing files to Database...")
                self.label_blank.setStyleSheet("color: green;")
                self.label_blank.show()
                for file_path in self.input_file_paths:
                    try:
                        self.client.upload_model_file(
                            "input", str(self.opt_model_id), "", file_path
                        )
                        failed = False
                    except Exception:
                        self.fail_uplaod(self.opt_model_id)
                        failed = True
                        break

                if not failed:
                    self.success_uplaod(self.opt_model_id)

                if self.droped_down_flag:
                    for file_path in self.output_file_paths:
                        try:
                            self.client.upload_model_file(
                                "output", str(self.opt_model_id), "", file_path
                            )
                            failed = False
                        except Exception:
                            self.fail_uplaod(self.opt_model_id)
                            failed = True
                            break

                    if not failed:
                        self.success_uplaod(self.opt_model_id)

        elif (self.system_sel_flag) and (not self.system_mod_flag):
            self.label_blank.setText("Please select the model of the selected system.")
            self.label_blank.setStyleSheet("color: red;")
            self.label_blank.show()
        elif (not self.system_sel_flag) and (not self.system_mod_flag):
            self.label_blank.setText("Please select the system and its model.")
            self.label_blank.setStyleSheet("color: red;")
            self.label_blank.show()

    def success_uplaod(self, model_id):
        """
        Appears if files have been uploaded successfully.

        Args:
            model_id (str): The ID of the model that was successfully uploaded.

        Returns:
            None
        """
        self.success_box = QMessageBox()
        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icons/icon-success.png")
        icon_pixmap = QPixmap(icon_path)
        self.success_box.setIconPixmap(icon_pixmap)
        self.success_box.setText(
            f"Files of Model ID {model_id} have been pushed to remote database successfully. \n\n"
        )
        ok_button = self.success_box.addButton(QMessageBox.StandardButton.Ok)
        ok_button.setStyleSheet(GLOBAL_BUTTON_STYLE)
        self.success_box.setWindowTitle("Successful request")
        self.success_box.show()
        # self.success_box.finished.connect(self.return_to_main_window())

    def fail_uplaod(self, model_id):
        """
        Appears if files have not been uploaded successfully.

        Args:
            model_id (str): The ID of the model that was failed to upload.

        Returns:
            None
        """
        self.fail_box = QMessageBox()
        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icons/failure.svg")
        icon_pixmap = QPixmap(icon_path)
        self.fail_box.setIconPixmap(icon_pixmap)
        self.fail_box.setText(
            f"Files of Model ID {model_id} have failed to upload to remote database. "
            f"Please check the remote database and ensure the models are synced properly."
        )
        ok_button = self.fail_box.addButton(QMessageBox.StandardButton.Ok)
        ok_button.setStyleSheet(GLOBAL_BUTTON_STYLE)
        self.fail_box.setWindowTitle("Failed request")
        self.fail_box.show()

    def appear_roxie_files(self):
        """
        Enables or disables the roxie_files_toolButton based on the number of data files in the input.

        If there is exactly one data file, the button is enabled. Otherwise, it is disabled.

        Parameters:
            None

        Returns:
            None
        """

        data_files = [
            self.textEditInput.item(index).text()
            for index in range(self.textEditInput.count())
            if self.textEditInput.item(index).text().endswith(".data")
        ]
        if len(data_files) == 1:
            self.roxie_files_toolButton.setEnabled(True)
        else:
            self.roxie_files_toolButton.setEnabled(False)

    def add_roxie_files_clicked(self):
        """
        Adds ROXIE files to the input and output lists when the corresponding button is clicked.

        This function first searches for related ROXIE files and then adds them to the input and output lists.
        It checks for the existence of iron, cable, and bh files, as well as pdf, xml, and output files.
        If any of these files exist, they are added to the corresponding lists.

        Parameters:
            None

        Returns:
            None
        """
        data_files = [
            self.textEditInput.item(index).text()
            for index in range(self.textEditInput.count())
            if self.textEditInput.item(index).text().endswith(".data")
        ]

        message_box = QMessageBox()
        message_box.setWindowTitle("ROXIE files")
        message_box.setText("Please wait while searching for related ROXIE files...")
        message_box.setStandardButtons(QMessageBox.StandardButton.Cancel)
        QTimer.singleShot(2500, message_box.close)
        message_box.exec()

        iron_file = self.extract_file_paths(data_files[0]).get("iron")
        cable_file = self.extract_file_paths(data_files[0]).get("cadata")
        bh_file = self.extract_file_paths(data_files[0]).get("bhdata")

        # Add all the relevant input/output files
        if iron_file is not None and not self.item_input_exists(iron_file):
            self.textEditInput.addItem(f"{iron_file}")

        if cable_file is not None and not self.item_input_exists(cable_file):
            self.textEditInput.addItem(f"{cable_file}")

        if bh_file is not None and not self.item_input_exists(bh_file):
            self.textEditInput.addItem(f"{bh_file}")

        # Extract the file name
        # file_name = os.path.basename(data_files[0])
        file_base = os.path.splitext(data_files[0])[0]
        # Remove the '.data' extension
        # file_corename = os.path.splitext(file_name)[0]

        # Output is pdf+post.xml+output
        pdf_file = file_base + ".pdf"
        xml_file = file_base + ".post.xml"
        output_file = file_base + ".output"

        # Check if the .pdf file pdf_file
        if os.path.exists(pdf_file) and not self.item_output_exists(pdf_file):
            self.textEditOutput.addItem(f"{pdf_file}")

        # Check if the .xml file exists
        if os.path.exists(xml_file) and not self.item_output_exists(xml_file):
            self.textEditOutput.addItem(f"{xml_file}")

        # Check if the output file exists
        if os.path.exists(output_file) and not self.item_output_exists(output_file):
            self.textEditOutput.addItem(f"{output_file}")

        # If any of the above files exist, call the dropdown_output_files method
        if (
            os.path.exists(pdf_file)
            or os.path.exists(xml_file)
            or os.path.exists(output_file)
        ):
            self.droped_down_flag = False  # Always drop it down
            self.dropdown_output_files()

    def texts_empty(self):
        """
        Check if the lists are empty.

        This function retrieves the text content from two QlistW widgets,
        'textEditInput' and 'textEditOutput', and checks if they are empty.
        If the 'droped_down_flag' is True, it checks both lists for
        content. If 'droped_down_flag' is False, it only checks 'textEditInput'.

        Returns:
            bool: True if either of the lists is empty, False otherwise.
        """

        def is_list_empty(list_widget):
            return list_widget.count() == 0

        if self.droped_down_flag:
            return is_list_empty(self.textEditInput) or is_list_empty(
                self.textEditOutput
            )
        else:
            return is_list_empty(self.textEditInput)

    def extract_file_paths(self, data_file):
        """
        Extracts .iron, .cadata, and .bhdata file paths from the first 5 lines of a .data file.

        Parameters:
        data_file (str): The path to the .data file.

        Returns:
        dict: A dictionary with the file paths.
        """
        # Initialize the file paths
        paths = {"iron": None, "cadata": None, "bhdata": None}

        # Regular expressions to match the file paths
        patterns = {
            "iron": r"\/.*\.iron",
            "cadata": r"\/.*\.cadata",
            "bhdata": r"\/.*\.bhdata",
        }

        try:
            with open(data_file, "r") as file:
                # Read only the first 5 lines
                for i, line in enumerate(file):
                    if i >= 5:
                        break
                    for key, pattern in patterns.items():
                        match = re.search(pattern, line)
                        if match:
                            paths[key] = match.group()

        except FileNotFoundError:
            print(f"File {data_file} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        return paths

    def hideLabel(self):
        """
        It is triggered when Push files is pressed but incomplete/wrong
        information is catched and displayed. Hides the information box
        after the timer finishes.
        """
        self.label_blank.hide()

    def extract_id(self, text):
        """
        Extracts the id from the given text.

        The text is expected to have the format "<id>, <name>", where <id> is an integer
        and <name> is a string.

        Args:
            text (str): The input text containing the id and name.

        Returns:
            str: The extracted id.
        """
        # Split the text by space and return the first part
        return text.split(", ")[0]

    def on_combo_systems(self, index: Optional[int] = 0):
        if index > 0:
            combo_text = self.combo_systems.itemText(index)
            selected_sys = self.extract_id(combo_text)
            self.sys_ID = selected_sys
            self.tableSystems.show()
            # self.tableSystems.setStyleSheet(GLOBAL_TABLE_STYLE)
            # print("Selected item:", selected_sys)
            self.row_num = self.find_row_by_id(str(selected_sys))
            # print(f"Selected system: {self.row_num}")
            self.models = self.client.get_system_models(selected_sys)
            # print("MODELS")
            # print(self.models)

            # Clear and populate the combobox for models accordingly
            self.combo_models.clear()
            self.combo_models.addItem("")
            # Populate the box accordingly
            if self.models:
                self.label_empty_models.hide()
                for row, _ in enumerate(self.models):
                    self.combo_models.addItem(
                        str(self.models[row]["id"])
                        + ", "
                        + str(self.models[row]["name"])
                    )
            else:
                self.label_empty_models.show()

            # Populate the table accordingly
            for column, _ in enumerate(self.cols):
                self.tableSystems.setItem(
                    0,
                    column,
                    QTableWidgetItem(
                        str(self.systems[self.row_num][self.cols[column]])
                    ),
                )

            self.tableSystems.setItem(
                0, len(self.cols), QTableWidgetItem("View Report")
            )

            self.style_system_table()
            self.system_sel_flag = 1
            self.tableModels.hide()
            self.label_provide_descr.hide()
            self.label_provide_descr2.hide()
            self.label_provide_descr3.hide()
            self.lineModelID.hide()
            self.lineSysID.hide()
        else:
            self.tableSystems.hide()
            self.tableModels.hide()
            self.combo_models.clear()
            self.label_empty_models.hide()
            self.system_sel_flag = 0
            self.label_provide_descr.hide()
            self.label_provide_descr2.hide()
            self.label_provide_descr3.hide()
            self.lineModelID.hide()
            self.lineSysID.hide()
        # if index is None:
        # print("index is None")

    def doAddViewButtons(self):
        # View Models
        for row, _ in enumerate(self.systems):
            self.tableModels.insertRow(row)
            for column, _ in enumerate(self.cols):
                self.tableModels.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(self.systems[row][self.cols[column]])),
                )
            # item_icon = QTableWidgetItem("View Model")
            # item_icon.setIcon(QIcon("/workspaces/roxie/mmbse-client/mmbse_gui/icons/monitor.svg"))
            self.tableModels.setItem(
                row, len(self.cols), QTableWidgetItem("View Models")
            )
            self.tableModels.setItem(
                row, len(self.cols) + 1, QTableWidgetItem("View Report")
            )

    def doColumnWidthSystems(self):
        self.tableSystems.resizeColumnToContents(3)
        self.tableSystems.setColumnWidth(1, 150)
        self.tableSystems.setColumnWidth(0, 80)
        self.tableSystems.setColumnWidth(2, 240)

    def on_combo_models(self, index):
        # Populate them in accordance to system id
        # print(index)
        # print(index)

        if index > 0:
            combo_text = self.combo_models.itemText(index)
            selected_model = self.extract_id(combo_text)
            self.opt_model_id = selected_model
            self.tableSystems.show()
            # print("Selected model item:", selected_model)
            self.row_num = self.find_row_by_model_id(str(selected_model))
            # self.tableModels.clear()
            for column, _ in enumerate(self.model_cols):
                self.tableModels.setItem(
                    0,
                    column,
                    QTableWidgetItem(
                        str(self.models[self.row_num][self.model_cols[column]])
                    ),
                )

            self.tableModels.show()
            self.lineModelID.setText(f"{selected_model}")
            self.lineSysID.setText(f"{self.sys_ID}")
            self.system_mod_flag = 1
            self.style_model_table()

        else:
            self.tableModels.hide()
            self.label_provide_descr.hide()
            self.label_provide_descr2.hide()
            self.label_provide_descr3.hide()
            self.lineModelID.hide()
            self.lineSysID.hide()
            self.system_mod_flag = 0

    def doAlignColumns(self, table, columns_to_align):
        # columns_to_align = [0, 1, 4, 5, 6, 7, 8]  # Change this to the desired column indices
        for row, _ in enumerate(self.systems):
            for column in columns_to_align:
                item = table.item(row, column)
                if item is not None:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def doColumnsFont(self):
        for row in range(self.tableModels.rowCount()):
            item = self.tableModels.item(
                row, self.tableModels.columnCount() - 1
            )  # Last column
            self.applyFormatting(item)
            # item = self.tableModels.item(row, self.tableModels.columnCount() - 2)  #2nd to last column
            # self.applyFormatting(item)

    def doColumnWidthModel(self):
        self.tableModels.resizeColumnToContents(3)
        self.tableModels.setColumnWidth(0, 80)
        self.tableModels.setColumnWidth(5, 90)
        self.tableModels.setColumnWidth(6, 90)
        self.tableModels.setColumnWidth(2, 150)
        self.tableModels.setColumnWidth(3, 240)

    def find_row_by_id(self, id_to_find):
        cols = ["id"]
        for row, _ in enumerate(self.systems):
            for column, _ in enumerate(cols):
                if str(self.systems[row][self.cols[column]]) == id_to_find:
                    return row

        QMessageBox.critical(
            self,
            "Warning",
            f"Model with ID '{id_to_find}' not found. Make sure that the model is available in the Database or has not been deleted.",
        )
        return -1
        #  TODO as below

    def find_row_by_model_id(self, id_to_find):
        cols = ["id"]
        for row, _ in enumerate(self.models):
            for column, _ in enumerate(cols):
                if str(self.models[row][self.cols[column]]) == id_to_find:
                    return row

        QMessageBox.critical(
            self,
            "Warning",
            f"Model with ID '{id_to_find}' not found.  Make sure that the model is available in the Database or has not been deleted.",
        )
        self.system_mod_flag = 0
        # TODO the flag should take place
        # self.hide()
        # TODO it does not hide
        return -1

    def applyFormatting(self, item):
        if item:
            font = QFont("MS Shell Dlg 2", 10)
            font.setUnderline(True)
            cern_blue = QColor(7, 68, 250)  # RGB values for CERN blue
            item.setForeground(cern_blue)
            item.setFont(font)

    def doLastColumnFont(self, table):
        for row in range(table.rowCount()):
            item = table.item(row, table.columnCount() - 1)  # Last column
            self.applyFormatting(item)
            # item = self.tableSystems.item(row, self.tableSystems.columnCount() - 2)  #2nd to last column
            # self.applyFormatting(item)

    def clean_dates(self, table, date_col):
        for row in range(table.rowCount()):
            date_item = table.item(row, date_col)
            original_text = date_item.text()
            cleaned_text = (
                original_text.split("T")[0] if "T" in original_text else original_text
            )
            date_item.setText(cleaned_text)

    def doHeadersBold(self, table):
        font = QFont()
        font.setBold(True)
        for col in range(table.columnCount()):
            item = table.horizontalHeaderItem(col)
            if item:
                item.setFont(font)

        for col in range(table.columnCount()):
            item = table.horizontalHeaderItem(col)
            if item:
                item.setFont(font)

    def return_to_main_window(self):
        self.w = mmbse_gui.ROXIE_Gui(self.token)
        self.w.show()
        self.hide()


class TokenInvalidError(Exception):
    pass
