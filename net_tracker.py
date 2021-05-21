import json
import psutil
import datetime
import csv
import time


def get_timestamp():
    return datetime.datetime.now()


def get_current_transfer():
    return psutil.net_io_counters()[0] + psutil.net_io_counters()[1]


def get_init_transfer():
    with open(r"C:\bitbucket\python-code\playground\init.json", "r") as f:
        init_v = json.load(f)
    return init_v['transfer'][0]['bytes_sent'] + init_v['transfer'][0]['bytes_recv']


def update_init():
    data = {}
    data['transfer'] = []
    data['transfer'].append({'bytes_sent': psutil.net_io_counters()[0], 'bytes_recv': psutil.net_io_counters()[1]})

    with open(r"C:\bitbucket\python-code\playground\init.json", "w") as f:
        json.dump(data, f)


def save_to_csv(delta):
    with open(r'C:\bitbucket\python-code\playground\network_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([get_timestamp(), delta])


if __name__ == '__main__':
    while True:
        delta = round((get_current_transfer() - get_init_transfer()) * 0.000001, 2)
        update_init()
        save_to_csv(delta)
        time.sleep(300)
