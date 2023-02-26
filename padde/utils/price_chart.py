import json
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO


class ConsumptionChart:
    def __init__(self, json_file):
        self.json_file = json_file
        self.x = []
        self.y = []

    def load_data(self):
        with open(self.json_file, 'r') as f:
            data = json.load(f)

        for entry in data:
            dt = datetime.fromisoformat(entry['from'][:-6])
            self.x.append(dt)
            self.y.append(entry['consumption'])

    def plot_data(self):
        plt.plot(self.x, self.y)
        plt.xlabel('Time')
        plt.ylabel('Power Consumption (kWh)')

    def save_plot(self, png_file):
        plt.savefig(png_file)

    def gen_plot(self):
        self.load_data()
        self.plot_data()
        self.save_plot('padde/data/power_consumption.png')

