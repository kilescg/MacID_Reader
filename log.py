import csv
import os
import sqllite_interface
from utils import PopulateTableView, PrintLabel

file_path = "database/employee_file.csv"
fieldnames = ['macID', 'deviceType', 'deviceName', 'Location', 'Controller Type']

def WriteCSV(mac_id, deviceType, deviceName, location, controllerType):    
    new_row = {"macID" : mac_id, 
                             "deviceType" : deviceType, 
                             "deviceName" : deviceName, 
                             "Location" : location, 
                             "Controller Type" : controllerType}
    # Write data_list to the CSV file

    try:
        with open(file_path, 'r', newline='') as file:
            # Read the existing data
            data = list(csv.DictReader(file))
    except FileNotFoundError:
        # If the file doesn't exist, create it with headers and add the new row
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(new_row)
    else:
        # If the file exists, open it in append mode and add the new row
        with open(file_path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(new_row)

def CheckIfReachMaxLabel(ui, maxLabel):
    shouldRemove = 0
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "r+") as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
            num_rows = len(list(csvreader))
            if num_rows == maxLabel:
                '''
                Sent to database (WIP)
                '''
                PrintLabel()
                shouldRemove = 1
                PopulateTableView(ui.devicesForPrintTableView, fieldnames, [])
    if shouldRemove:
        os.remove(file_path)

def ResetCSV():
    try:
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            print(f"Deleted {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

def ShowTableFromCSV(table):
    showList = []
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            showList = list(csvreader).copy()
    
    PopulateTableView(table, showList[0], showList[1:])

def IsStringInCsv(input_string, target_field_name):
    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get(target_field_name) == input_string:
                    return True
    except FileNotFoundError:
        return False
    

if __name__ == "__main__":
    pass