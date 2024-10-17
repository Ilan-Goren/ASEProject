def rotate_right(bitmap, width, height):
    """Rotate a rectangular bitmap 90 degrees clockwise."""
    new_bitmap = 0
    for row in range(height):
        for col in range(width):
            # Move the bit at (row, col) to (col, height - row - 1) in the rotated bitmap
            if bitmap & (1 << (row * width + col)):
                new_bitmap |= 1 << (col * height + (height - row - 1))
    return new_bitmap

def rotate_left(bitmap, width, height):
    """Rotate a rectangular bitmap 90 degrees counterclockwise."""
    new_bitmap = 0
    for row in range(height):
        for col in range(width):
            # Move the bit at (row, col) to (width - col - 1, row) in the rotated bitmap
            if bitmap & (1 << (row * width + col)):
                new_bitmap |= 1 << ((width - col - 1) * height + row)
    return new_bitmap

def rotate_180(bitmap, width, height):
    """Rotate a rectangular bitmap 180 degrees."""
    new_bitmap = 0
    for row in range(height):
        for col in range(width):
            # Invert both row and column
            if bitmap & (1 << (row * width + col)):
                new_bitmap |= 1 << ((height - row - 1) * width + (width - col - 1))
    return new_bitmap

def flip_horizontal(bitmap, width, height):
    """Flip a rectangular bitmap horizontally."""
    new_bitmap = 0
    for row in range(height):
        for col in range(width):
            if bitmap & (1 << (row * width + col)):
                # Flip horizontally (reverse the column position)
                new_bitmap |= 1 << (row * width + (width - col - 1))
    return new_bitmap

def flip_vertical(bitmap, width, height):
    """Flip a rectangular bitmap vertically."""
    new_bitmap = 0
    for row in range(height):
        for col in range(width):
            if bitmap & (1 << (row * width + col)):
                # Flip vertically (reverse the row position)
                new_bitmap |= 1 << ((height - row - 1) * width + col)
    return new_bitmap


def generate_transformations(piece_bitmap, width, height):
    """Generate all unique rotations and flips of a polyomino represented by its bitmap."""
    transformations = set()

    # Add the original bitmap
    transformations.add((int(str(piece_bitmap),2), width, height))
    print("original: " + str(piece_bitmap))

    # Rotate 90 degrees clockwise
    rotated_right = rotate_right(piece_bitmap, width, height)
    transformations.add((rotated_right, height, width))  # width and height swap
    print("90cw: " + "{0:b}".format(rotated_right))

    # Rotate 180 degrees
    rotated_180 = rotate_180(piece_bitmap, width, height)
    transformations.add((rotated_180, width, height))
    print("180: " + "{0:b}".format(rotated_180))

    # Rotate 90 degrees counterclockwise
    rotated_left = rotate_left(piece_bitmap, width, height)
    transformations.add((rotated_left, height, width))  # Width and height swap
    print("90ccw: " + "{0:b}".format(rotated_left))

    # Flip horizontally
    flipped_horiz = flip_horizontal(piece_bitmap, width, height)
    transformations.add((flipped_horiz, width, height))
    print("hf: " + "{0:b}".format(flipped_horiz))

    # Flip vertically
    flipped_vert = flip_vertical(piece_bitmap, width, height)
    transformations.add((flipped_vert, width, height))
    print("vf: " + "{0:b}".format(flipped_vert))

    return list(transformations)