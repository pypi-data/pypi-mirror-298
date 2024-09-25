import os, platform, sys, time

class Colors:
    RESET = '\033[0m'
    
    # Estilos básicos
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'
    DOUBLE_UNDERLINE = '\033[21m'
    OVERLINE = '\033[53m'

    # Colores del texto (foreground) estándar
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Colores brillantes (foreground)
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Colores de fondo
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    # Colores de fondo brillantes
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'

    # Función para colores de 256 paleta ANSI
    @staticmethod
    def palette_256(fg=None, bg=None):
        """Devuelve el color ANSI de 256 paletas."""
        result = ""
        if fg is not None:
            result += f"\033[38;5;{fg}m"  # Colores de primer plano (foreground)
        if bg is not None:
            result += f"\033[48;5;{bg}m"  # Colores de fondo (background)
        return result

    # Función para colores RGB (24-bit)
    @staticmethod
    def rgb(r, g, b, is_bg=False):
        """Devuelve el color RGB de 24 bits."""
        return f"\033[{48 if is_bg else 38};2;{r};{g};{b}m"

# Función para habilitar secuencias ANSI en Windows
def enable_windows_ansi_support():
    """Habilita secuencias de escape ANSI en la terminal de Windows (cmd y powershell)."""
    if platform.system() == "Windows":
        from ctypes import windll, byref
        from ctypes.wintypes import DWORD

        # Obtener el manejador para stdout (salida estándar)
        kernel32 = windll.kernel32
        handle = kernel32.GetStdHandle(DWORD(-11))  # STD_OUTPUT_HANDLE = -11

        # Habilitar los códigos ANSI
        mode = DWORD()
        kernel32.GetConsoleMode(handle, byref(mode))
        mode.value |= 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        kernel32.SetConsoleMode(handle, mode)

# Habilitar soporte ANSI en Windows si es necesario
enable_windows_ansi_support()

def colored(text, color=Colors.RESET, bg_color='', style=''):
    """
    Devuelve el texto con el color especificado, color de fondo y estilo.

    Args:
        text (str): El texto a colorear.
        color (str): El color del texto (por defecto es reset).
        bg_color (str): El color del fondo (opcional).
        style (str): El estilo (negrita, subrayado, etc.) (opcional).
    """
    return f"{style}{color}{bg_color}{text}{Colors.RESET}"

# Atajos para los estilos comunes
def bold(text):
    return colored(text, style=Colors.BOLD)

def underline(text):
    return colored(text, style=Colors.UNDERLINE)

def italic(text):
    return colored(text, style=Colors.ITALIC)

def blink(text):
    return colored(text, style=Colors.BLINK)

def strikethrough(text):
    return colored(text, style=Colors.STRIKETHROUGH)

def double_underline(text):
    return colored(text, style=Colors.DOUBLE_UNDERLINE)

def overline(text):
    return colored(text, style=Colors.OVERLINE)

# Función para aplicar varios estilos y colores juntos
def style_text(text, color=Colors.RESET, bg_color='', styles=[]):
    """
    Aplica múltiples estilos y colores a un texto.

    Args:
        text (str): El texto a formatear.
        color (str): El color del texto.
        bg_color (str): El color de fondo.
        styles (list): Lista de estilos a aplicar (opcional).
    
    Returns:
        str: Texto formateado.
    """
    style_code = ''.join(styles)
    return colored(text, color=color, bg_color=bg_color, style=style_code)

# Función de arcoíris para efectos estáticos
def rainbow(text):
    """
    Aplica el efecto arcoíris al texto dado.
    """
    colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
    result = ''
    for i, char in enumerate(text):
        result += colored(char, color=colors[i % len(colors)])
    return result

# Función para animar el efecto arcoíris
def rainbow_animate(text, speed=0.1, reverse=False):
    """
    Aplica el efecto arcoíris animado al texto, cambiando los colores dinámicamente.

    Args:
        text (str): El texto a animar.
        speed (float): Velocidad del cambio de color (segundos).
        reverse (bool): Determina si la animación va en dirección inversa.
    """
    colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
    
    try:
        while True:
            for i in range(len(colors)):
                if reverse:
                    result = ''.join(colored(char, color=colors[(i - j) % len(colors)]) for j, char in enumerate(text))
                else:
                    result = ''.join(colored(char, color=colors[(i + j) % len(colors)]) for j, char in enumerate(text))
                sys.stdout.write(f'\r{result}')
                sys.stdout.flush()
                time.sleep(speed)
    except KeyboardInterrupt:
        pass  # Captura la interrupción y no hace nada, simplemente termina

def disable_colors():
    """Deshabilita los colores si la terminal no los soporta."""
    global Colors
    Colors.RESET = ''
    Colors.BOLD = ''
    Colors.UNDERLINE = ''
    # Continua eliminando el resto de los estilos y colores si es necesario
