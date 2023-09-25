import csv
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem

def PopulateTableView(tableView, columnHeaders, data):
    # Create a model and set it for the table view
    model = QStandardItemModel()
    tableView.setModel(model)

    # Set column headers
    model.setHorizontalHeaderLabels(columnHeaders)

    # Populate the model with data
    for row in data:
        item_list = [QStandardItem(str(item)) for item in row]
        model.appendRow(item_list)

    tableView.resizeColumnsToContents()

def AddDataToTableView(tableView, newData):
    # Get the current model
    model = tableView.model()

    # Check if the model exists
    if model is not None:
        # Append the new data to the model
        item_list = [QStandardItem(str(item)) for item in newData]
        model.appendRow(item_list)
            
    tableView.resizeColumnsToContents()