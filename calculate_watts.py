import csv

import toml


def watts(duration_hours: float, kwhs: float):
    return (1000 * kwhs) / duration_hours


def hours(duration_seconds: float):
    return duration_seconds / 3600


def calculate_watts():
    data = {}
    with open("emissions.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            experiment = row[2]
            duration_seconds = float(row[3])
            power_kwh = float(row[5])

            duration_hours = hours(duration_seconds)
            power_watts = watts(duration_hours, power_kwh)

            data[experiment] = {"name": experiment, "watts": power_watts, "running_time": duration_hours}
    export = {"experiment": []}
    for k, v in data.items():
        export["experiment"].append(v)
    print(toml.dumps(export))


if __name__ == '__main__':
    calculate_watts()
