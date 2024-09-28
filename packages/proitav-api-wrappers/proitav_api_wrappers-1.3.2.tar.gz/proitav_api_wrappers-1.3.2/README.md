# ProITAV API Wrappers

A collection of API wrappers for ProITAV products.

## Installation

You can install this package directly from PyPI:

```bash
pip install proitav-api-wrappers
```

For the latest development version, you can install directly from GitHub:

```bash
pip install git+https://github.com/yourusername/proitav-api-wrappers.git
```

## Usage

Here's an example of how to import and use a wrapper:

```python
from proitav_api_wrappers import IP5100

# Create an instance of the IP5100 wrapper
ip5100 = IP5100('192.168.1.100')

# Use the wrapper methods
ip5100.connect()
ip5100.get_device_info()
```

## Available Wrappers

- IP5100
- CAM600
- AMP120
- SW0401_N081_000
- MV0401_H2H4K60
- SC010
- SC009
- MS0402_N011
- FSC640
- (Add other wrappers as needed)

## Development

To set up the project for development:

1. Clone the repository:

   ```bash
   git clone https://github.com/JFaulk1434/proitav-api-wrappers.git
   cd proitav-api-wrappers
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package in editable mode with development dependencies:

   ```bash
   pip install -e .[dev]
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.
