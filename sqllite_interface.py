from cs50 import SQL
import datetime


class SQLLite_DB:
    # https://www.freecodecamp.org/news/sqlite-python-beginners-tutorial/
    def __init__(self):
        self.sql_db = SQL("sqlite:///database.db")
        self.sql_db.execute("CREATE TABLE IF NOT EXISTS devices (macID TEXT, device_type INT, controller_type TEXT, location TEXT, datetime TEXT)")

    def add_device(self, macID, device_type, controller_type, location):
        current_datetime = datetime.datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d")
        self.sql_db.execute("INSERT INTO devices (macID, device_type, controller_type, location, datetime) VALUES(?, ?, ?, ?, ?)", macID, device_type, controller_type, location, formatted_date)

    def remove_device(self, macID):
        self.sql_db.execute(f"DELETE FROM devices WHERE macID='{macID}'")
    
    def read_devices(self):
        devices = self.sql_db.execute("SELECT * FROM devices")
        print(devices)

if __name__ == "__main__":
    sql_lite_db = SQLLite_DB()
    sql_lite_db.read_devices()