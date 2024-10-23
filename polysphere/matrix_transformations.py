from . import matrix_polyominoes

def rotate90(p):
    """Rotates a polyomino 90 degrees clockwise."""
    h = len(p.tiles)
    w = len(p.tiles[0])

    # Create an empty array for the rotated tiles
    tiles = [[False for _ in range(h)] for _ in range(w)]

    # Perform the rotation
    for i in range(h):
        for j in range(w):
            tiles[j][h - i - 1] = p.tiles[i][j]

    p.tiles = tiles


def equals(p, q):
    """Checks if two polyominoes are equal."""
    if len(p.tiles) != len(q.tiles) or len(p.tiles[0]) != len(q.tiles[0]):
        return False

    for i in range(len(p.tiles)):
        for j in range(len(p.tiles[0])):
            if p.tiles[i][j] != q.tiles[i][j]:
                return False

    return True


def contains(polys, p):
    """Checks if the polyomino vector contains the polyomino p."""
    for e in polys:
        if equals(e, p):
            return True
    return False


def rotate_polyomino(p, d):
    """
    Returns the polyomino `p` rotated `d` times:
    - For 0 <= d <= 3, rotate `p` by 90 degrees clockwise `d` times.
    - For 4 <= d <= 7, mirror `p` horizontally and rotate `(d - 4)` times.
    """
    d = d % 8
    p_new = matrix_polyominoes.Polyomino([row[:] for row in p.tiles],p.poly_id)  # Deep copy of the tiles

    if d >= 4:
        # Mirror the polyomino horizontally
        mirrored_tiles = [row[::-1] for row in p_new.tiles]  # Reverse each row
        p_new.tiles = mirrored_tiles
        d = d - 4

    # Rotate the polyomino `d` times by 90 degrees clockwise
    for _ in range(d):
        rotate90(p_new)

    return p_new

def unique_rotations(coll, p):
    """Returns up to 8 unique possibilities from rotation and flipping."""
    rotations = []
    for i in range(8):
        q = rotate_polyomino(p, i)
        if not contains(rotations, q):
            rotations.append(q)

    coll.extend(rotations)

