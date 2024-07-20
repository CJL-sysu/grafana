import psutil
from connect import database
import GPUtil
import argparse
from time import sleep
def avg(lst):
    return sum(lst) / len(lst)
# print(f"{avg(psutil.cpu_percent(interval=0.5, percpu=True))}%")
def get_cpu_percent():
    return avg(psutil.cpu_percent(interval=0.5, percpu=True))
def get_mem_percent():
    return psutil.virtual_memory().percent

def get_gpu():
    GPUs = GPUtil.getGPUs()
    if len(GPUs) == 0:
        return 0, 0
    else:
        return GPUs[0].load, GPUs[0].memoryUtil
    
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
        gpu_load, gpu_mem = get_gpu()
        db.exec(
            f"""INSERT INTO {args.table} (time, cpu, mem, gpu_load, gpu_mem) VALUES (NOW(), {cpu_percent}, {mem_percent}, {gpu_load}, {gpu_mem});"""
        )
        sleep(args.flush)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.134.123")
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--user", type=str, default="node1")
    parser.add_argument("--pwd", type=str, default="mysql114514")
    parser.add_argument("--database", type=str, default="grafana")
    parser.add_argument("--table", type=str, default="gauge")
    parser.add_argument("--log_file", type=str, default="log/transformer.log")
    parser.add_argument("--flush", type=int, default=5, help="flush interval (s)")
    args = parser.parse_args()
    main(args)
