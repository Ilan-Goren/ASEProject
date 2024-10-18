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

    # Add all rotations of the original piece
    current_bitmap = piece_bitmap
    for _ in range(4):
        transformations.add((current_bitmap, width, height))
        # Rotate 90 degrees clockwise
        current_bitmap = rotate_right(current_bitmap, width, height)
        width, height = height, width  # Swap width and height after each 90-degree rotation

    # Flip the piece horizontally
    flipped_bitmap = flip_horizontal(piece_bitmap, width, height)

    # Add all rotations of the horizontally flipped piece
    for _ in range(4):
        transformations.add((flipped_bitmap, width, height))
        # Rotate 90 degrees clockwise
        flipped_bitmap = rotate_right(flipped_bitmap, width, height)
        width, height = height, width  # Swap width and height after each 90-degree rotation

    return list(transformations)

def list_to_bitmap(piece_bitmap, width):
    """Convert a 2D list (with leading zeros) to an integer bitmap, respecting row width."""
    bitmap = 0
    for row in piece_bitmap:
        # Convert each row to an integer with correct width (leading zeros)
        row_bitmap = 0
        for cell in row:
            row_bitmap = (row_bitmap << 1) | cell
        # Shift the row into the correct position in the overall bitmap
        bitmap = (bitmap << width) | row_bitmap
    return bitmap


def bitmap_to_list(bitmap, width, height):
    """Convert an integer bitmap back into a 2D list with the given width and height."""
    piece_list = []

    # Iterate over each row (from bottom to top, since we're reading bits left-to-right)
    for row in range(height):
        row_list = []
        # Extract each bit in the row by shifting the appropriate number of times
        for col in range(width):
            # The bit we're interested in is at the position (row * width + col)
            bit_position = (height - row - 1) * width + (width - col - 1)
            row_list.insert(0, (bitmap >> bit_position) & 1)
        piece_list.append(row_list)

    return piece_list