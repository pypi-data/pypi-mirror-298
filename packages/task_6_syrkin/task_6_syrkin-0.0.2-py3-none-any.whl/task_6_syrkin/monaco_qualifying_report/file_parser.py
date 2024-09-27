import datetime
import os


def parse_racing_data(folder_path: str):
    """
    Parses the start.log, end.log, and abbreviations.txt files from the specified folder to extract
    start times, end times, and racer details (name and team).

    Args:
        folder_path (str): Path to the folder containing the log files (start.log, end.log, abbreviations.txt).

    Returns:
        dict: A dictionary with 'start_times', 'end_times', and 'abbreviations', each containing the parsed data.
    """

    # Helper function to parse log files (start.log and end.log)
    def parse_logs(file_path: str):
        racer_times = {}
        with open (file_path, 'r') as file:
            for line in file:
                line = line.strip ()  # Remove any leading or trailing whitespace
                if not line:  # Skip empty lines
                    continue
                abbreviation = line[:3]
                timestamp_str = line[3:].strip ()
                try:
                    timestamp = datetime.datetime.strptime (timestamp_str, '%Y-%m-%d_%H:%M:%S.%f')
                    racer_times[abbreviation] = timestamp
                except ValueError as e:
                    print (f"Error parsing line: {line}. Error: {e}")
        return racer_times

    # Helper function to parse abbreviations.txt
    def parse_abbreviations(file_path: str):
        racer_info = {}
        with open (file_path, 'r') as file:
            for line in file:
                abbreviation, name, team = [item.strip () for item in line.split ('_')]
                racer_info[abbreviation] = (name, team)
        return racer_info

    # File paths
    start_log_path = os.path.join (folder_path, 'start.log')
    end_log_path = os.path.join (folder_path, 'end.log')
    abbreviations_path = os.path.join (folder_path, 'abbreviations.txt')

    # Parse the files
    start_times = parse_logs (start_log_path)
    end_times = parse_logs (end_log_path)
    abbreviations = parse_abbreviations (abbreviations_path)

    return {
        'start_times': start_times,
        'end_times': end_times,
        'abbreviations': abbreviations
    }

# # Example usage:
# folder_path = '../data'
# racing_data = parse_racing_data(folder_path)
# from pprint import pprint
# pprint(racing_data)
