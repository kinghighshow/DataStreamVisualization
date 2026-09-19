import os
import time
import pandas as pd
import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class StreamingSimulator:
    """
    Simulates a robot sending telemetry records from a CSV file.

    Each record can be stored in PostgreSQL and passed to a dashboard.
    """

    def __init__(self, csv_path):
        """Load the robot dataset and start at the first record."""
        self.data = pd.read_csv(csv_path)
        self.current_index = 0

    def nextDataPoint(self):
        """
        Return the next robot record.

        Returns None when all records have been processed.
        """
        if self.current_index >= len(self.data):
            return None

        data_point = self.data.iloc[self.current_index]
        self.current_index += 1

        return data_point

    def connect_db(self):
        """Connect to the PostgreSQL database."""
        if not DATABASE_URL:
            print("DATABASE_URL is not set.")
            return None

        connection = psycopg.connect(DATABASE_URL)
        print("Database connected successfully.")

        return connection

    def create_table(self):
        """Create the robot_data table if it does not already exist."""
        connection = self.connect_db()

        if connection is None:
            return

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS robot_data (
                id BIGSERIAL PRIMARY KEY,
                trait VARCHAR(50),
                axis_1 DOUBLE PRECISION,
                axis_2 DOUBLE PRECISION,
                axis_3 DOUBLE PRECISION,
                axis_4 DOUBLE PRECISION,
                axis_5 DOUBLE PRECISION,
                axis_6 DOUBLE PRECISION,
                axis_7 DOUBLE PRECISION,
                axis_8 DOUBLE PRECISION,
                year INTEGER,
                month INTEGER,
                day INTEGER,
                time TIME,
                UNIQUE (year, month, day, time)
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()

        print("robot_data table is ready.")

    def send_to_database(self, data_point):
        """
        Insert one streamed robot record into PostgreSQL.
        """
        if DATABASE_URL is None:
            print("Database skipped: DATABASE_URL is not set.")
            return

        from datetime import datetime

        timestamp = datetime.fromisoformat(
            str(data_point["Time"]).replace("Z", "+00:00")
        )

        year = timestamp.year
        month = timestamp.month
        day = timestamp.day
        record_time = timestamp.time().replace(tzinfo=None)

        connection = self.connect_db()

        if connection is None:
            return

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO robot_data (
                trait,
                axis_1,
                axis_2,
                axis_3,
                axis_4,
                axis_5,
                axis_6,
                axis_7,
                axis_8,
                year,
                month,
                day,
                time
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            ON CONFLICT (year, month, day, time) DO NOTHING
        """, (
            data_point["Trait"],
            data_point["Axis #1"],
            data_point["Axis #2"],
            data_point["Axis #3"],
            data_point["Axis #4"],
            data_point["Axis #5"],
            data_point["Axis #6"],
            data_point["Axis #7"],
            data_point["Axis #8"],
            year,
            month,
            day,
            record_time
        ))

        connection.commit()

        if cursor.rowcount == 1:
            print("  -> Database: record inserted")
        else:
            print("  -> Database: duplicate record skipped")

        cursor.close()
        connection.close()

    def send_to_dashboard(self, data_point):
        """
        Placeholder for the dashboard component.
        """
        print("  -> Dashboard: record received")

    def get_records(self):
        """Retrieve stored robot records from PostgreSQL."""
        connection = self.connect_db()

        if connection is None:
            return []

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM robot_data
            ORDER BY id
        """)

        records = cursor.fetchall()

        cursor.close()
        connection.close()

        print(f"{len(records)} record(s) retrieved from database.")

        return records

    def start_stream(self):
        """
        Stream records one at a time with a 2-second delay.
        """
        print("Starting robot data stream...")

        record_number = 0

        while True:
            data_point = self.nextDataPoint()

            if data_point is None:
                break

            record_number += 1

            print(f"\nSending record {record_number}...")
            print(data_point)

            self.send_to_database(data_point)
            self.send_to_dashboard(data_point)

            if self.current_index < len(self.data):
                time.sleep(2)

        print("\nEnd of dataset.")
        print("Streaming stopped.")