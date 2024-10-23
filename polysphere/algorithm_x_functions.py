class Node:
    def __init__(self, col=None, value=0):
        self.up = self.down = self.left = self.right = self
        self.col = col
        self.value = value


class Column:
    def __init__(self, id):
        self.left = self.right = self
        self.head = Node(self)
        self.length = 0
        self.id = id


class Matrix:
    def __init__(self, primary, secondary):
        num_cols = primary + secondary
        self.columns = [Column(i) for i in range(num_cols + 1)]  # columns[0] is root node
        self.num_cols = num_cols
        self.num_rows = 0
        self.sol = []

        # root node setup
        self.columns[0].head.down = self.columns[0].head
        self.columns[0].head.up = self.columns[0].head
        self.columns[0].right = self.columns[1]
        self.columns[0].left = self.columns[primary]

        # initialize primary columns
        for i in range(1, primary + 1):
            self.columns[i].left = self.columns[i - 1]
            self.columns[i].right = self.columns[(i + 1) % (primary + 1)]
            self.columns[i].head.down = self.columns[i].head
            self.columns[i].head.up = self.columns[i].head

        # initialize secondary columns (not linked into header row)
        for i in range(primary + 1, num_cols + 1):
            self.columns[i].left = self.columns[i]
            self.columns[i].right = self.columns[i]
            self.columns[i].head.down = self.columns[i].head
            self.columns[i].head.up = self.columns[i].head


def add_row(matrix, indices):
    """Appends the sparse row indices to the matrix."""
    # input verification
    last = -1
    for element in indices:
        if element <= 0 or element > matrix.num_cols:
            raise ValueError("Index out of range.")
        if element <= last:
            raise ValueError("Indices not ordered")
        last = element

    matrix.num_rows += 1

    # Add new nodes to columns
    for e in indices:
        current = Node(col=matrix.columns[e], value=matrix.num_rows)
        current.down = matrix.columns[e].head
        current.up = matrix.columns[e].head.up

        matrix.columns[e].head.up.down = current
        matrix.columns[e].head.up = current

        matrix.columns[e].length += 1

    # Link new nodes left-right
    for i, e in enumerate(indices):
        matrix.columns[e].head.up.right = matrix.columns[indices[(i + 1) % len(indices)]].head.up
        matrix.columns[indices[(i + 1) % len(indices)]].head.up.left = matrix.columns[e].head.up


def cover(c):
    """Removes `c` from the selection and removes all colliding rows."""
    # hide colliding rows
    p = c.head.down
    while p != c.head:
        hide(p)
        p = p.down

    # remove from header list
    c.left.right = c.right
    c.right.left = c.left


def hide(p):
    """Hide the row from the matrix."""
    q = p.right
    while q != p:
        q.up.down = q.down
        q.down.up = q.up
        q.col.length -= 1
        q = q.right


def uncover(c):
    """Undoes the deletion done by `cover(c)`."""
    # add to header list
    c.left.right = c
    c.right.left = c

    # unhide colliding rows
    p = c.head.up
    while p != c.head:
        unhide(p)
        p = p.up


def unhide(p):
    """Unhide the row in the matrix."""
    q = p.left
    while q != p:
        q.up.down = q
        q.down.up = q
        q.col.length += 1
        q = q.left


def mrv(matrix):
    """Uses Knuth's MRV heuristic to choose the column with the fewest rows."""
    min_len = -1
    min_col = None

    # Check for the column with the smallest length
    c = matrix.columns[0].right
    while c != matrix.columns[0]:
        if c.length < min_len or min_len == -1:
            min_len = c.length
            min_col = c
        c = c.right

    return min_col

def solve(matrix, collector, first):
    """Backtracking search using the matrix data structure with MRV heuristic."""
    # Problem is solved
    if matrix.columns[0].left == matrix.columns[0]:
        #solution = [e.value for e in matrix.sol]
        rows = [[False] * matrix.num_cols for _ in range(len(matrix.sol))]

        for i, e in enumerate(matrix.sol):
            rows[i][e.col.id - 1] = True
            n = e.right
            while n != e:
                rows[i][n.col.id - 1] = True
                n = n.right

        collector.append(rows)
        #sol_copy = copy.deepcopy(matrix.sol)
        #collector.append(sol_copy)
        #return matrix.sol
        return rows

    # MRV heuristic
    col = mrv(matrix)
    if col.length == 0:
        return None

    cover(col)

    # Classic backtracking algorithm
    r = col.head.down
    while r != col.head:
        # Add r to solution
        matrix.sol.append(r)

        # Cover r
        n = r.right
        while n != r:
            cover(n.col)
            n = n.right

        result = solve(matrix, collector, first)

        if first and result is not None:
            return result

        # Remove r from solution
        undo = matrix.sol.pop()
        col = undo.col

        # Uncover r
        n = undo.left
        while n != undo:
            uncover(n.col)
            n = n.left

        r = r.down

    uncover(col)
    return None


def find_first(matrix):
    """Find one solution to the exact cover problem."""
    collector = []
    solve(matrix, collector, True)

    if len(collector) == 0:
        print("Error: No solution found.")
        return None
    return collector[0]


def find_rows(matrix):
    """Find one solution and return the options represented by their row id and content."""
    sol = solve(matrix, [], True)
    return sol


def find_all(matrix):
    """Find all solutions to the exact cover problem."""
    coll = []
    solve(matrix, coll, False)
    return coll


def pretty_print(matrix):
    """Print a non-sparse table representation of the matrix for debugging."""
    elements = [[False] * matrix.num_cols for _ in range(matrix.num_rows)]

    for i in range(1, matrix.num_cols + 1):
        h = matrix.columns[i]
        e = h.head.down
        while e != h.head:
            elements[e.value - 1][i - 1] = True
            e = e.down

    num_primary = 0
    c = matrix.columns[0].right
    while c != matrix.columns[0]:
        num_primary += 1
        c = c.right

    for x in range(1, matrix.num_rows + 1):
        print("|", end="")
        for y in range(1, matrix.num_cols + 1):
            if elements[x - 1][y - 1]:
                print("X|", end="")
            else:
                print(" |", end="")
            if y == num_primary:
                print("|", end="")
        print("")


def force_option(matrix, col_id, value):
    """Ensure a specific option (row) is included in all solutions."""
    col = matrix.columns[col_id]

    # Collect columns covered by forced option
    columns = [col]

    r = col.head.down
    while r != col.head:
        if r.value == value:
            # Add r to solution
            matrix.sol.append(r)

            n = r.right
            while n != r:
                columns.append(n.col)
                n = n.right

            # Cover r
            for e in columns:
                cover(e)

            break

        r = r.down