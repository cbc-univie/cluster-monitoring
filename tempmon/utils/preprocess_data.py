# This file preporcess the data
import copy
import os
import re
from datetime import datetime

import numpy as np
import pandas as pd
import pendulum
import pytz
from definitions import PROJECT_ROOT


def convert_utc_to_local_time(utc_time):
    cet = pytz.timezone('CET')
    tz_abbreviation = utc_time.astimezone(cet).tzname()

    if tz_abbreviation == 'CET':
        print("The time is in Central European Time (CET).")
    elif tz_abbreviation == 'CEST':
        print("The time is in Central European Summer Time (CEST).")


class BaseLineReader:
    def __init__(self):
        self.per_line_dict = {
            "outdoor temp": np.nan, #float 
            "GPU jobs": np.nan, #int
            "CPU jobs": np.nan, #int 
            "CPU on GPU jobs": np.nan, #int
            "total jobs": np.nan, #int
            "server room temp": np.nan, #float
            "date": np.nan, #datetime
        }

    def detect_format(self, line):
        raise NotImplementedError("Subclasses must implement detect_format() method.")
    
    def read_line(self, line):
        raise NotImplementedError("Subclasses must implement read_line() method.")

class LineReaderError(BaseLineReader):
    def detect_format(self, line):
        return line.startswith("Error 23")
    
    def read_line(self, line):
        #if line.startswith("Error 23"):
            return copy.deepcopy(self.per_line_dict)

class LineReader1(BaseLineReader):
    def detect_format(self, line):
        return re.match(r"[A-Za-z]{3} \d{2} \d{2}:\d{2}:\d{2} Sensor 0 C: \d+\.\d+ F: \d+\.\d+", line)
    
    def read_line(self, line):
        # Format 1: Jul 24 18:45:03 Sensor 0 C: 22.81 F: 73.06
        time_format = "%b %d %H:%M:%S %Y"
        record = line.strip().split("Sensor 0")
        my_line = copy.deepcopy(self.per_line_dict)
        my_line.update({"server room temp": float(record[1].strip().split(" ")[1]), "date": datetime.strptime(f"{record[0].strip()} 2023", time_format)})
        return my_line

class LineReader2(BaseLineReader):
    def detect_format(self, line):
        return re.match(r"(outdoor|ambient) temp: \d+(\.\d+)?, GPU jobs: \d+, CPU jobs: \d+, CPU on GPU jobs: \d+, total jobs: \d+, [A-Za-z]{3} \d{2} \d{2}:\d{2}:\d{2} Sensor 0 C: \d+\.\d+ F: \d+\.\d+", line)
    
    def read_line(self, line):
        # Format 2: outdoor temp: 18.76, GPU jobs: 16, CPU jobs: 4, CPU on GPU jobs: 0, total jobs: 20, Jul 25 14:30:04 Sensor 0 C: 22.62 F: 72.72
         # or (only difference: outdoor vs ambient)
            # ambient temp: 18.76, GPU jobs: 18, CPU jobs: 0, CPU on GPU jobs: 1, total jobs: 19, Jul 25 14:22:44 Sensor 0 C: 18.19 F: 64.74
        time_format = "%b %d %H:%M:%S %Y"
        record = line.strip().split(", ")
        my_line = copy.deepcopy(self.per_line_dict)
        my_line.update({"outdoor temp": float(record[0].split(": ")[1]), "GPU jobs": int(record[1].split(": ")[1]), "CPU jobs": int(record[2].split(": ")[1]), 
                        "CPU on GPU jobs": int(record[3].split(": ")[1]), "total jobs": int(record[4].split(": ")[1])})
        record_last = record[5].strip().split("Sensor 0")
        my_line.update({"server room temp": float(record_last[1].strip().split(" ")[1]), "date": datetime.strptime(f"{record_last[0].strip()} 2023", time_format)})
        return my_line

class LineReader3(BaseLineReader):
    def detect_format(self, line):
        return re.match(r"outdoor temp: -?\d+(\.\d+)?, GPU jobs: \d+, CPU jobs: \d+, CPU on GPU jobs: \d+, total jobs: \d+, server room temp: -?\d+\.\d+, date: [A-Za-z]{3} [A-Za-z]{3} *\d{1,2} \d{2}:\d{2}:\d{2} UTC \d{4}", line) # becuase CEST and CET
    
    def read_line(self, line):
        # Format 3: outdoor temp: 27, GPU jobs: 16, CPU jobs: 0, CPU on GPU jobs: 0, total jobs: 16, server room temp: 22.81, date: Fri Jul 28 17:00:02 CEST 2023
        time_format = "%a %b %d %H:%M:%S %Z %Y"
        record = line.strip().split(", ")

        utc_time = datetime.strptime(record[6].split(": ")[1], time_format)
        pendulum_time = pendulum.instance(utc_time)
        local_time = pendulum_time.in_tz("Europe/Vienna")

        my_line = copy.deepcopy(self.per_line_dict)
        my_line.update({"outdoor temp": float(record[0].split(": ")[1]), "GPU jobs": int(record[1].split(": ")[1]), "CPU jobs": int(record[2].split(": ")[1]), 
                        "CPU on GPU jobs": int(record[3].split(": ")[1]), "total jobs": int(record[4].split(": ")[1]), "server room temp": float(record[5].split(": ")[1]), 
                        "date": local_time})
        return my_line

class BufferReader:
    def __init__(self, buffer):
        self.line_readers = [LineReaderError(), LineReader1(), LineReader2(), LineReader3()]
        self.buffer = buffer
        self.df = self.read_buffer(buffer)

    def read_buffer(self, buffer):
        dict_list = []
        for line in buffer:
            line_dict = self.read_line(line)
            dict_list.append(line_dict)
        df = pd.DataFrame(dict_list)
        df = df.reindex(columns=self.line_readers[0].per_line_dict.keys())
        return df

    def read_line(self, line):
        for reader in self.line_readers:
            if reader.detect_format(line):
                return reader.read_line(line)
        print("Format not recognized")
        print(line)
        raise RuntimeError()


def generate_rs02_df():
    file = os.path.join(PROJECT_ROOT, "data", "temp_rs02.log")
    with open(file, "r") as f:
        buffer = f.readlines()
    reader = BufferReader(buffer)
    return reader.df

def generate_rs10_df():
    file = os.path.join(PROJECT_ROOT, "data", "temp_rs10.log")
    with open(file, "r") as f:
        buffer = f.readlines()
    reader = BufferReader(buffer)
    return reader.df

def generate_dfs():
    return generate_rs02_df(), generate_rs10_df()

def filter(*args: pd.DataFrame, **kwargs):
    col_name = kwargs["col_name"]
    for df in args:
        filtered_data = df[col_name].rolling(15).mean()
        df[f"filtered {col_name}"] = filtered_data
    return args
