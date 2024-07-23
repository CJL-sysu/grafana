import psutil
from connect import database
import GPUtil
import argparse
from time import sleep
from time import time
def avg(lst):
    return sum(lst) / len(lst)
# print(f"{avg(psutil.cpu_percent(interval=0.5, percpu=True))}%")
def get_cpu_percent():
    return avg(psutil.cpu_percent(interval=0.5, percpu=True))
def get_mem_percent():
    return psutil.virtual_memory().percent

def get_mem_total():
    return psutil.virtual_memory().total/(1024*1024)

def get_mem_used():
    return psutil.virtual_memory().used/(1024*1024)

disk_io_start = psutil.disk_io_counters()
last_time = time()
def get_disk_io_rate():
    global disk_io_start, last_time
    disk_io_end = psutil.disk_io_counters()
    current_time = time()
    read_bytes = disk_io_end.read_bytes - disk_io_start.read_bytes
    write_bytes = disk_io_end.write_bytes - disk_io_start.write_bytes

    read_rate = read_bytes / (current_time - last_time)
    write_rate = write_bytes / (current_time - last_time)

    disk_io_start = disk_io_end
    last_time = current_time
    return read_rate, write_rate

def get_gpu():
    """
    Returns: gpu load, gpu memory percentage, gpu memory used, gpu memory total, gpu temperature
    """
    GPUs = GPUtil.getGPUs()
    if len(GPUs) == 0:
        return 0, 0
    else:
        return GPUs[0].load, GPUs[0].memoryUtil, GPUs[0].memoryUsed, GPUs[0].memoryTotal, GPUs[0].temperature
    
def main(args):
    db = database(
        ip=args.ip,
        port=args.port,
        user=args.user,
        pwd=args.pwd,
        database=args.database,
    )
    while True:
        cpu_percent = get_cpu_percent()
        mem_percent = get_mem_percent()
        gpu_load, gpu_mem_percent, gpu_mem_used, gpu_mem_total, gpu_temp = get_gpu()
        db.exec(
            f"""INSERT INTO {args.database}.gauge (time, cpu, mem, gpu_load, gpu_mem) VALUES (NOW(), {cpu_percent}, {mem_percent}, {gpu_load}, {gpu_mem_percent});"""
        )
        db.exec(
            f"""INSERT INTO {args.database}.memory (time, total, used) VALUES (NOW(), {get_mem_total()}, {get_mem_used()});"""
        )
        db.exec(
            f"""INSERT INTO {args.database}.gpumem (time, total, used) VALUES (NOW(), {gpu_mem_total}, {gpu_mem_used});"""
        )
        sleep(args.flush)
        read_rate, write_rate = get_disk_io_rate()
        db.exec(
            f"""INSERT INTO {args.database}.diskio (time, read_rate, write_rate) VALUES (NOW(), {read_rate / 1024}, {write_rate / 1024});"""
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.134.123")
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--user", type=str, default="node1")
    parser.add_argument("--pwd", type=str, default="mysql114514")
    parser.add_argument("--database", type=str, default="grafana")
    parser.add_argument("--log_file", type=str, default="log/transformer.log")
    parser.add_argument("--flush", type=int, default=10, help="flush interval (s)")
    args = parser.parse_args()
    main(args)
