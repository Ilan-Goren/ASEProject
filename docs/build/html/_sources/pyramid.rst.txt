Pyramid Application Documentation
==================================

This documentation provides an overview of the Pyramid application, its class structure, and views.

Content
-------

1. Pyramid Class
2. Pyramid Views

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
