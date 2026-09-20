import time
import pandas as pd

from src.database_service import insert_record
from src.dashboard import update_dashboard


class StreamingSimulator:

    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)
        self.current_index = 0

    def nextDataPoint(self):

        if self.current_index >= len(self.data):
            return None

        data_point = self.data.iloc[self.current_index]
        self.current_index += 1

        return data_point

    def send_to_database(self, data_point):

        insert_record(
            data_point["Trait"],
            data_point["Axis #1"],
            data_point["Axis #2"],
            data_point["Axis #3"],
            data_point["Axis #4"],
            data_point["Axis #5"],
            data_point["Axis #6"],
            data_point["Axis #7"],
            data_point["Axis #8"],
            data_point["Time"]
        )

    def send_to_dashboard(self, data_point):

        update_dashboard(data_point)


    def start_stream(self):

        print("Starting robot data stream...")

        record_number = 0

        while True:

            data_point = self.nextDataPoint()

            if data_point is None:
                break

            record_number += 1

            print(f"Sending record {record_number}")
            print(data_point)

            self.send_to_database(data_point)
            self.send_to_dashboard(data_point)

            if self.current_index < len(self.data):
                time.sleep(2)

        print("End of dataset")
        print("Streaming stopped")
