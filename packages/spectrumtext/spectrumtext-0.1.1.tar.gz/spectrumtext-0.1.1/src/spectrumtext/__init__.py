from .spectrumtext import SpectrumText
from .printer import Printer
from .exceptions import ColorError
from . import colors

"""
This module initializes the SpectrumText package by importing and exposing its main components.
Modules:
    spectrumtext (module): Contains the SpectrumText class.
    printer (module): Contains the Printer class.
    exceptions (module): Contains custom exceptions, including ColorError.
    colors (module): Provides color-related utilities.
__all__:
    List of public objects of this module, as interpreted by `import *`.
    Includes:
        - SpectrumText: Main class for handling spectrum text operations.
        - Printer: Class for printing text with spectrum colors.
        - ColorError: Custom exception for color-related errors.
        - colors: Module for color utilities.
"""

__all__ = ["SpectrumText", "Printer", "ColorError", "colors"]
