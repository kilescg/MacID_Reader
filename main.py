from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView
from ui import Ui_MainWindow
import jlink
import sys
import json
from utils import *
import log 

header = ['macID', 'deviceType', 'deviceName', 'Location', 'Controller Type']
json_file = open("configuration.json")
combo_box_json = json.load(json_file)

def setTableHeader(ui):
    file_path = "database/employee_file.csv"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        log.ShowTableFromCSV(ui.devicesForPrintTableView)
    else:
        PopulateTableView(ui.devicesForPrintTableView, header, [])
    PopulateTableView(ui.devicesDBTableView, header, [])
    
def ComboBoxInitialize(ui):
    device_type = combo_box_json["device_type"]
    for option in device_type:
        ui.deviceTypeComboBox.addItem(option)
    location = combo_box_json["location"]
    for option in location:
        ui.locationComboBox.addItem(option)
    controller_type = combo_box_json["controller_type"]
    for option in controller_type:
        ui.controllerTypeComboBox.addItem(option)

def ConnectUiWithFunction(ui):
    '''
    Button
    '''
    ui.powerOnButton.clicked.connect(jlink.JLink_Power_On) # Done
    ui.readMacButton.clicked.connect(lambda : ReadMacButton_Event(ui)) #Done
    ui.addDeviceButton.clicked.connect(lambda : AddDevice_Event(ui))
    ui.printNowButton.clicked.connect(lambda : PrintNow_Event(ui))
    ui.clearListButton.clicked.connect(lambda : ClearList_Event(ui))
    '''
    Combo Box
    '''
    ui.deviceTypeComboBox.currentIndexChanged.connect(lambda index, ui=ui: (DeviceNameUpdate_Event(ui)))

def ReadMacButton_Event(ui):
    mac_id = jlink.MAC_ID_Check()
    if mac_id != "":
        ui.macStatuslabel.setText("Read Mac Status : <span style=\"color:green\">Success</span></p>")
    else:
        ui.macStatuslabel.setText("Read Mac Status : <span style=\"color:red\">Fail</span></p>")
    ui.macIDShowLabel.setText(mac_id)

def AddDevice_Event(ui):
    # getting user setting
    mac_id = ui.macIDShowLabel.text()
    if mac_id == "":
        return
    device_type = ui.deviceTypeComboBox.currentText()
    device_name = ui.deviceNameComboBox.currentText()
    location = ui.locationComboBox.currentText()
    controller_type = ui.controllerTypeComboBox.currentText()
    device_type_index = combo_box_json["device_name_to_index"][device_name]
    mac_id = device_type_index + "_" + mac_id
    is_mac_id_duplicated = log.IsStringInCsv(mac_id, "macID")

    # AddDataToTableView(ui.devicesForPrintTableView, [mac_id, device_type, device_name, location, controller_type])
    if not is_mac_id_duplicated:
        log.WriteCSV(mac_id, device_type, device_name, location, controller_type)
        log.ShowTableFromCSV(ui.devicesForPrintTableView)

        log.CheckIfReachMaxLabel(ui, 4)

def ClearList_Event(ui):
    log.ResetCSV()
    PopulateTableView(ui.devicesForPrintTableView, header, [])
    
def PrintNow_Event(ui):
    PrintLabel()
    ClearList_Event(ui)

def DeviceNameUpdate_Event(ui):
    ui.deviceNameComboBox.clear()
    device_type = ui.deviceTypeComboBox.currentText()
    device_names = combo_box_json["device_type_to_device_name"][device_type]
    for option in device_names:
        ui.deviceNameComboBox.addItem(option)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ConnectUiWithFunction(ui)
    ComboBoxInitialize(ui)
    setTableHeader(ui)
    MainWindow.show()
    sys.exit(app.exec_())