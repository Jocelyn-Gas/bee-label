def rgb_to_hex(r, g, b, a) -> str:
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex_to_rgb(hex: str):
  if hex[0] == '#':
    hex = hex[1:]
  rgb = []
  for i in (0, 2, 4):
    decimal = int(hex[i:i+2], 16)
    rgb.append(decimal)

  return tuple(rgb)
