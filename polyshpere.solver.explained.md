# How does our polysphere solver work?

## The matrix

Our solution is based on Knuth's Algorithm X:
<https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X>, which is an
implementation of the dancing links technique.

A matrix is constructed from the board and the pieces to precompute all
the possible ways each piece can be placed on the board so that we don't
have to repeatedly do it during all the nasty brute forcing!

The universe U for the matrix is N for board w \* h and additional
columns holding w \* h + an ID for each piece. These ID's must be
enumerated starting from w\*h+1

Each row represents how a piece could cover the board

e.g. for a 2x2 board:

\[0,0\]

\[0,0\]

where each cell is represented 1-4 and we have a single piece that
occupies one cell with an ID of 1: \[1\] we would get this matrix:

  --------------------------------------------------------------------------
  -Cells of the                                               -piece IDs-
  board-                                                      
  -------------- -------------- -------------- -------------- --------------
  **1**          **2**          **3**          **4**          **5**

  X                                                           X

                 X                                            X

                                X                             X

                                               X              X
  --------------------------------------------------------------------------

The initial row of numbers 1-6 is our universe U as explained before and
the subsequent rows are options for where we could place our piece
within the matrix.

Furthering this example lets add an L shape piece to the matrix that
looks like this on the 2x2 board:\
\[2,0\]

\[2,2\]

We can add this to the matrix like so

  ------------------------------------------------------------------------
  -Cells of                                       -piece IDs-  
  the board-                                                   
  ----------- ----------- ----------- ----------- ------------ -----------
  **1**       **2**       **3**       **4**       **5**        **6**

  X                                               X            

              X                                   X            

                          X                       X            

                                      X           X            

  X                       X           X                        X
  ------------------------------------------------------------------------

There is only way this piece can be placed on the board so there is only
one row added to the matrix...except we have not accounted for rotating
and flipping! There are 3 other shapes the piece can be transformed
into:

1.  2\. 3.

> \[0,2\] \[2,2\] \[2,2\]
>
> \[2,2\] \[0,2\] \[2,0\]

So lets add these to the matrix too

  ------------------------------------------------------------------------
  -Cells of                                       -piece IDs-  
  the board-                                                   
  ----------- ----------- ----------- ----------- ------------ -----------
  **1**       **2**       **3**       **4**       **5**        **6**

  X                                               X            

              X                                   X            

                          X                       X            

                                      X           X            

  X                       X           X                        X

              X           X           X                        X

  X           X                       X                        X

  X           X           X                                    X
  ------------------------------------------------------------------------

Here's where the brute forcing is required, we need to now look through
the matrix, compare each row with the others so we can identify which
ones completely fill each cell exactly once. Applying this to our matrix
we get four solutions:

  ------------------------------------------------------------------------
  -Cells of                                       -piece IDs-  
  the board-                                                   
  ----------- ----------- ----------- ----------- ------------ -----------
  **1**       **2**       **3**       **4**       **5**        **6**

  X                                               X            

              X                                   X            

                          X                       X            

                                      X           X            

  X                       X           X                        X

              X           X           X                        X

  X           X                       X                        X

  X           X           X                                    X
  ------------------------------------------------------------------------

We can then rebuild the solved boards from this information. This method
minimises the brute forcing required with the precomputed matrix and is
therefore much more efficient.

## Node Objects

In our implementation to represent the matrix, we use node object to
construct a graph. The lowest level of graph components are Node
objects, they have an up, down, left and right field for linking to
other nodes, a value field (self-explanatory) and a column field to
track what column object they are a part of (more on that soon). Here's
a visualisation of a node objects:

> ![A black background with white circles and white text Description
> automatically generated](media/image1.png){width="4.375in"
> height="2.966666666666667in"}
>
> Each connection is first initialised to the object itself.

## Column Objects

Column objects store a head node object, and they have a left and right
for linking to other columns. They also have an ID which tracks our
numerated universe U, and length field for keeping track of how many
nodes link to that column, here is a Visualisation:

![A screenshot of a computer Description automatically
generated](media/image2.png){width="6.268055555555556in"
height="2.892361111111111in"}

It's not very pretty to look at visually, but having this circularly
linked list data structure provides a lot of utility which is useful
during the brute-forcing steps. As you can see columns are circularly
linked, as are the nodes within a column. Column0 is the entry point
when accessing the structure. Root Node, Node 1 and Node 2 in the
diagram are head nodes who don't store a value or keep track of their
column, they just provide a starting point for traversing each column.

You'll also notice that the head nodes aren't connected from left to
right, nodes within columns are only connected in this way when they are
a part of the same piece placement option.

Using a portion of the previous examples, lets again consider the
placement option for this translation of an L piece:

\[2,0\]

\[2,2\]

On a 2x2 board:

\[0,0\]

\[0,0\]

Where that L piece is the only transformation to consider, i.e. this
table representation of the matrix:

  --------------------------------------------------------------------------
  **1**          **2**          **3**          **4**          **5**
  -------------- -------------- -------------- -------------- --------------
  X                             X              X              X

  --------------------------------------------------------------------------

![A black and white diagram Description automatically
generated](media/image3.png){width="11.056944444444444in"
height="2.703472222222222in"}This is the graph representation we would
end up with:

Once again, it looks complex but remember that by precomputing this we
save ourselves a lot of time later. Also, notice how we skipped a node
on column 2 as it's blank, this means our graph is considered sparse as
we only represent cells of the matrix with a value which saves time when
traversing the rows left/right which is useful as most pieces only cover
a small amount of the board.

## Matrix Objects

