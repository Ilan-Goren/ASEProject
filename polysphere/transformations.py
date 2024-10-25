def rotate_90(shape):
    """Rotate the polyomino 90 degrees clockwise."""
    return [(-y, x) for x, y in shape]


def rotate_180(shape):
    """Rotate the polyomino 180 degrees."""
    return [(-x, -y) for x, y in shape]


def rotate_270(shape):
    """Rotate the polyomino 270 degrees clockwise (or 90 degrees counterclockwise)."""
    return [(y, -x) for x, y in shape]


def flip_horizontal(shape):
    """Flip the polyomino horizontally."""
    return [(-x, y) for x, y in shape]


def flip_vertical(shape):
    """Flip the polyomino vertically."""
    return [(x, -y) for x, y in shape]


def generate_transformations(shape):
    """Generate all unique transformations (rotations and flips) of a polyomino."""
    transformations = set()

    # Generate all rotations
    orientations = [
        shape,
        rotate_90(shape),
        rotate_180(shape),
        rotate_270(shape),
    ]

    # Add flipped versions of all rotations
    for orientation in orientations:
        transformations.add(tuple(orientation))  # Add original rotation
        transformations.add(tuple(flip_horizontal(orientation)))  # Add horizontally flipped
        transformations.add(tuple(flip_vertical(orientation)))  # Add vertically flipped
    return [list(t) for t in transformations]  # Return as a list of lists