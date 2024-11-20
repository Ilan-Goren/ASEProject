export const pieces  = { 
  1: [[0, 0, 0], [0, 2, 0], [0, 4, 0], [2, 0, 0], [2, 4, 0]],
  2: [[0, 0, 0], [0, 2, 0], [2, 2, 0], [2, 2, 0], [2, 4, 0]],
  3: [[0, 0, 0], [0, 2, 0], [2, 2, 0], [2, 4, 0], [4, 2, 0]],
  4: [[0, 0, 0], [0, 2, 0], [0, 4, 0], [2, 2, 0]],
  5: [[0, 0, 0], [0, 2, 0], [0, 4, 0], [0, 6, 0], [2, 2, 0]],
  6: [[0, 0, 0], [0, 2, 0], [0, 4, 0], [2, 0, 0], [2, 2, 0]],
  7: [[0, 0, 0], [2, 0, 0], [2, 2, 0], [4, 2, 0]],
  8: [[0, 0, 0], [0, 2, 0], [0, 4, 0], [2, 0, 0]],
  9: [[0, 0, 0], [0, 2, 0], [0, 4, 0], [2, 0, 0], [4, 0, 0]],
  10: [[0, 0, 0], [0, 2, 0], [0, 4, 0], [0, 6, 0], [2, 0, 0]],
  11: [[0, 0, 0], [0, 2, 0], [2, 0, 0]],
  12: [[0, 0, 0], [0, 2, 0], [2, 2, 0], [2, 4, 0], [4, 4, 0]]
};

// Define color mapping
export const colorMapping = {
  '1': 0xff0000, // Red
  '2': 0x00ff00, // Green
  '3': 0x0000ff, // Blue
  '4': 0xffff00, // Yellow
  '5': 0xff00ff, // Magenta
  '6': 0x00ffff, // Cyan
  '7': 0xffa500, // Orange
  '8': 0x8a2be2, // Blue Violet
  '9': 0x00ff7f, // Spring Green
  '10': 0xdc143c, // Crimson
  '11': 0x4682b4, // Steel Blue
  '12': 0xdda0dd, // Plum
};