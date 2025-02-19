import os
import csv
import sys
from typing import Dict, Any, Literal, List, NamedTuple
from datetime import datetime

class Log(NamedTuple):
    time: str
    description: str
    state: Literal["START", "END"]
    pid: str

class Report(NamedTuple):
    start: Log
    end: Log

class Summary(NamedTuple):
    total_records: int
    error_records: int
    warning_records: int
    exception_records: int
    start_without_end_records: int

DEFAUL_FILE_NAME = './files/log.csv'
TIME_FORMAT = "%H:%M:%S"
WARNING_TIME_IN_SECONDS = 5 * 60 # 5 mins
ERROR_TIME_IN_SECONDS = 10 * 60 # 10 mins
VALID_STATE = ["START", "END"]

def is_file_exist(filename: str) -> bool:
    """
    Check if the filename is exist
    """
    return os.path.exists(filename)

def time_diff_in_seconds(start_at:str, end_at:str) -> int:
    start_time = datetime.strptime(start_at, TIME_FORMAT)
    end_time = datetime.strptime(end_at, TIME_FORMAT)
    time_diff = end_time - start_time
    time_diff_seconds = time_diff.total_seconds()
    return int(time_diff_seconds)

def is_warining(start_at: str, end_at: str) -> bool:
    time_diff = time_diff_in_seconds(start_at, end_at)
    return time_diff >= WARNING_TIME_IN_SECONDS and time_diff < ERROR_TIME_IN_SECONDS

def is_error(start_at: str, end_at: str) -> bool:
    time_diff = time_diff_in_seconds(start_at, end_at)
    return time_diff >= ERROR_TIME_IN_SECONDS

def analy_log(filename: str) -> Summary:
    """Reads a CSV file safely and handles missing file errors."""
    if not is_file_exist(filename):
        print(f"Error: {filename} not found.")
        return Summary(total_records=0, error_records=0, warning_records=0, exception_records=0, start_without_end_records=0)

    total_records = 0
    logs: Dict[Any] = {}
    exception: List[Any] = []
    warning: List[Report] = []
    error: List[Report] = []
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for columns in reader:
            try:
                log = Log(time=columns[0].strip(), description=columns[1].strip(), state=columns[2].strip(), pid=columns[3].strip())
                if log.state in VALID_STATE:
                    key = f"log_{log.pid}"

                    start_job = logs.get(key)
                    if start_job:
                        if is_error(start_job.time, log.time):
                            error.append(Report(start=start_job, end=log))
                        elif is_warining(start_job.time, log.time):
                            warning.append(Report(start=start_job, end=log))
                        del logs[key]
                    else:
                        logs[key] = log
                total_records += 1
            except Exception:
                exception.append(columns)


    return Summary(total_records=total_records, error_records=len(error), warning_records=len(warning), exception_records=len(exception), start_without_end_records=len(logs))

# Check if a filename was provided
filename = DEFAUL_FILE_NAME

if len(sys.argv) > 1:
    filename = sys.argv[1]

result = analy_log(filename)
print(f"Total records: {result.total_records}\n" + 
      f"Total error: {result.error_records}\n" +
      f"Total warning: {result.warning_records}\n" +
      f"Total excaption: {result.exception_records}\n" +
      f"Total start without stop: {result.start_without_end_records}") 



