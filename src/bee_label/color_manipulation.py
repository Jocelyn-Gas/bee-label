from PIL import ImageColor


def rgb_to_hex(r, g, b) -> str:
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return "#{:02x}{:02x}{:02x}".format(r, g, b).upper()


def hex_to_rgb(hex):
    hex = hex.lstrip("#")

    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i : i + 2], 16)
        rgb.append(decimal)

    return tuple(value / 255.0 for value in rgb)


def srgb_to_linear_rgb(c):
    if c < 0:
        return 0
    elif c < 0.04045:
        return c / 12.92
    else:
        return ((c + 0.055) / 1.055) ** 2.4


def hex_to_rgb_gamma(hex: str, alpha=1):
    hex = hex.lstrip("#")
    hex_value = int(hex, 16)
    r = (hex_value & 0xFF0000) >> 16
    g = (hex_value & 0x00FF00) >> 8
    b = hex_value & 0x0000FF
    return tuple([srgb_to_linear_rgb(c / 0xFF) for c in (r, g, b)] + [alpha])
