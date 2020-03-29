import speedtest
import psutil as p
import platform
import time
import json
import psycopg2
from configparser import ConfigParser
from datetime import datetime
import pprint
import connection_db


db = connection_db.Connection()
pp = pprint.PrettyPrinter(indent=2)
uname = platform.uname()


def convert_bytes(b, format_to):
    value = float(1024)
    if format_to == "MB":
        value = float(value ** 2)
    elif format_to == "GB":
        value = float(value ** 3)

    return f"{(b / value):.2f}{format_to}"


def get_network_status():
    print('Checking network status...')
    st = speedtest.Speedtest()
    st.download()
    st.upload()
    data = st.results.dict()

    data['timestamp'] = datetime.now().isoformat()
    data['download'] = convert_bytes(data['download'], "MB")
    data['upload'] = convert_bytes(data['upload'], "MB")

    data['server_host'] = data['server']['host']
    data['server_name'] = data['server']['name']
    data['server_sponsor'] = data['server']['sponsor']
    data['server_latency'] = data['server']['latency']
    data['server_lat'] = data['server']['lat']
    data['server_long'] = data['server']['lon']
    del data['server']

    data['client_ip'] = data['client']['ip']
    data['client_isp'] = data['client']['isp']
    data['client_lat'] = data['client']['lat']
    data['client_long'] = data['client']['lon']
    del data['client']
    print('Network status collected')
    return data


def get_system_information():
    print('Checking hardware and systems status...')
    data = {}
    data['hostname'] = uname.node
    data['os'] = uname.system
    data['version'] = uname.version

    boot_time_timestamp = p.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp).isoformat()
    data['boot_time'] = bt
    data['cpu_utilization'] = f"{p.cpu_percent()}%"

    svmem = p.virtual_memory()
    data['memory_total'] = convert_bytes(svmem.total, "GB")
    data['memory_available'] = convert_bytes(svmem.available, "GB")
    data['memory_used'] = convert_bytes(svmem.used, "GB")
    data['memory_percentagem'] = f"{svmem.percent}%"

    partitions = p.disk_partitions()
    # for partition in partitions:
    partition = partitions[0]
    data['partition_device'] = partition.device
    data['partition_mountpoint'] = partition.mountpoint
    data['partition_type'] = partition.fstype
    try:
        partition_usage = p.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        pass
    data['partition_total'] = convert_bytes(partition_usage.total, "GB")
    data['partition_used'] = convert_bytes(partition_usage.used, "GB")
    data['partition_free'] = convert_bytes(partition_usage.free, "GB")
    data['partition_percent'] = f"{partition_usage.percent}%"
    print('Hardware and systems status collected')
    return data


if __name__ == '__main__':

    while True:
        network = get_network_status()
        system = get_system_information()

        network.update(system)

        pp.pprint(network)

        db.manipulate(sql="INSERT INTO public.machine_status(hostname, os, os_version, boot_time, cpu_utilization, " +
                      "memory_total, memory_used, memory_available, memory_percentagem, partition_device, partition_free, " +
                      "partition_mountpoint, partition_percent, partition_total, partition_type, partition_used, download, " +
                      "upload, bytes_sent, bytes_received, ping, client_ip, client_isp, client_lat, client_long, server_host, " +
                      "server_lat, server_long, server_latency, server_name, server_sponsor, share, datetime) " +
                      "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                      .format(network["hostname"], network["os"], network["version"],
                              network["boot_time"], network["cpu_utilization"], network[
                          "memory_total"], network["memory_used"], network["memory_available"],
                          network["memory_percentagem"], network["partition_device"], network[
                          "partition_free"], network["partition_mountpoint"], network["partition_percent"],
                          network["partition_total"], network["partition_type"], network[
                          "partition_used"], network["download"], network["upload"],
                          network["bytes_sent"], network["bytes_received"], network[
                          "ping"], network["client_ip"], network["client_isp"],
                          network["client_lat"], network["client_long"], network[
                          "server_host"], network["server_lat"], network["server_long"],
                          network["server_latency"], network["server_name"], network["server_sponsor"], network["share"], network["timestamp"]))

        print('To stop execution type: CTRL C')
        print('One minute for the next execution...')
        time.sleep(60)
