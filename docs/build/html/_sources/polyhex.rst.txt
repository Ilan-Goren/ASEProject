Polyhex Application Documentation
==================================

This documentation provides an overview of the Polyhex application, its class structure, and views.

Content
-------

1. Polyhex Class
2. Polyhex Views

Polyhex Class
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
