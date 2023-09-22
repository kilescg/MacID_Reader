# MacID Reader Tool

The MacID Reader Tool is a utility designed for reading MacIDs using the Segger Flasher Pro. It is built using PyQt5.

## Prerequisites

Before using this tool, you need to ensure that the following software is installed:

1. **Jlink:** Jlink is a required tool for the MacID Reader Tool. You can download and install it from [Segger's website](https://www.segger.com/downloads/jlink).

2. **NRF Command Line Tool:** This tool is also required for proper functioning. You can download and install it from [Nordic Semiconductor's website](https://www.nordicsemi.com/Software-and-Tools/Development-Tools/nRF-Command-Line-Tools/Download).

3. **Python** which some dependency such as *PqQt5*

```
pip install PyQt5
pip install cs50
```

## Features

- **MacID Reading:** The tool enables the reading of MacIDs using the Segger Flasher Pro, automatically printing the results after three reads. Additionally, you have the option to manually trigger printing using the *Print Now* function before reaching three reads.

- **Upcoming Features:** While SQLite functionality is currently not implemented, it is planned as a future enhancement.

- **Upcoming Features:** The Flashing Button currently does not update its status. This will be addressed once I'm back in the office.

- **Printing:** The printing functionality is not yet implemented in the main tool but can be found in the `utils.py` file. The specific function you can use for printing is `PrintNow()`.

## Usage

1. Install the prerequisite software mentioned above.

2. Launch the MacID Reader Tool by running **main.py**.

<!-- 3. Follow the on-screen instructions to read MacIDs using your Segger Flasher Pro. -->

## Future Development

The development of this tool is ongoing, and future updates may include:

- Implementation of SQLite functionality for data storage and management.

- Integration of the printing feature directly into the main application.

---
