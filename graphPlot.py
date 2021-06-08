import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime


def plotGraph(col):
    data = pd.read_csv("sensor_readings.csv")

    # process date time
    dateTime = []
    for date, time in zip(data["date"], data["time"]):
        # print(date, time)
        year, month, day = map(int, date.split("-"))
        hour, minute, second = map(int, time.split(":"))
        dateTime.append(datetime.datetime(
            year, month, day, hour, minute, second))

    # To set Figure size
    plt.figure(figsize=(9, 4))

    # To plot graph, with datetime as x value and specified param as y value
    plt.plot(dateTime, data[col], marker='.')
    plt.title("{} Graph".format(col))
    plt.xlabel("Date and Time")
    plt.ylabel(col)

    plt.show()


# PlotGraph("PH")
