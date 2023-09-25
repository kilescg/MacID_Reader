import subprocess
import sys
import os
import time

JLINK_COMMANDER_PATH = r"C:\Program Files (x86)\SEGGER\Flasher\JLink.exe"
JLINK_POWER_ON_COMMAND = [JLINK_COMMANDER_PATH] + ["power on"]

def MAC_ID_Check():
    # Define the nrfjprog command you want to run
    command = "nrfjprog --memrd 0x10000060 --n 8 --family nrf52"
    mac_id = ""

    # Run the command and capture the return code
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        mac_id = "F4CE36" + result.stdout.split(" ")[1][6:] + result.stdout.split(" ")[2]
    except Exception as e:
        print("Cant Read macID with jprog")
        print("An error occurred:", e)
    return mac_id

def JLink_Power_On():
    jlink_process = subprocess.Popen([JLINK_COMMANDER_PATH], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Send the "power on" command
    command = "power on\n"  # Add '\n' to simulate pressing Enter
    jlink_process.stdin.write(command)
    jlink_process.stdin.flush()

    # Read the response from J-Link (if needed)
    output, error = jlink_process.communicate()

    # Close the subprocess
    jlink_process.stdin.close()
    jlink_process.stdout.close()
    jlink_process.stderr.close()
    jlink_process.wait()

def JLink_Program_Flash(hex_name):
    # Define the nrfjprog command you want to run
    command = f"nrfjprog -f nrf52 --program {hex_name} --sectorerase --verify"
    is_ok = 0

    # Run the command and capture the return code
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
        if "Verify file - Done verifying" in result.stdout:
            is_ok = 1
        else:
            is_ok = 0
        
    except Exception as e:
        print("Cant Read macID with jprog")
        print("An error occurred:", e)
    return is_ok


if __name__ == "__main__":
    # JLink_Power_On()
    MAC_ID_Check()