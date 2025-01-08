import argparse
import subprocess
import time
from monitor import NVGPUMonitor
from csv_process import map_list_to_csv, csv_to_map_list
from plots import plot_time_series
from typing import List, Dict, Any
import os
from datetime import datetime, timedelta

def get_map_list_fileds(map_list: List[Dict[str, Any]]) -> List[str]:
    return map_list[0].keys()

def get_list_from_map_list_by_filed(map_list: List[Dict[str, Any]], filed: str) -> List[Any]:
    return [float(m[filed]) for m in map_list]

def start(args):
    output_path = None
    if args.output is not None:
        output_path = os.path.abspath(args.output)
        if os.path.exists(output_path) and not args.force_overwrite:
            print(f"Error: The file '{output_path}' already exists. Use --force-overwrite to overwrite it.")
    monitor = NVGPUMonitor()
    monitor.start_monitor(interval = args.interval, show = (args.output is None))
    # 等待结束
    if args.duration is not None:
        time.sleep(args.duration)
        monitor.stop_monitor()
    else:
        monitor.wait_until_stop()
    if output_path is not None and (not os.path.exists(output_path) or args.force_overwrite):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        utilization = monitor.get_monitor_result()
        map_list_to_csv(utilization, output_path)
        print(f"Output data to file \"{output_path}\"")

def show(args):
    utilization = csv_to_map_list(args.input)
    fileds = get_map_list_fileds(utilization)
    for filed in fileds:
        data_list = []
        if filed.endswith(" gpu utilization") or filed.endswith(" memory utilization"):
            data_list = get_list_from_map_list_by_filed(utilization, filed)
        else:
            continue
        output_path = os.path.abspath(args.output + " " + filed + '.png')
        if os.path.exists(output_path) and not args.force_overwrite:
            print(f"Error: The file '{output_path}' already exists. Use --force-overwrite to overwrite it.")
        else:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            plot_time_series(data_list, output_path, filed, "Time", "%", start_time = utilization[0]["Time"], end_time = utilization[-1]["Time"])
            print(f"Plot \'{filed}\' line chart to file \"{output_path}\"")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nsight Concurrent Kernels")
    subparsers = parser.add_subparsers()

    # start命令
    parser_start = subparsers.add_parser('start', help='Start monitoring GPU utilization')
    parser_start.add_argument('-i', '--interval', type=float, default=0.05, help='Sampling interval in seconds (default: 0.05)')
    parser_start.add_argument('-d', '--duration', type=float, default=None, help='Total duration in seconds for monitoring. If not specified, it runs indefinitely.')
    parser_start.add_argument('-o', '--output', type=str, default=None, help='Output CSV file path to save GPU utilization data. If not specified, data is printed to the console.')
    parser_start.add_argument('-f', '--force-overwrite', action="store_true", help='Force overwrite the output file if it already exists.')
    parser_start.set_defaults(func=start)

    # show命令
    parser_show = subparsers.add_parser('show', help='Plot the GPU utilization CSV file')
    parser_show.add_argument('-i', '--input', type=str, required=True, help='Input CSV file path containing GPU utilization data.')
    parser_show.add_argument('-o', '--output', type=str, required=True, help='Output file path to save the plot.')
    parser_show.add_argument('-f', '--force-overwrite', action="store_true", help='Force overwrite the output file if it already exists.')
    parser_show.set_defaults(func=show)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()  # 提示用户需要输入命令