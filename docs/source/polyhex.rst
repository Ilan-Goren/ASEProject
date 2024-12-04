Polyhex Application Documentation
==================================

This documentation provides an overview of the Polyhex application, its class structure, and views.

Content
-------

1. Polyhex Views
2. Polyhex Main
3. Polyhex Board
4. Polyhex Piece
5. Polyhex Solver

Polyhex Main
--------------

The `Polyhex` class handles the core functionality of the application. It includes the logic for solving the Polyhex puzzle and managing the state of the puzzle board.

.. autoclass:: polyhex.polyhex.Polyhex_Solver
   :members:
   :undoc-members:
   :show-inheritance:

Polyhex Views
-------------

The views in this module handle the HTTP requests for rendering different parts of the Polyhex application, such as the puzzle board and solution generator.

.. automodule:: polyhex.views
   :members:
   :undoc-members:
   :show-inheritance:

Polyhex Board
-------------

This module is responsible for managing the puzzle board structure, including the initialization and manipulation of the board grid. It contains logic for positioning pieces and verifying the validity of piece placements within the puzzle.

.. automodule:: polyhex.solver_functions.board
   :members:
   :undoc-members:
   :show-inheritance:

Polyhex Piece
-------------

The module handles the properties and behaviors of individual puzzle pieces. It includes logic for defining piece shapes, positioning, and interactions with the board.

.. automodule:: polyhex.solver_functions.piece
   :members:
   :undoc-members:
   :show-inheritance:

Polyhex Solver
-------------

The solver module includes the core algorithm for solving the Polyhex puzzle. It utilizes the board and piece modules to generate valid solutions by testing different piece placements and configurations.

.. automodule:: polyhex.solver_functions.solver
   :members:
   :undoc-members:
   :show-inheritance:
