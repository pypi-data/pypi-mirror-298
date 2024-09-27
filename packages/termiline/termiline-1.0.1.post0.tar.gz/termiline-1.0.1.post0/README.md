# Termiline: Terminal Text Alignment Utilities

This module offers functions for aligning text in the terminal, making it easier to create visually appealing command-line interfaces. It includes options for centering text horizontally and vertically, as well as right-aligning text.

![Example with the result of centerX and centerY.](https://i.imgur.com/3WyP906_d.webp?maxwidth=1520&fidelity=grand)

### Install

- **Windows:** ```pip install termiline```
- **MacOS/Linux/Unix:** ```pip(3, or python version you are using) install termiline```

## Functions

### `centerX(str, adjust=0)`

Centers text horizontally within the terminal.

- **Parameters:**
  - `str` (str): The text to center.
  - `adjust` (int, optional): Additional spaces for centering adjustment (default is `0`).

- **Returns:** 
  - Centered text as a string.

### `centerY(str, uadjust=0, dadjust=0)`

Centers text vertically in the terminal.

- **Parameters:**
  - `str` (str): The text to center.
  - `uadjust` (int, optional): Spaces above the text (default is `0`).
  - `dadjust` (int, optional): Spaces below the text (default is `0`).

- **Returns:** 
  - Vertically centered text as a string.

### `alignRight(str, ladjust=0)`

Aligns text to the right side of the terminal.

- **Parameters:**
  - `str` (str): The text to align.
  - `ladjust` (int, optional): Additional spaces to the left of the text (default is `0`).

- **Returns:** 
  - Right-aligned text as a string.

## Compatibility

- Python version: 3 and above.

## Troubleshooting

- **Misplacement**: Ensure your string has no extra spaces. For example, use "text" instead of "text     ".

## Usage

To use the functions, import the module in your script:

```python
import termiline

# Example usage
print(termiline.centerX("Horizontally Centered Text"))
print(termiline.centerY("Vertically Centered Text"))
print(termiline.alignRight("Right Aligned Text"))