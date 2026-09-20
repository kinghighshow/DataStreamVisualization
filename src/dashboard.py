import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

from src.database_service import get_records


# Store recent live-stream data
times = []
axis_1_values = []
axis_2_values = []
axis_3_values = []
axis_4_values = []
axis_5_values = []
axis_6_values = []
axis_7_values = []
axis_8_values = []

# Live figure is created only when live data arrives
live_fig = None
live_ax = None


def update_dashboard(data_point):
    global live_fig, live_ax

    # Create ONE live figure the first time data arrives
    if live_fig is None:
        plt.ion()
        live_fig, live_ax = plt.subplots()

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

    # Keep only the most recent 90 seconds
    while times and times[0] < timestamp - timedelta(seconds=90):
        times.pop(0)
        axis_1_values.pop(0)
        axis_2_values.pop(0)
        axis_3_values.pop(0)
        axis_4_values.pop(0)
        axis_5_values.pop(0)
        axis_6_values.pop(0)
        axis_7_values.pop(0)
        axis_8_values.pop(0)

    # Clear only the live chart
    live_ax.clear()

    live_ax.plot(times, axis_1_values, label="Axis #1")
    live_ax.plot(times, axis_2_values, label="Axis #2")
    live_ax.plot(times, axis_3_values, label="Axis #3")
    live_ax.plot(times, axis_4_values, label="Axis #4")
    live_ax.plot(times, axis_5_values, label="Axis #5")
    live_ax.plot(times, axis_6_values, label="Axis #6")
    live_ax.plot(times, axis_7_values, label="Axis #7")
    live_ax.plot(times, axis_8_values, label="Axis #8")

    live_ax.set_xlabel("Time")
    live_ax.set_ylabel("Axis Reading")
    live_ax.set_title("Robot Axis Readings - Live Data")
    live_ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    live_ax.legend()

    live_fig.autofmt_xdate()
    live_fig.tight_layout()
    live_fig.canvas.draw()
    live_fig.canvas.flush_events()

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

    # Historical data gets its own figure
    historical_fig, historical_ax = plt.subplots()

    historical_ax.plot(
        historical_times, historical_axis_1, label="Axis #1"
    )
    historical_ax.plot(
        historical_times, historical_axis_2, label="Axis #2"
    )
    historical_ax.plot(
        historical_times, historical_axis_3, label="Axis #3"
    )
    historical_ax.plot(
        historical_times, historical_axis_4, label="Axis #4"
    )
    historical_ax.plot(
        historical_times, historical_axis_5, label="Axis #5"
    )
    historical_ax.plot(
        historical_times, historical_axis_6, label="Axis #6"
    )
    historical_ax.plot(
        historical_times, historical_axis_7, label="Axis #7"
    )
    historical_ax.plot(
        historical_times, historical_axis_8, label="Axis #8"
    )

    historical_ax.set_xlabel("Time")
    historical_ax.set_ylabel("Axis Reading")
    historical_ax.set_title(
        "Robot Axis Readings - Full Historical Dataset"
    )

    historical_ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%Y-%m-%d %H:%M")
    )

    historical_ax.legend()

    historical_fig.autofmt_xdate()
    historical_fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    show_historical_data()