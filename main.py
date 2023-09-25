from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView
from ui import Ui_MainWindow
import jlink
import sys
import json
from utils import *
import log 
import threading

print_list = []

def thread_callback(ui):
        result = jlink.JLink_Program_Flash(os.path.join("hex_files", ui.hexFileComboBox.currentText()))
        if result:
            ui.flashStatusLabel.setText("Flash Status : <span style=\"color:green\">Success</span></p>")
        else:
            ui.flashStatusLabel.setText("Flash Status : <span style=\"color:red\">Fail</span></p>")

header = ['macID', 'deviceType', 'deviceName', 'Location', 'Controller Type']
json_file = open("configuration.json")
combo_box_json = json.load(json_file)

def setTableHeader(ui):
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
    HexFileComboBoxClick_Event(ui)

def ConnectUiWithFunction(ui):
    '''
    Button
    '''
    ui.powerOnButton.clicked.connect(jlink.JLink_Power_On) # Done
    ui.readMacButton.clicked.connect(lambda : ReadMacButton_Event(ui)) #Done
    ui.addDeviceButton.clicked.connect(lambda : AddDevice_Event(ui))
    ui.printNowButton.clicked.connect(lambda : PrintNow_Event(ui))
    ui.clearListButton.clicked.connect(lambda : ClearList_Event(ui))
    ui.flashButton.clicked.connect(lambda : Flash_Event(ui))
    '''
    Combo Box
    '''
    ui.deviceTypeComboBox.currentIndexChanged.connect(lambda index, ui=ui: (DeviceNameUpdate_Event(ui)))
    ui.hexFileComboBox.activated.connect(lambda index, ui=ui: (HexFileComboBoxClick_Event(ui)))

def ReadMacButton_Event(ui):
    mac_id = jlink.MAC_ID_Check()
    if mac_id != "":
        ui.macStatuslabel.setText("Read Mac Status : <span style=\"color:green\">Success</span></p>")
    else:
        ui.macStatuslabel.setText("Read Mac Status : <span style=\"color:red\">Fail</span></p>")
    ui.macIDShowLabel.setText(mac_id)

def HexFileComboBoxClick_Event(ui):
    hex_files_folder = "hex_files"
        
    # Clear the current items in the combobox
    currentText = ui.hexFileComboBox.currentText()
    ui.hexFileComboBox.clear()

    # Check if the folder exists
    if os.path.exists(hex_files_folder) and os.path.isdir(hex_files_folder):
        # Get a list of file names in the folder
        file_names = os.listdir(hex_files_folder)
        
        # Filter out only the files (not directories) and add them to the combobox
        for file_name in file_names:
            file_path = os.path.join(hex_files_folder, file_name)
            if os.path.isfile(file_path):
                ui.hexFileComboBox.addItem(file_name)
                ui.hexFileComboBox.setCurrentText(currentText)


def Flash_Event(ui):
    thr = threading.Thread(target=thread_callback, args=[ui])
    thr.start()
    ui.flashStatusLabel.setText("Flash Status : <span style=\"color:yellow\">In Progress</span></p>")

def AddDevice_Event(ui):
    # getting user setting
    global print_list
    mac_id = ui.macIDShowLabel.text()
    if mac_id == "":
        return
    device_type = ui.deviceTypeComboBox.currentText()
    device_name = ui.deviceNameComboBox.currentText()
    location = ui.locationComboBox.currentText()
    controller_type = ui.controllerTypeComboBox.currentText()
    device_type_index = combo_box_json["device_name_to_index"][device_name]
    mac_id = device_type_index + "_" + mac_id
    is_mac_id_duplicated = any(inner_list and inner_list[0] == mac_id for inner_list in print_list)

    if not is_mac_id_duplicated:
        print_list.append([mac_id, device_type, device_name, location, controller_type])
        PopulateTableView(ui.devicesForPrintTableView, header, print_list)

        if len(print_list) == 3:
            log.WriteCsv(print_list)
            ClearList_Event(ui);

def ClearList_Event(ui):
    global print_list
    print_list = []
    PopulateTableView(ui.devicesForPrintTableView, header, print_list)
    
def PrintNow_Event(ui):
    # todo
    log.WriteCsv(print_list)
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