Matrix objects store a list of columns (what we've just seen), the total
number of columns, the total number of rows and a list that represents a
solution. Which will result in a 2D array representing a solution matrix
table. We have a function *print_packing* to convert a 2D array solution
matrix into the solution board configuration.

## Solving

Once we have the fully constructed matrix, solving the solution is
pretty straightforward with a classic backtracking solution, here's the
pseudo code:

*solutionArr* = \[\]

Solve:

If *matrix*.*columns* only has the root, a solution has been found:

Return solution

*minCol* = shortest column in *matrix*.*columns*

If *minCol.length is 0:*

Return False

Hide all other rows that collide with *minCol*

Remove *minCol* from *matrix*.*columns*

For *row* in *minCol*

Add *row* to *solutionArr*

For each *column* in *row*

Hide all other rows that collide with *column*

> Remove *column* from *matrix*.*columns*

*result =* Solve

If *result* is not False:

Return *solutionArr* formatted as 2D array

Remove *row* from *solutionArr*

For each *column* in *row*

unhide all rows that collide with *column*

> Add *column* back into *matrix*.*columns*

Unhide all rows that collide with *minCol*

Add *minCol* back into *matrix*.*columns*

Return False

## Partial configurations

For solving partial configurations (boards that already have pieces on
them) the solution gets a bit creative, rather than modify the solving
algorithm in anyway, we chose to incorporate everything necessary for
supporting partial configurations into the matrix set up stage in the
solution.

Lets use the following example of a partially configurated board:

\[1,1,0,0\]

\[1,0,0,2\]

\[0,0,2,2\]

With remaining pieces we want to solver for being:

1.  2\.

\[0,3\] \[4,4\]

\[3,3\] \[4,4\]

If the board were empty and none of our, we could create a matrix for
our 2 pieces in the way we have previously done:

  --------------------------------------------------------------------------------------------------------------------------------------
  **1**   **2**   **3**   **4**   **5**   **6**   **7**   **8**   **9**   **10**   **11**   **12**   **13**   **14**   **15**   **16**
  ------- ------- ------- ------- ------- ------- ------- ------- ------- -------- -------- -------- -------- -------- -------- --------
  X       X                       X                                                                  X                          

                                                          X                        X        X                 X                 

  ...     ...     ...     ...     ...     ...     ...     ...     ...     ...      ...      ...      ...      ...      ...      ...
  --------------------------------------------------------------------------------------------------------------------------------------

However, if we were to just pass the pieces that are placed on the board
in standard form into the matrix constructor as is it would generate all
possible transformations of each piece, e.i.:

  --------------------------------------------------------------------------------------------------------------------------------------
  **1**   **2**   **3**   **4**   **5**   **6**   **7**   **8**   **9**   **10**   **11**   **12**   **13**   **14**   **15**   **16**
  ------- ------- ------- ------- ------- ------- ------- ------- ------- -------- -------- -------- -------- -------- -------- --------
  X       X                       X                                                                  X                          

          X       X                       X                                                          X                          

  ...     ...     ...     ...     ...     ...     ...     ...     ...     ...      ...      ...      ...      ...      ...      ...
  --------------------------------------------------------------------------------------------------------------------------------------

And it would generate solutions as though we could move those pieces, so
how do we fix their position? Well we chose the a very simple but
intuitive option, we create a copy of each placed piece that is the size
of the board and tell the constructor that there is only one
transformation for the already piece. So, consider this piece with ID 1
on the board we previously showed:

\[**1**,**1**,0,0\]

\[**1**,0,0,2\]

\[0,0,2,2\]

To fix the pieces position we reconstruct it as so:

\[1,1,0,0\]

\[1,0,0,0\]

\[0,0,0,0\]

We can do the same for piece with ID 2:

\[0,0,0,0\]

\[0,0,0,2\]

\[0,0,2,2\]

We feed these now board size pieced into the matrix as their only
placement options, so we end up with the configurations the solvers
need, e.g.

  --------------------------------------------------------------------------------------------------------------------------------------
  **1**   **2**   **3**   **4**   **5**   **6**   **7**   **8**   **9**   **10**   **11**   **12**   **13**   **14**   **15**   **16**
  ------- ------- ------- ------- ------- ------- ------- ------- ------- -------- -------- -------- -------- -------- -------- --------
  X       X                       X                                                                  X                          

                                                          X                        X        X                 X                 

  ...     ...     ...     ...     ...     ...     ...     ...     ...     ...      ...      ...      ...      ...      ...      ...
  --------------------------------------------------------------------------------------------------------------------------------------

The solver can now only find solutions that include these two rows
meaning it can only find solutions that match our initial partial
configuration!

### Piece ID enumeration

There is one major assumption that the solution I have described so far
makes, and that is that each piece we feed into the matrix will be
appropriately enumerated. The user needs to be able to define a partial
configuration with any number of pieces. E.g. Imagine if there are
pieces with IDs 1,2,3 and 4 for the 4X3 board and they have placed piece
3 and 4. how will the solver know that the ID's of the pieces placed are
and the ID's of the remaining pieces are?

Well... it doesn't, when we feed pieces into the matrix constructor it
assigns ID's sequentially to each piece itself as they need to be
properly enumerated for the solver to function.

So, how do we keep track of where each piece is placed? We simply create
a list that tracks the IDs of the pieces as they were fed in then
convert them back to their original values in the output from the
solver. E.g Piece 3 and 4 are fed in first as they are already placed,
then we feed in the remaining pieces 1 and 2. We create a list so to
track how the pieces are re-numerated that would look like this
\[\[3,1\],\[4,2\],\[1,3\],\[2,4\]\] then use this list to reassign all
the original ID's back in the output.
