# from operator import truediv

# from django.test import TestCase

# from . import matrix_polyominoes, matrix_transformations, matrix_solver

# class PolysphereTestCase(TestCase):
#     def test_rotate_matrix_poly(self):
#         for p in matrix_polyominoes.POLYOMINOES:
#             poly = matrix_polyominoes.Polyomino(p["tiles"],p["poly_id"])
#             coll = []
#             ur = matrix_transformations.unique_rotations(coll, poly)
#             for r in coll:
#                 print(r.poly_id)
#                 matrix_polyominoes.print_polyomino(r)

#     def test_matrix_solver(self):
#         polys = []
#         for p in matrix_polyominoes.POLYOMINOES:
#             poly = matrix_polyominoes.Polyomino(p["tiles"],p["poly_id"])
#             polys.append(poly)
#         s = matrix_solver.MatrixSolver()
#         solution = s.solve_packing(polys,11,5)
#         print(solution)

#     def test_matrix_solver2(self):
#         tiles1 = [[1,0,0],
#                   [1,1,0],
#                   [1,0,0]]
#         tiles2 = [[0,2,2],
#                   [0,0,2],
#                   [0,2,2]]
#         poly1 = matrix_polyominoes.Polyomino(tiles1,1)
#         poly2 = matrix_polyominoes.Polyomino(tiles2,2)
#         polys = [poly1,poly2]
#         s = matrix_solver.MatrixSolver()
#         s.solve_packing(polys, 3, 3)

#     def test_matrix_solver_partial_config(self):
#         p = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[0]["tiles"], 3)
#         polys = [p]
#         board = [[2,2,2],
#                  [0,2,0],
#                  [0,0,0]]
#         s = matrix_solver.MatrixSolver()
#         id_conversions = []
#         solution = s.solve_packing(polys,3,3,board, id_conversions)
#         solution = s.revert_ids(id_conversions, solution)
#         print(solution)

#     def test_matrix_solver_partial_config2(self):
#         p1 = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[0]["tiles"],
#                                          matrix_polyominoes.POLYOMINOES[0]["poly_id"])
#         p2 = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[3]["tiles"],
#                                          matrix_polyominoes.POLYOMINOES[3]["poly_id"])
#         polys = [p1,p2]
#         board = [[0,0,0],
#                  [0,0,0],
#                  [0,0,0]]
#         s = matrix_solver.MatrixSolver()
#         id_conversions = []
#         solutions = s.count_packing(polys,3,3,None,id_conversions)
#         for sol in solutions:
#             s.revert_ids(id_conversions, sol)
#             print(sol)

#     def test_sover_full_board_with_piece_palced(self):
#         #a 11X5 board with a piece with ID 4 on it:
#         board = [[0,0,0,0,0,0,0,0,0,0,0],
#                  [0,0,4,0,0,0,0,0,0,0,0],
#                  [0,4,4,0,0,0,0,0,0,0,0],
#                  [0,0,4,0,0,0,0,0,0,0,0],
#                  [0,0,0,0,0,0,0,0,0,0,0]]

#         # get every piece
#         mps = matrix_polyominoes.POLYOMINOES
#         #remove piece with ID 4 as it's already placed
#         mps.remove(matrix_polyominoes.POLYOMINOES[3])

#         #create polyomino objects from each piece
#         polys = []
#         for mp in mps:
#             polys.append(matrix_polyominoes.Polyomino(mp["tiles"],mp["poly_id"]))

#         #create a solver object
#         s = matrix_solver.MatrixSolver()

#         #list to store ID conversions from the solver
#         id_conversions = []

#         #call the solver
#         solution = s.solve_packing(polys, 11, 5, board, id_conversions)

#         #revert piece ID's to originals
#         solution = s.revert_ids(id_conversions, solution)

#         print("list representation of final solution:")
#         print(solution)



#     def test_all_solutions_empty_board(self):
#         # a 11X5 board with a piece with ID 4 on it:
#         board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


#         # solution = s.count_packing(polys, 11, 5, board, id_conversions)

#         s = matrix_solver.MatrixSolver()

#         # get every piece
#         mps = matrix_polyominoes.POLYOMINOES

#         # create polyomino objects from each piece
#         polys = []
#         for mp in mps:
#             polys.append(matrix_polyominoes.Polyomino(mp["tiles"], mp["poly_id"]))

#         solution = s.count_packing(polys, 11, 5)



#     def test_matrix_solver_gen(self):
#         polys = []
#         for p in matrix_polyominoes.POLYOMINOES:
#             poly = matrix_polyominoes.Polyomino(p["tiles"],p["poly_id"])
#             polys.append(poly)
#         s = matrix_solver.MatrixSolver()
#         #next is used to get the first solution from a generator function
#         rows = next(s.generate_packing_solutions(polys, 11, 5), None)

#         if rows is None:
#             print("no solutions!")
#         else:
#             # Have to now print packing separately from the solver solving function now it's a generator
#             sol = s.print_packing(rows, 11, 5)

