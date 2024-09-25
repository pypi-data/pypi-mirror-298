# tintalib

`tintalib` is a versatile Python package that provides a wide range of tools to apply advanced text styling and color customization in the terminal using ANSI escape sequences. This package supports text effects such as bold, underline, foreground and background colors, and even more advanced styles like blinking, strikethrough, double underline, and rainbow effects. It also includes support for 256-color palettes and 24-bit RGB color customization, making it an excellent choice for enhancing the visual appeal of CLI applications and scripts.

## Features

- **ANSI Text Effects**: Full support for styling text with bold, italic, underline, overline, strikethrough, and more.
- **Color Customization**: Apply both standard and bright colors to text, or use 24-bit RGB values for precise control. Customize both foreground and background colors.
- **256-Color Support**: Easily use terminal-supported 256-color palettes.
- **Advanced Text Effects**: Includes rare styles like double underline, blinking, and overline.
- **Rainbow Effects**: Static and animated rainbow color effects for eye-catching displays.
- **Windows Compatibility**: Enable ANSI escape sequences in Windows terminals (`cmd` and PowerShell) with a simple function.
- **Cross-platform**: Works seamlessly across macOS, Linux, and Windows.

## Color Options

`tintalib` supports an extensive range of color options:

| **Category**         | **Foreground**                  | **Background**                |
|----------------------|---------------------------------|-------------------------------|
| **Standard Colors**   | `Tinta.BLACK`                  | `Tinta.BG_BLACK`              |
|                      | `Tinta.RED`                    | `Tinta.BG_RED`                |
|                      | `Tinta.GREEN`                  | `Tinta.BG_GREEN`              |
|                      | `Tinta.YELLOW`                 | `Tinta.BG_YELLOW`             |
|                      | `Tinta.BLUE`                   | `Tinta.BG_BLUE`               |
|                      | `Tinta.MAGENTA`                | `Tinta.BG_MAGENTA`            |
|                      | `Tinta.CYAN`                   | `Tinta.BG_CYAN`               |
|                      | `Tinta.WHITE`                  | `Tinta.BG_WHITE`              |
| **Bright Colors**     | `Tinta.BRIGHT_BLACK`           | `Tinta.BG_BRIGHT_BLACK`       |
|                      | `Tinta.BRIGHT_RED`             | `Tinta.BG_BRIGHT_RED`         |
|                      | `Tinta.BRIGHT_GREEN`           | `Tinta.BG_BRIGHT_GREEN`       |
|                      | `Tinta.BRIGHT_YELLOW`          | `Tinta.BG_BRIGHT_YELLOW`      |
|                      | `Tinta.BRIGHT_BLUE`            | `Tinta.BG_BRIGHT_BLUE`        |
|                      | `Tinta.BRIGHT_MAGENTA`         | `Tinta.BG_BRIGHT_MAGENTA`     |
|                      | `Tinta.BRIGHT_CYAN`            | `Tinta.BG_BRIGHT_CYAN`        |
|                      | `Tinta.BRIGHT_WHITE`           | `Tinta.BG_BRIGHT_WHITE`       |
| **256-Color Palette** | `Tinta.palette_256(fg=X)`      | `Tinta.palette_256(bg=X)`     |
| **RGB Colors**        | `Tinta.rgb(r, g, b)`           | `Tinta.rgb(r, g, b, is_bg=True)` |



### Example Usage of Colors:

```python
from tintalib import Tinta, colored

# Using standard colors
print(colored("This text is red!", color=Tinta.RED))
print(colored("This text has a green background!", bg_color=Tinta.BG_GREEN))

# Using bright colors
print(colored("This text is bright cyan!", color=Tinta.BRIGHT_CYAN))

# Using 256-color palette
print(colored("Custom 256-color text!", color=Tinta.palette_256(fg=46), bg_color=Tinta.palette_256(bg=160)))

# Using RGB colors
print(colored("This is custom RGB text!", color=Tinta.rgb(255, 100, 100)))
```

## Installation

To install the package, simply use `pip`:

```bash
pip install tintalib
```

## Usage

### Basic Example

Here’s a simple example of how to use `tintalib`'s basic functionality:

```python
from tintalib import Tinta, bold, underline, colored

print(bold("This is bold text"))
print(underline("This is underlined text"))

print(colored("This text is red!", color=Tinta.RED))

print(colored("This text has custom foreground and background colors!", color=Tinta.palette_256(fg=46), bg_color=Tinta.palette_256(bg=160)))
```

### Advanced Usage

#### Using RGB Colors

You can specify exact RGB values for even greater control over your text styling:

```python
from tintalib import Tinta, colored

print(colored("This is red using RGB!", color=Tinta.rgb(255, 0, 0)))

print(colored("This text has a green background!", color=Tinta.WHITE, bg_color=Tinta.rgb(0, 255, 0, is_bg=True)))
```

#### Rainbow Effect

Apply a static rainbow color effect to your text:

```python
from tintalib import rainbow

print(rainbow("This text has a static rainbow effect!"))
```

#### Animated Rainbow Effect

For dynamic CLI applications, you can even create text with animated rainbow effects:

```python
from tintalib import rainbow_animate

rainbow_animate("This is an animated rainbow!", speed=0.2)
```

### Styles and Effects

Here are additional examples of how to apply various styles and effects:

```python
from tintalib import italic, blink, double_underline, overline, strikethrough

print(italic("This text is italicized"))
print(blink("This text is blinking"))
print(double_underline("This text has a double underline"))
print(overline("This text has an overline"))
print(strikethrough("This text is strikethrough"))
```

### Custom Text Styling with Multiple Effects

You can also combine several styles in a single function call:

```python
from tintalib import style_text, Tinta

styled_text = style_text("Styled Text!", color=Tinta.GREEN, styles=[Tinta.BOLD, Tinta.UNDERLINE])
print(styled_text)
```

## Windows Compatibility

By default, Windows terminals (`cmd` and PowerShell) do not natively support ANSI escape sequences. To resolve this, `tintalib` provides a built-in function to enable ANSI sequence support in these environments:

```python
from tintalib import enable_windows_ansi_support

# Enable ANSI support for Windows terminals
enable_windows_ansi_support()
```

Call this function at the beginning of your script to ensure proper rendering of ANSI sequences in Windows environments.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
