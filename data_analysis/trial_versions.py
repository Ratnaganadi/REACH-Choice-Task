import pandas
import glob
import numpy as np
import datetime
import os
import sys

SHEET_NAME = "REACH_TASK"

def correct_reading_level(date, level):
    if datetime.datetime(2014,10,15) <= date < datetime.datetime(2014,11,22):
        return level + 2
    elif datetime.datetime(2014,11,22) <= date < datetime.datetime(2014,12,6):
        return level + 1
    else:
        return level

def main(data_dir, output_file):
    try:
        main_data = pandas.read_excel(output_file, SHEET_NAME)
        main_data = {row["Task Version"]: dict(row) for i, row in main_data.iterrows()}
    except IOError:
        main_data = {}

    for filename in glob.glob(os.path.join(data_dir, '*.xls')):
        basename = os.path.basename(filename)
        if ("conflicted copy" not in basename) and ("test" not in basename):
            in_data = pandas.read_excel(filename, "Main")

            date = datetime.datetime.strptime(" ".join(filename.split("_")[-4:-1]), "%Y %b %d")

            if "Task Version" in in_data:
                taskversions = in_data["Task Version"].unique()
            elif "task_version" in in_data:
                taskversions = in_data["task_version"].unique()
            else:
                taskversions = ("",)

            for taskversion in taskversions:
                if not taskversion in main_data:
                    main_data[taskversion] = {}
                    main_data[taskversion]["Task Version"] = taskversion

                if date < main_data[taskversion].get("min_date", datetime.datetime.max):
                    main_data[taskversion]["min_date"] = date

                if date > main_data[taskversion].get("max_date", datetime.datetime.min):
                    main_data[taskversion]["max_date"] = date


    main_data = pandas.DataFrame(main_data.values())

    main_data.sort(columns="min_date", inplace=True)

    main_data.to_excel(output_file, sheet_name=SHEET_NAME, index=False)

if __name__ == "__main__":
    data_dir = sys.argv[1] if len(sys.argv) > 1 else '../data/complete_data/'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'REACH_Task_Versions.xls'
 
    main(data_dir, output_file)