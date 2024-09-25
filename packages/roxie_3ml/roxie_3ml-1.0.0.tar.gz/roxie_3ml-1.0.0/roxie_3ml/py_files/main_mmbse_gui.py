# SPDX-FileCopyrightText: 2024 Konstantinos Diamantis <konstantinos.diamantis@cern.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import os

from PyQt6.QtWidgets import QApplication, QMessageBox

from roxie_3ml.py_files.mmbse_gui import ROXIE_Gui
from roxie_3ml.py_files.push_files_db_window import PushFileDB
from roxie_3ml.py_files.styles import *
from roxie_3ml.py_files.system_models_window import (
    SystemModelsWindow,
    TokenInvalidError,
)
from roxie_3ml.py_files.token_window import TokenLoginWindow, TokenManager


def main():
    """
    Run the 3ML - Magnet Model Management Layer application.

    This function initializes the application, loads the token from the Token Manager,
    and based on the provided mode argument, it either launches the default application,
    pushes model files from Xroxie, or loads a ROXIE model from Xroxie.

    Parameters:
        None

    Returns:
        None
    """

    path = os.getcwd()
    app = QApplication([])

    # Token Manager
    token_manager = TokenManager()
    token = token_manager.load_token()

    #  0 for default app, 1 for push, 2 for pull
    parser = argparse.ArgumentParser(
        description="3ML - Magnet Model Management Layer application"
    )
    parser.add_argument(
        "mode",
        type=int,
        nargs="?",
        default=0,
        choices=[0, 1, 2],
        help="0 for default app, 1 for push model files from Xroxie, 2 for Loading ROXIE model from Xroxie",
    )
    args = parser.parse_args()

    run = args.mode

    if is_roxiedb_path(path) and run == 1:
        sys_id, model_id = extract_ids_from_path(path)
        try:
            window = PushFileDB(token, "", sys_id, model_id)
            window.show()
        except Exception:
            QMessageBox.warning(
                None,
                "Invalid or Missing Token",
                "You need to login first before you push/pull models to the Database.",
            )
            window = ROXIE_Gui("")
            new_window = TokenLoginWindow(window)
            window.show()
            new_window.show()
    elif is_roxiedb_path(path) and run == 2:
        sys_id, model_id = extract_ids_from_path(path)
        try:
            system_models_window = SystemModelsWindow(sys_id, token)
            system_models_window.hide()
            system_models_window.load_roxie_model(model_id)
            return
        except Exception:
            QMessageBox.warning(
                None,
                "Invalid/Missing Token or Outdated Database",
                "You need to login first before you push/pull models to the Database. \
                 Make sure that the models exist in the remote database.",
            )
            window = ROXIE_Gui("")
            new_window = TokenLoginWindow(window)
            window.show()
            new_window.show()
    elif token:
        roxie_gui = ROXIE_Gui(token)  # noqa: F841
    else:
        roxie_gui = ROXIE_Gui("")  # noqa: F841
    app.exec()


"""
Check if the provided path corresponds to a ROXIE database path.

Parameters:
    path (str): A string representing the path to be checked.

Returns:
    bool: True if the path matches the ROXIE database path pattern, False otherwise.
"""


def is_roxiedb_path(path):
    # Split the path into components
    components = path.split("/")

    # Check if there are at least three components
    if len(components) < 3:
        return False

    # Get the last three components
    last_two = components[-2:]

    # Check if the last three components match the pattern
    if (
        len(last_two) == 2
        and last_two[0].startswith("sys_")
        and last_two[1].startswith("model_")
        and last_two[1][6:].isdigit()  # Part after "model_"
        and last_two[0][4:].isdigit()  # Part after "sys_"
        and len(last_two[0][4:]) <= 3  # 3 digits at most
        and len(last_two[1][6:]) <= 3  # 3 digits at most
    ):
        return True
    else:
        return False


"""
Extracts the system and model IDs from the provided path.

Parameters:
    path (str): A string representing the path containing the system and model IDs.

Returns:
    tuple: A tuple containing the extracted system ID and model ID.
"""


def extract_ids_from_path(path):
    # Split the path by "/"
    parts = path.split("/")

    # Extract ids from the directory name
    _, var1 = parts[-2].split("_")
    _, var2 = parts[-1].split("_")

    return var1, var2


if __name__ == "__main__":
    main()
