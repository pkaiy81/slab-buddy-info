**This project is not yet released.**
**To be released soon.**

# slab-buddy-info

A Python tool to display Linux kernel slab and buddy allocator information in a `top`-like interface, with real-time monitoring and interactive time-series graphs.

## Features

- **Real-Time Monitoring**: Displays slab and buddy allocator information in a `top`-like interface with periodic updates.
- **Combined Display**: Shows both slab usage (top N) and buddy info on one screen.
- **Time-Series Graphs**: Generates interactive HTML graphs of slab usage over time after execution.
- **Interactive Filtering**: Allows filtering of slabs in the graph via a dropdown menu (multiple selections allowed).
- **No External Dependencies**: Uses only standard Python libraries and pure JavaScript; no external libraries required.

## Table of Contents

- [Installation](#installation)
  - [Running Directly](#running-directly)
  - [Installation via pip](#installation-via-pip)
- [Usage](#usage)
  - [Command-Line Options](#command-line-options)
  - [Examples](#examples)
- [Generated Graphs](#generated-graphs)
- [Contributing](#contributing)
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

- `--interval N`: Set the update interval to N seconds for real-time monitoring (default is 3 seconds).
- `--top N`: Specify the top N slabs to display (default is 10).
- `--graph`: Generate interactive time-series line graphs after execution.
- `--filename NAME`: Filename to save the graph (without extension). Default is `slab_buddy_graph`.
- `--output html`: Output format for the graph (currently only `html` is supported).
- Press `q` during execution to exit the monitoring interface.

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

- **Sample Graph**:

  ![Sample Graph](TBD)

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or bugfix.
3. **Commit your changes** with clear and descriptive messages.
4. **Push to your fork** and submit a **pull request** to the `develop` branch.

Before submitting, please ensure that:

- Your code follows the project's coding style.
- All existing tests pass, and new tests are added if needed.
- Documentation is updated to reflect your changes.

## License

This project is licensed under the [MIT License](LICENSE).

---

_Note: This project is intended for educational and informational purposes. Please ensure you have the necessary permissions and comply with your organization's policies before running scripts that access system files like `/proc/slabinfo` and `/proc/buddyinfo`._