#             print("list representation of final solution:")
#             print(sol)

#     def test_matrix_solver2_gen(self):
#         tiles1 = [[1,0,0],
#                   [1,1,0],
#                   [1,0,0]]
#         tiles2 = [[0,2,2],
#                   [0,0,2],
#                   [0,2,2]]
#         poly1 = matrix_polyominoes.Polyomino(tiles1,1)
#         poly2 = matrix_polyominoes.Polyomino(tiles2,2)
#         polys = [poly1,poly2]
#         s = matrix_solver.MatrixSolver()
#         # next is used to get the first solution from a generator function
#         rows = next(s.generate_packing_solutions(polys, 3, 3), None)

#         if rows is None:
#             print("no solutions!")
#         else:
#             # Have to now print packing separately from the solver solving function now it's a generator
#             sol = s.print_packing(rows, 3, 3)

#             print("list representation of final solution:")
#             print(sol)

#     def test_matrix_solver_partial_config_gen(self):
#         p = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[0]["tiles"], 3)
#         polys = [p]
#         board = [[2,2,2],
#                  [0,2,0],
#                  [0,0,0]]
#         s = matrix_solver.MatrixSolver()
#         id_conversions = []

#         rows = next(s.generate_packing_solutions(polys, 3, 3, board, id_conversions), None)

#         if rows is None:
#             print("no solutions!")
#         else:
#             # Have to now print packing separately from the solver solving function now it's a generator
#             sol = s.print_packing(rows, 3, 3)

#             sol_reverted = s.revert_ids(id_conversions, sol)
#             print("list representation of final solution:")
#             print(sol_reverted)

#     def test_generator_solver_all_gen(self):
#         p1 = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[0]["tiles"],
#                                           matrix_polyominoes.POLYOMINOES[0]["poly_id"])
#         p2 = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[3]["tiles"],
#                                           matrix_polyominoes.POLYOMINOES[3]["poly_id"])
#         polys = [p1, p2]
#         board = [[0, 0, 0],
#                  [0, 0, 0],
#                  [0, 0, 0]]
#         s = matrix_solver.MatrixSolver()
#         id_conversions = []
#         solution_count = 0

#         for rows in s.generate_packing_solutions(polys, 3, 3, None, id_conversions):
#             # Have to now print packing separately from the solver solving function now it's a generator
#             sol = s.print_packing(rows, 3, 3)

#             sol_reverted = s.revert_ids(id_conversions, sol)
#             if sol_reverted != None:
#                 solution_count += 1
#                 print("list representation of solution " + str(solution_count) + ":")
#                 print(sol_reverted)

#         if solution_count == 0:
#             print("no solutions!")

#     def test_sover_full_board_with_piece_palced_gen(self):
#         #a 11X5 board with a piece with ID 4 on it:
#         board = [[0,0,0,0,0,0,0,0,0,0,0],
#                  [0,0,4,0,0,0,0,0,0,0,0],
#                  [0,4,4,0,0,0,0,0,0,0,0],
#                  [0,0,4,0,0,0,0,0,0,0,0],
#                  [0,0,0,0,0,0,0,0,0,0,0]]

#         # get every piece
#         mps = matrix_polyominoes.POLYOMINOES
#         #remove piece with ID 4 as it's already placed
#         mps.remove(matrix_polyominoes.POLYOMINOES[3])

#         #create polyomino objects from each piece
#         polys = []
#         for mp in mps:
#             polys.append(matrix_polyominoes.Polyomino(mp["tiles"],mp["poly_id"]))

#         #create a solver object
#         s = matrix_solver.MatrixSolver()

#         #list to store ID conversions from the solver
#         id_conversions = []

#         rows = next(s.generate_packing_solutions(polys, 11, 5, board, id_conversions), None)

#         if rows is None:
#             print("no solutions!")
#         else:
#             # Have to now print packing separately from the solver solving function now it's a generator
#             sol = s.print_packing(rows, 11, 5)

#             sol_reverted = s.revert_ids(id_conversions, sol)
#             print("list representation of final solution:")
#             print(sol_reverted)



#     def test_all_solutions_empty_board_gen(self):
#         # a 11X5 board with a piece with ID 4 on it:
#         board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


#         # solution = s.count_packing(polys, 11, 5, board, id_conversions)

#         s = matrix_solver.MatrixSolver()

#         # get every piece
#         mps = matrix_polyominoes.POLYOMINOES

#         # create polyomino objects from each piece
#         polys = []
#         for mp in mps:
#             polys.append(matrix_polyominoes.Polyomino(mp["tiles"], mp["poly_id"]))

#         solution_count = 0

#         for rows in s.generate_packing_solutions(polys, 11, 5):
#             # Have to now print packing separately from the solver solving function now it's a generator
#             sol = s.print_packing(rows, 11, 5)

#             if sol != None:
#                 solution_count += 1
#                 print("list representation of solution " + str(solution_count) + ":")
#                 print(sol)

#         if solution_count == 0:
#             print("no solutions!")





