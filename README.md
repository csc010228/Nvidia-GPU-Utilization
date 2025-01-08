# Nvidia GPU Utilization

A Python tool for monitoring NVIDIA GPU utilization and visualizing the results.

## Features

*   Monitor GPU utilization: Collect GPU usage statistics at a configurable interval and duration.
*   Visualize GPU utilization: Generate plots from the collected data for better understanding.

## Installation

1.   Clone the repository:

     ```bash
     git clone https://github.com/csc010228/Nvidia-GPU-Utilization.git
     cd Nvidia-GPU-Utilization
     ```

2.   Ensure Python 3.6+ is installed on your system.

3.   Install required dependencies:

     ```bash
     pip install -r requirements.txt
     ```

## Usage

The tool supports two main commands: `start` and `show`

1.   Start Monitoring (start):

     ```bash
     python main.py start [-i INTERVAL] [-d DURATION] [-o OUTPUT] [-f]
     ```

     Example: 
     
     Monitor GPU utilization every 0.1 seconds for 10 seconds and save results to utilization.csv:

     ``````bash
     python main.py start -i 0.1 -d 10 -o utilization.csv -f
     ``````

2.   Visualize Results (show): 

     ```bash
     python main.py show [-i INPUT] [-o OUTPUT] [-f]
     ```

     Example: 

     Generate a plot from utilization.csv and save it to utilization_plot.png:

     ```bash
     python main.py show -i utilization.csv -o utilization_plot.png -f
     ```

**Help**

To view detailed help for the commands:

```bash
python main.py --help
```



## License

This project is licensed under the MIT License. See the LICENSE file for details.