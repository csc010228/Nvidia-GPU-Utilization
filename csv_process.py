import csv
from typing import List, Dict, Any
import traceback

def map_list_to_csv(map_list: List[Dict[str, any]], filepath: str) -> bool:
    """
    将一个由map组成的list输出成csv文件

    Args:
        map_list (List[Dict[str, any]]): 由map组成的list
        filepath (str): 要输出的csv文件路径

    Returns:
        bool: 输出是否成功
    """
    if not map_list:
        print("Error: map_list is empty.")
        return False

    try:
        fieldnames = map_list[0].keys()
        with open(filepath, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(map_list)
        return True
    except Exception as e:
        print(f"Error while writing to CSV: {e}")
        traceback.print_exc()
        return False

def csv_to_map_list(filepath: str) -> List[Dict[str, str]]:
    """
    将csv文件读取成一个由map组成的list

    Args:
        filepath (str): csv文件路径

    Returns:
        List[Dict[str, str]]: 返回的由map组成的list, 失败返回None
    """
    try:
        with open(filepath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            map_list = [dict(row) for row in reader]
        return map_list
    except Exception as e:
        print(f"Error while reading CSV: {e}")
        traceback.print_exc()
        return None