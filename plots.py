import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def plot_time_series(data, output_path, title, xlabel, ylabel, start_time, end_time):
    """
    绘制带时间轴的折线图，并添加平均值虚线，时间轴精确到毫秒。

    Parameters:
        data (list): 数据列表，用于绘制折线图。
        start_time (str): 横轴起始时间，格式为 '%Y-%m-%d %H:%M:%S.%f'。
        end_time (str): 横轴结束时间，格式为 '%Y-%m-%d %H:%M:%S.%f'。
        output_path (str): 图像保存路径。
    """
    # 将字符串解析为 datetime 对象
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')

    # 计算时间间隔
    time_interval = (end_time - start_time) / (len(data) - 1)

    # 生成时间序列作为横轴
    time_intervals = [start_time + i * time_interval for i in range(len(data))]

    # 计算平均值
    mean_value = sum(data) / len(data)

    # 绘制折线图，设置线条宽度为 1
    plt.plot(time_intervals, data, color='blue', linewidth=1, label='Data')

    # 绘制红色虚线，表示平均值
    plt.axhline(y=mean_value, color='red', linestyle='--', label=f'Average ({mean_value:.2f})')

    # 设置时间格式化精确到毫秒
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))  # 时间格式到毫秒

    # 只显示起始和结束时间
    plt.gca().set_xticks([time_intervals[0], time_intervals[-1]])  # 设置刻度为两端时间点

    # 添加标题和标签
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # 显示图例
    plt.legend()

    # 保存图像
    plt.savefig(output_path, dpi=300, bbox_inches='tight')  # 保存图像

    # 清理绘图对象
    plt.close()