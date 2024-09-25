## SpectrumText

SpectrumText is a Python library for adding colorful text output to your terminal applications. It provides an easy-to-use interface for printing text in various colors and styles.

## Features

- Print colored text using hex color codes or RGB values
- Support for background colors
- Rainbow text printing
- Multi-colored text printing
- Error handling for invalid color inputs

## Installation

You can install SpectrumText using pip:

```
pip install spectrumtext
```

## Usage

Here are some basic examples of how to use SpectrumText:

```python
from spectrumtext import Printer
from colors import *

# Print colored text
Printer.print_colored("Hello, World!", "#FF0000")  # Red text
Printer.print_colored("Hello, World!", colors.JADE_GREEN)  # Green text

# Print with background color
Printer.print_colored("Background", (0, 255, 0), background=True)  # Green background

# Print rainbow text
Printer.print_rainbow("Rainbow Text")

# Print multi-colored text
Printer.print_multi_colored(
    "Example Multi Colored 1",
    ("Red", "#FF0000"),
    ("Green", "#00FF00"),
    ("Blue", "#0000FF")
)

Printer.print_multi_colored(
    "Example Multi Colored 2",
    ("I am", colors.JADE_GREEN),
    ("From", colors.YELLOW),
    ("VietNam", colors.RED_ORANGE)
)
```

For more detailed usage instructions and examples, please refer to the documentation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

