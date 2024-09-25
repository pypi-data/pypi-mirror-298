import re
from typing import Tuple, Union
from .exceptions import ColorError


class SpectrumText:
    """
    The `SpectrumText` class provides static methods for handling color conversions and applying colors to text in the terminal.
    Methods:
        hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
            Converts a hexadecimal color code to its corresponding RGB values.
        validate_rgb(rgb: Tuple[int, int, int]) -> None:
            Validates if the given RGB values are integers between 0 and 255.
        colored_text(text: str, color: Union[str, Tuple[int, int, int]], background: bool = False) -> str:
            Returns the text with the specified color applied in the terminal. The color can be provided as a string (hex code) or an RGB tuple. An optional background flag can be set to apply the color to the text background.
    """

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """
        The function `hex_to_rgb` converts a hexadecimal color code to its corresponding RGB values.

        :param hex_color: The `hex_color` parameter is a string representing a color in hexadecimal
        format
        :type hex_color: str
        :return: A tuple containing the RGB values converted from the given hexadecimal color code is
        being returned.
        """
        hex_color = hex_color.lstrip("#")
        if not re.match(r"^[0-9A-Fa-f]{6}$", hex_color):
            raise ColorError(f"Invalid hex color code: {hex_color}")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def validate_rgb(rgb: Tuple[int, int, int]) -> None:
        """
        The `validate_rgb` static method in Python checks if RGB values are valid integers between 0 and
        255.

        :param rgb: The `rgb` parameter is a tuple containing three integers representing the red,
        green, and blue values of a color in the RGB color model
        :type rgb: Tuple[int, int, int]
        """
        if not all(isinstance(c, int) and 0 <= c <= 255 for c in rgb):
            raise ColorError(
                f"Invalid RGB values: {rgb}. Each value should be an integer between 0 and 255."
            )

    @staticmethod
    def colored_text(
        text: str, color: Union[str, Tuple[int, int, int]], background: bool = False
    ) -> str:
        """
        This static method `colored_text` in Python takes a text string, a color (either as a string or
        RGB tuple), and an optional background flag to return the text with the specified color in the
        terminal.

        :param text: The `text` parameter is a string that represents the text that you want to colorize
        :type text: str
        :param color: The `color` parameter in the `colored_text` method can be either a string
        representing a color (e.g., "red", "blue") or a tuple of three integers representing the RGB
        values of the color (e.g., (255, 0, 0) for red)
        :type color: Union[str, Tuple[int, int, int]]
        :param background: The `background` parameter in the `colored_text` method is a boolean flag
        that determines whether the specified color should be used for the text background. If
        `background` is set to `True`, the color will be applied to the background of the text. If
        `background` is set to, defaults to False
        :type background: bool (optional)
        :return: The `colored_text` method returns a string with the specified text colored according to
        the provided color and background settings. If there is an error related to the color input, a
        warning message is printed and the default color is used. If there is an unexpected error, an
        error message is printed and the default color is used.
        """
        try:
            if isinstance(color, str):
                if color.startswith("\033"):
                    return f"{color}{text}\033[0m"
                rgb = SpectrumText.hex_to_rgb(color)
            else:
                SpectrumText.validate_rgb(color)
                rgb = color
            color_code = (
                f"\033[{'48' if background else '38'};2;{rgb[0]};{rgb[1]};{rgb[2]}m"
            )
            return f"{color_code}{text}\033[0m"
        except ColorError as e:
            print(f"Warning: {str(e)}. Using default color.")
            return text
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}. Using default color.")
            return text
