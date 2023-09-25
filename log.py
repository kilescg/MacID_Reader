import csv
import os
import sqllite_interface
from utils import PopulateTableView

file_path = "database/devices.csv"
fieldnames = ['macID', 'deviceType', 'deviceName', 'Location', 'Controller Type']

def WriteCsv(data_list):
    # Check if the output file already exists and delete it
    if os.path.exists(file_path):
        print("deleting csv")
        os.remove(file_path)
    print("writing new csv")


    # Open the CSV file for writing
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write data rows
        for inner_list in data_list:
            if len(inner_list) == len(fieldnames):
                # Create a dictionary by zipping fieldnames and inner_list
                data_dict = dict(zip(fieldnames, inner_list))
                writer.writerow(data_dict)
            else:
                print(f"Skipping invalid data: {inner_list}")

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
    data_list = [
    ['1', 'Type1', 'Name1', 'Loc1', 'Ctrl1'],
    ['2', 'Type2', 'Name2', 'Loc2', 'Ctrl2'],
    # Add more data lists as needed
    ]

    output_filename = 'output.csv'

    WriteCsv(data_list)