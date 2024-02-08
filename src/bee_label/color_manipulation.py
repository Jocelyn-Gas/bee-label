def rgb_to_hex(r, g, b, a) -> str:
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex_to_rgb( hex: str ) -> tuple[float, float, float]:
    if hex[0] == '#':
      hex = hex[1:]
    hex_value = int(hex, 16)
    b = (hex_value & 0xFF) / 255.0
    g = ((hex_value >> 8) & 0xFF) / 255.0
    r = ((hex_value >> 16) & 0xFF) / 255.0

    return r, g, b
