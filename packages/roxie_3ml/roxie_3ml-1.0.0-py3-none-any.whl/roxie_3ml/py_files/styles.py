# SPDX-FileCopyrightText: 2024 Konstantinos Diamantis <konstantinos.diamantis@cern.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Define the global stylesheet


GLOBAL_LINE_STYLESHEET = """
            QLineEdit {
                color: #666666;
                font-size: 12px;
                border: 2px solid #000000; /* Set outline color to black */
                border-radius: 5px; /* Optional: Add border radius for rounded corners */
            }
 """


GLOBAL_LABEL_STYLESHEET = """
            QLabel {
                color: #666666;
                font-size: 12px;
                }
            """


GLOBAL_LINE_STYLESHEET = """
            QLineEdit {
                border: 2px solid #666666;
                border-radius: 3px;
                color: #444444;
                padding: 1px 3px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border-color: #6495ED;
            }
        """

GLOBAL_TABLE_STYLE = """
    /* QTableWidget Styles */
    QTableWidget {
        background-color: transparent;
        border: 1px solid #666666;
        color: black;
        selection-background-color: #CCCCCC;
        selection-color: black;
        border-radius: 5px;
        font-size: 12px;
    }

    QTableWidget::item {
        padding: 5px;
    }

    QHeaderView::section {
        background-color: #CCCCCC;
        border: none;
        font-size: 12px;
        padding: 3px;
    }
"""


GLOBAL_BUTTON_STYLE = """
    /* QPushButton Styles */
    QPushButton {
        background-color: #CCCCCC;
        border: none;
        padding: 1px 3px;
        text-align: center;
        text-decoration: none;
        font-size: 14px;
        border-radius: 3px;
        border: 2px solid #6495ED;
        min-height: 25px;
    }

    QPushButton:hover {
        background-color:#666666;
        color: white;
    }

    QPushButton:pressed {
        background-color: #6495ED;
        border: none;
        color: white;
        padding: 1px 3px;
        text-align: center;
        text-decoration: none;
        font-size: 14px;
        margin: 1px 2px;
        border-radius: 3px;
        border: 2px solid #666666;
        min-height: 25px;
    }
"""
