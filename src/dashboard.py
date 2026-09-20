import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

from src.database_service import get_records

times = []
axis_1_values = []
axis_2_values = []
axis_3_values = []
axis_4_values = []
axis_5_values = []
axis_6_values = []
axis_7_values = []
axis_8_values = []


def update_dashboard(data_point):
    plt.ion()
    timestamp = datetime.fromisoformat(
        data_point["Time"].replace("Z", "+00:00")
)

    times.append(timestamp)

    axis_1_values.append(data_point["Axis #1"])
    axis_2_values.append(data_point["Axis #2"])
    axis_3_values.append(data_point["Axis #3"])
    axis_4_values.append(data_point["Axis #4"])
    axis_5_values.append(data_point["Axis #5"])
    axis_6_values.append(data_point["Axis #6"])
    axis_7_values.append(data_point["Axis #7"])
    axis_8_values.append(data_point["Axis #8"])

    while times[0] < timestamp - timedelta(seconds=90):
        times.pop(0)
        axis_1_values.pop(0)
        axis_2_values.pop(0)
        axis_3_values.pop(0)
        axis_4_values.pop(0)
        axis_5_values.pop(0)
        axis_6_values.pop(0)
        axis_7_values.pop(0)
        axis_8_values.pop(0)

    plt.clf()

    plt.plot(times, axis_1_values, label="Axis #1")
    plt.plot(times, axis_2_values, label="Axis #2")
    plt.plot(times, axis_3_values, label="Axis #3")
    plt.plot(times, axis_4_values, label="Axis #4")
    plt.plot(times, axis_5_values, label="Axis #5")
    plt.plot(times, axis_6_values, label="Axis #6")
    plt.plot(times, axis_7_values, label="Axis #7")
    plt.plot(times, axis_8_values, label="Axis #8")

    plt.xlabel("Time")
    plt.ylabel("Axis Reading")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    plt.gcf().autofmt_xdate()
    plt.title("Robot Axis Readings - Live Data")
    plt.legend()

    plt.show()
    plt.pause(0.01)

def show_historical_data():
    records = get_records()

    print(f"Dashboard received {len(records)} historical records.")
       

    historical_times = []
    historical_axis_1 = []
    historical_axis_2 = []
    historical_axis_3 = []
    historical_axis_4 = []
    historical_axis_5 = []
    historical_axis_6 = []
    historical_axis_7 = []
    historical_axis_8 = []

    for record in records:
        timestamp = datetime.combine(
            datetime(record[10], record[11], record[12]),
            record[13]
        )

        historical_times.append(timestamp)
        historical_axis_1.append(record[2])
        historical_axis_2.append(record[3])
        historical_axis_3.append(record[4])
        historical_axis_4.append(record[5])
        historical_axis_5.append(record[6])
        historical_axis_6.append(record[7])
        historical_axis_7.append(record[8])
        historical_axis_8.append(record[9])

    plt.figure()

    plt.plot(historical_times, historical_axis_1, label="Axis #1")
    plt.plot(historical_times, historical_axis_2, label="Axis #2")
    plt.plot(historical_times, historical_axis_3, label="Axis #3")
    plt.plot(historical_times, historical_axis_4, label="Axis #4")
    plt.plot(historical_times, historical_axis_5, label="Axis #5")
    plt.plot(historical_times, historical_axis_6, label="Axis #6")
    plt.plot(historical_times, historical_axis_7, label="Axis #7")
    plt.plot(historical_times, historical_axis_8, label="Axis #8")

    plt.xlabel("Time")
    plt.ylabel("Axis Reading")
    plt.title("Robot Axis Readings - Full Historical Dataset")
    plt.legend()

    plt.show()

if __name__ == "__main__":
    show_historical_data()