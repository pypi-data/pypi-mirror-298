from typing import List, Tuple, Union
from .spectrumtext import SpectrumText
from .exceptions import ColorError

ColorInput = Union[str, Tuple[str, Union[str, Tuple[int, int, int]]]]


class Printer:
    """
    The `Printer` class provides static methods for printing text with various color formatting options.
    It includes methods for printing colored text, rainbow-colored text, and multi-colored text, with
    error handling for color-related exceptions.
    Methods:
        - print_colored(text: str, color: Union[str, Tuple[int, int, int]], background: bool = False) -> None:
            Prints colored text with the specified color and optional background color.
        - print_rainbow(text: str) -> None:
            Prints text in rainbow colors using a predefined list of colors.
        - print_multi_colored(*args: ColorInput) -> None:
            Prints multiple pieces of colored text using the `format_multi_colored` method.
        - format_multi_colored(*args: ColorInput) -> str:
            Formats multiple pieces of text with different colors and returns the formatted string.
    """

    @staticmethod
    def print_colored(
        text: str, color: Union[str, Tuple[int, int, int]], background: bool = False
    ) -> None:
        """
        The `print_colored` static method prints colored text with error handling for color-related
        exceptions.

        :param text: The `text` parameter is a string that represents the text that you want to print
        with color
        :type text: str
        :param color: The `color` parameter in the `print_colored` method can be either a string
        representing a color name (e.g., "red", "blue", "green") or a tuple of three integers
        representing the RGB values of the desired color (e.g., (255, 0,
        :type color: Union[str, Tuple[int, int, int]]
        :param background: The `background` parameter in the `print_colored` method is a boolean flag
        that determines whether the specified color should be used as the text color or the background
        color when printing the text. If `background` is set to `True`, the specified color will be used
        as the background color for, defaults to False
        :type background: bool (optional)
        """
        try:
            print(SpectrumText.colored_text(text, color, background))
        except ColorError as e:
            print(f"Warning: {str(e)}. Printing without color.")
            print(text)
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}. Printing without color.")
            print(text)

    @staticmethod
    def print_rainbow(text: str) -> None:
        """
        The `print_rainbow` static method prints text in rainbow colors using a predefined list of
        colors.

        :param text: The `text` parameter is a string that represents the text for which you want to
        print in rainbow colors
        :type text: str
        """
        rainbow_colors = [
            "#FF0000",
            "#FF7F00",
            "#FFFF00",
            "#00FF00",
            "#0000FF",
            "#8B00FF",
        ]
        for i, char in enumerate(text):
            color = rainbow_colors[i % len(rainbow_colors)]
            print(SpectrumText.colored_text(char, color), end="")
        print()

    @staticmethod
    def print_multi_colored(*args: ColorInput) -> None:
        """
        The function `print_multi_colored` prints multiple colored text using the `format_multi_colored`
        method.

        :param : It looks like the code snippet defines a static method named `print_multi_colored`
        within a class. This method takes variable arguments of type `ColorInput` and returns `None`.
        The method calls another method named `format_multi_colored` from a class named `Printer` to
        format and print
        :type : ColorInput
        """
        print(Printer.format_multi_colored(*args))

    @staticmethod
    def format_multi_colored(*args: ColorInput) -> str:
        """
        This static method in Python formats multiple pieces of text with different colors and handles
        errors gracefully.

        :param : This static method `format_multi_colored` takes in variable arguments of type
        `ColorInput` and returns a formatted string with colored text. The method iterates through the
        arguments, where each argument can be a single value or a tuple containing text and color. If a
        tuple is provided, the text
        :type : ColorInput
        :return: A string is being returned by the `format_multi_colored` method. The method takes in
        variable arguments of type `ColorInput`, processes each argument to extract text and color
        information, and then formats the text with the specified color using the
        `SpectrumText.colored_text` method. If any errors occur during the processing, a warning message
        is printed and the text is added to the result with
        """
        result = []
        default_color = "\033[0m"  # Default to reset color
        for arg in args:
            if isinstance(arg, tuple):
                text, color = arg
            else:
                text, color = arg, default_color
            try:
                result.append(SpectrumText.colored_text(str(text), color))
            except ColorError as e:
                print(f"Warning: {str(e)}. Using default color for '{text}'.")
                result.append(str(text))
            except Exception as e:
                print(
                    f"An unexpected error occurred: {str(e)}. Using default color for '{text}'."
                )
                result.append(str(text))
        return " ".join(result)
