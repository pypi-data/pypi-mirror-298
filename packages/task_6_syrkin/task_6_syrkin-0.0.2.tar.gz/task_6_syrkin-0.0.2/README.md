# Monaco 2018 Formula 1 Qualification Report

## Description
This project provides a report on the Formula 1 qualification for the Monaco 2018 stage. The program allows analyzing the best lap times of drivers, sorting the results, and filtering data by a specific driver.

## Requirements
The project requires Python version 3.12 or higher, and the following dependencies:
- `pytest>=8.3.2`
- `coverage>=7.6.1`
- `parameterized>=0.9.0`
- `argparse>=1.4.0`
- `setuptools>=75.1.0`

## Installation
To install the project, use the following command:

```bash
pip install task_6_syrkin
```

## Usage
### Running via CLI
Once installed, you can use the program through the command line. Example usage:

```bash
report --files ./data --asc
```

### Parameter descriptions:
- `--files`: Path to the folder containing the log files (`start.log`, `end.log`, and `abbreviations.txt`).
- `--asc`: Sort the lap times in ascending order (default).
- `--desc`: Sort the lap times in descending order.
- `--driver "Driver Name"`: Show statistics for a specific driver.

### Example commands:
1. Full report sorted in ascending order:
   ```bash
   monaco-report --files ./data --asc
   ```
2. Full report sorted in descending order:
   ```bash
   monaco-report --files ./data --desc
   ```
3. Filtering and showing information for a specific driver (e.g., Sebastian Vettel):
   ```bash
   monaco-report --files ./data --driver "Sebastian Vettel"
   ```

```

## License
This project is licensed under the MIT License. See the LICENSE file for details.