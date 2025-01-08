import threading
import time
import signal
import sys
from datetime import datetime
from typing import Dict, Any
import pynvml

def log(message):
    """打印带时间戳的消息"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"[{timestamp}] {message}")

class NVGPUMonitor:
    _instance = None  # 存储单例实例

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 确保只初始化一次
        if not hasattr(self, '_initialized'):
            self._initialized = True

            pynvml.nvmlInit()
            self._device_count = pynvml.nvmlDeviceGetCount()
            self._device_handles = []
            for i in range(self._device_count):
                self._device_handles.append(pynvml.nvmlDeviceGetHandleByIndex(i))
            
            self.running = True       # 控制任务运行的标志变量
            self.task_thread = None   # 保存线程对象

            self.utilization = []

    def __del__(self):
        # 确保在对象销毁时释放 NVML 资源
        if hasattr(self, '_initialized'):
            pynvml.nvmlShutdown()

    def start_monitor(self, interval: float = 0.02, show: bool = False):
        """启动定时任务"""
        log("Monitor started. Press Ctrl+C to stop.")
        self.utilization = []
        signal.signal(signal.SIGINT, self.signal_handler)
        # 创建并启动后台线程
        self.task_thread = threading.Thread(
            target=self._scheduled_task,
            kwargs={'interval': interval, "show": show}
        )
        self.task_thread.daemon = True
        self.task_thread.start()

    def get_monitor_result(self):
        return self.utilization

    def wait_until_stop(self):
        while self.running:
            time.sleep(0.1)

    def _scheduled_task(self, interval, show):
        """定时任务的逻辑"""
        while self.running:
            current_utilization = {"Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}
            current_utilization.update(self.sample_utilization(self._device_handles))
            if show:
                print(current_utilization)
            self.utilization.append(current_utilization)
            time.sleep(interval)

    def stop_monitor(self):
        """停止定时任务"""
        self.running = False  # 设置标志变量为 False，通知线程退出
        if self.task_thread:
            self.task_thread.join()  # 等待线程结束
            self.task_thread = None
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            log("Monitor stopped.")

    def signal_handler(self, sig, frame):
        """捕获 Ctrl+C 信号"""
        log("\nCtrl+C detected. Stopping the monitor...")
        self.stop_monitor()

    def sample_utilization(self, device_handles) -> Dict[str, Any]:
        sampled_utilization = {}
        for i, device_handle in enumerate(device_handles):
            device_name = pynvml.nvmlDeviceGetName(device_handle)
            device_utilization = pynvml.nvmlDeviceGetUtilizationRates(device_handle)
            device_gpu_utilization = device_utilization.gpu
            device_memory_utilization = device_utilization.memory
            sampled_utilization[f"GPU {i} {device_name} gpu utilization"] = device_gpu_utilization
            sampled_utilization[f"GPU {i} {device_name} memory utilization"] = device_memory_utilization
        return sampled_utilization