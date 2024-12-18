# slab-buddy-info

A Python tool to display Linux kernel slab and buddy allocator information in a `top`-like interface, with real-time monitoring and interactive time-series graphs.

## Features

- **Real-Time Monitoring**: Displays slab and buddy allocator information in a `top`-like interface with periodic updates.
- **Combined Display**: Shows both slab usage (top N) and buddy info on one screen.
- **Time-Series Graphs**: Generates interactive HTML graphs of slab usage over time after execution.
- **Interactive Filtering**: Allows filtering of slabs in the graph via a dropdown menu (multiple selections allowed).
- **No External Dependencies**: Uses only standard Python libraries and pure JavaScript; no external libraries required.
- **Immediate Exit**: Press `q` during execution to exit the monitoring interface immediately.
- **Data Collection Mode**: Use the `--count` option to specify the number of data collections without displaying the UI.
- **Output Format Enforcement**: When using the `--output` option, the `--graph` option becomes mandatory.

## Table of Contents

- [Installation](#installation)
  - [Running Directly](#running-directly)
  - [Installation via pip](#installation-via-pip)
- [Usage](#usage)
  - [Command-Line Options](#command-line-options)
  - [Examples](#examples)
- [Generated Graphs](#generated-graphs)
- [License](#license)
- [Author](#author)

## Installation

### Running Directly

You can run the script directly without installing it:

```bash
git clone https://github.com/pkaiy81/slab-buddy-info.git
cd slab-buddy-info
chmod +x slab-buddy-info  # Ensure the script is executable
sudo ./slab-buddy-info [options]
```

**Note**: Accessing `/proc/slabinfo` and `/proc/buddyinfo` may require root privileges. Use `sudo` as needed.

### Installation via pip

You can install the package using `pip`:

```bash
pip install .
```

After installation, you can run the tool using:

```bash
sudo slab-buddy-info [options]
```

## Usage

```bash
sudo ./slab-buddy-info [options]
```

### Command-Line Options

- `--interval N`:  
  Set the update interval to N seconds for real-time monitoring (default is 3 seconds).

- `--top N`:  
  Specify the top N slabs to display (default is 10).

- `--graph`:  
  Generate interactive time-series line graphs after execution.

- `--filename NAME`:  
  Filename to save the graph (without extension). Default is `slab_buddy_graph`.

- `--output html`:  
  Output format for the graph (currently only `html` is supported).  
  **Requires** `--graph` option.

- `--count N`:  
  Set the number of data collections. If specified, the program runs in count mode without displaying the UI.

- Press `q` during execution to exit the monitoring interface immediately.

### Examples

- **Display slab and buddy information with default settings**:

  ```bash
  sudo ./slab-buddy-info
  ```

- **Set update interval to 2 seconds and display top 15 slabs**:

  ```bash
  sudo ./slab-buddy-info --interval 2 --top 15
  ```

- **Generate time-series graphs after monitoring**:

  ```bash
  sudo ./slab-buddy-info --graph
  ```

- **Specify a custom filename for the generated graph**:

  ```bash
  sudo ./slab-buddy-info --graph --filename my_slab_graph
  ```

- **Collect data 10 times without displaying the UI and generate a graph**:

  ```bash
  sudo ./slab-buddy-info --count 10 --graph
  ```

- **Collect data 20 times without displaying the UI and save the graph with a custom filename**:

  ```bash
  sudo ./slab-buddy-info --count 20 --graph --filename my_custom_graph
  ```

- **Using the `--output` option (requires `--graph`)**:

  ```bash
  sudo ./slab-buddy-info --graph --output html
  ```

  **Incorrect Usage** (will result in an error):

  ```bash
  sudo ./slab-buddy-info --output html
  ```

## Generated Graphs

When the `--graph` option is used, the script generates an interactive HTML file containing time-series graphs of slab usage.

- **Opening the Graph**:

  - After execution, open the generated HTML file (e.g., `slab_buddy_graph.html`) in a modern web browser.

- **Features of the Graph**:

  - **Interactive Filtering**: Use the dropdown menu to select which slabs to display on the graph.
  - **Time-Series Visualization**: The graph displays memory usage over time for the selected slabs.
  - **Axes and Labels**: The X-axis represents time, and the Y-axis represents memory usage in bytes.
  - **Grid Lines**: Horizontal and vertical grid lines improve readability.
  - **Legend**: A legend indicates which color corresponds to each slab.

## License

This project is licensed under the [MIT License](LICENSE).

---

_Note: This project is intended for educational and informational purposes. Please ensure you have the necessary permissions and comply with your organization's policies before running scripts that access system files like `/proc/slabinfo` and `/proc/buddyinfo`._
