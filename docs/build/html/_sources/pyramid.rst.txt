Pyramid Application Documentation
==================================

This documentation provides an overview of the Pyramid application, its class structure, and views.

Content
-------

1. Pyramid Views
2. Pyramid Main
3. Pyramid Board
4. Pyramid Piece
5. Pyramid Solver

Pyramid Class
--------------

The `Pyramid` class handles the core functionality of the Pyramid puzzle application. It includes the logic for solving the Pyramid puzzle and managing the state of the puzzle board.

.. autoclass:: pyramid.Pyramid.Pyramid_Solver
   :members:
   :undoc-members:
   :show-inheritance:

Pyramid Views
-------------

The views in this module handle the HTTP requests for rendering different parts of the Pyramid application, such as the puzzle board and solution generator.

.. automodule:: pyramid.views
   :members:
   :undoc-members:
   :show-inheritance:

Pyramid Board
--------------

The `Board` module is responsible for the representation and management of the Pyramid puzzle board. It handles the structure and state of the board, including rendering and interacting with the pieces during the puzzle-solving process.

.. automodule:: pyramid.solver_functions.board  
   :members:  
   :undoc-members:  
   :show-inheritance:  

Pyramid Piece
--------------

The `Piece` module manages the individual pieces used to solve the Pyramid puzzle. It includes logic for piece manipulation, checking valid placements, and interacting with the board.

.. automodule:: pyramid.solver_functions.piece  
   :members:  
   :undoc-members:  
   :show-inheritance:  

Pyramid Solver
--------------

The `Solver` module contains the core algorithm for solving the Pyramid puzzle. It includes the logic for finding solutions, optimizing placements, and handling the puzzle-solving process.

.. automodule:: pyramid.solver_functions.solver  
   :members:  
   :undoc-members:  
   :show-inheritance:
