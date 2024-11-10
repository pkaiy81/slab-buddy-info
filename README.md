# slab-buddy-info

A Python tool to display Linux kernel slab and buddy allocator information.

## Features

- Parses and displays information from `/proc/slabinfo` and `/proc/buddyinfo`.
- Supports text-based graph display.
- Real-time monitoring with a specified update interval.
- Customizable via command-line arguments.
- Uses standard libraries only (no additional dependencies).

## Installation and Usage

### Run Directly from Git Repository

```bash
git clone https://github.com/pkaiy81/slab-buddy-info.git
cd slab-buddy-info
chmod +x slab-buddy-info  # Ensure the script is executable
./slab-buddy-info [options]
```

### Install via `pip`

You can install the package using `pip` with the `pyproject.toml` setup:

```bash
pip install .
```

Or install from PyPI:

```bash
pip install slab-buddy-info
```

After installation, you can run the tool using:

```bash
slab-buddy-info [options]
```

## Usage

```bash
slab-buddy-info [options]
```

### Options

- `--interval N`: Set the update interval to N seconds for real-time monitoring.
- `--graph`: Generate a graph of the data after execution.
- `--output {text, html}`: Set the output format for the graph ('text' or 'html'). Default is 'text'.
- `--save`: Save the graph to a file instead of displaying it.
- `--filename NAME`: Filename to save the graph (without extension). Default is 'slab_buddy_graph'.
- `--top N`: Specify the top N slabs to display in the graph (default is 10).
- `--show-slab`: Display only slab allocator information.
- `--show-buddy`: Display only buddy allocator information.

### Examples

- **Display both slab and buddy information once and generate a text-based graph**:

  ```bash
  slab-buddy-info --graph
  ```

- **Display slab information, generate an HTML graph, and save it to a file**:

  ```bash
  slab-buddy-info --show-slab --graph --output html --save --filename slab_graph
  ```

- **Display only buddy information, generate a text-based graph, and display it**:

  ```bash
  slab-buddy-info --show-buddy --graph --output text
  ```

- **Display slab information with graph, updating every 5 seconds**:

  ```bash
  slab-buddy-info --show-slab --graph --interval 5
  ```

- **Display only buddy information, updating every 10 seconds**:

  ```bash
  slab-buddy-info --show-buddy --interval 10
  ```

## Development

### Project Structure

```text
slab-buddy-info/
├── slab_buddy_info/
│   ├── __init__.py
│   ├── main.py
│   ├── slabinfo_parser.py
│   ├── buddyinfo_parser.py
│   ├── utils.py
├── slab-buddy-info       # Executable script
├── pyproject.toml
├── README.md
└── LICENSE
```

### Building the Package

To build the package for distribution:

```bash
python3 -m build
```

This will generate distribution files in the `dist/` directory.

### Testing

Before distributing, you can test the installation:

1. **Install in a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install .
   ```

2. **Run the tool**:

   ```bash
   slab-buddy-info --help
   ```

### Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository** on GitHub.

2. **Clone your forked repository**:

   ```bash
   git clone https://github.com/pkaiy81/slab-buddy-info.git
   ```

3. **Create a new branch** for your feature or bugfix:

   ```bash
   git checkout -b feature/new-feature
   ```

4. **Make your changes** and commit them with descriptive messages.

5. **Push to your forked repository**:

   ```bash
   git push origin feature/new-feature
   ```

6. **Open a pull request** on the original repository.

### Reporting Issues

If you encounter any issues or have suggestions, please open an issue on GitHub:

[GitHub Issues](https://github.com/pkaiy81/slab-buddy-info/issues)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Repository

[GitHub - pkaiy81/slab-buddy-info](https://github.com/pkaiy81/slab-buddy-info)

## Acknowledgments

- Thanks to the open-source community for valuable resources and inspiration.
- Inspired by Linux tools like `slabtop` and knowledge of kernel memory management.

## Disclaimer

This tool is intended for educational and informational purposes. Use it at your own risk. Ensure you have the necessary permissions to access system files and be cautious when running it on production systems.
