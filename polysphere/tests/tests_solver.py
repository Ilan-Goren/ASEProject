from operator import truediv

from django.test import TestCase

from ..solver_functions import matrix_polyominoes, matrix_solver

from ..solver_functions import matrix_transformations

class PolysphereTestCase(TestCase):
    def test_rotate_matrix_poly(self):
        # get all transformations for all polyominoes, print them and store them in options
        options = []
        for p in matrix_polyominoes.POLYOMINOES:
            poly = matrix_polyominoes.Polyomino(p["tiles"],p["poly_id"])
            coll = []
            ur = matrix_transformations.unique_rotations(coll, poly)
            options.append(coll)
            for r in coll:
                print(r.poly_id)
                matrix_polyominoes.print_polyomino(r)
        '''
        for o in options:
            for polyomino in o:
                print(polyomino.tiles)
        '''

        # get a few shapes that we expect to see in the results
        expected_shape1 = [[1,1],
                          [0,1],
                          [1,1]]
        expected_shape2 = [[1, 1, 1, 0],
                          [0, 0, 1, 1]]
        expected_shape3 = [[0,1],
                          [1,1],
                          [0,1]]
        expected_shape4 = [[1,0,0],
                          [1,0,0],
                          [1,1,1]]
        expected_shape5 = [[1,1],
                          [1,0]]

        expected_shapes = [expected_shape1,expected_shape2,expected_shape3,expected_shape4,expected_shape5]

        all_expected_shapes_found = True

        for e in expected_shapes:
            e_found = False
            for o in options:
                for polyomino in o:
                    if polyomino.tiles == e:
                        e_found = True
                        break
                if e_found:
                    break
            if not e_found:
                all_expected_shapes_found = False

        self.assertTrue(all_expected_shapes_found)

    def test_matrix_solver(self):
        polys = []
        for p in matrix_polyominoes.POLYOMINOES:
            poly = matrix_polyominoes.Polyomino(p["tiles"],p["poly_id"])
            polys.append(poly)
        s = matrix_solver.MatrixSolver()
        solution = s.solve_packing(polys,11,5)
        print(solution)

        # ensure the size of the solution is correct
        self.assertEqual(len(solution),5)
        self.assertEqual(len(solution[0]), 11)

        board_has_empty_space = False
        IDs_found = set()

        for y in solution:
            for x in y:
                if x == 0:
                    board_has_empty_space = True
                else:
                    IDs_found.add(x)

        expectedIDs = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
        self.assertFalse(board_has_empty_space)
        self.assertEqual(IDs_found, expectedIDs)

    def test_matrix_solver2(self):
        tiles1 = [[1,0,0],
                  [1,1,0],
                  [1,0,0]]
        tiles2 = [[0,2,2],
                  [0,0,2],
                  [0,2,2]]
        poly1 = matrix_polyominoes.Polyomino(tiles1,1)
        poly2 = matrix_polyominoes.Polyomino(tiles2,2)
        polys = [poly1,poly2]
        s = matrix_solver.MatrixSolver()
        res = s.solve_packing(polys, 3, 3)

        expected_res = [[1,2,2],
                       [1,1,2],
                       [1,2,2]]

        self.assertEqual(res, expected_res)

    def test_matrix_solver_partial_config(self):
        p = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[0]["tiles"], 3)
        polys = [p]
        board = [[2,2,2],
                 [0,2,0],
                 [0,0,0]]
        s = matrix_solver.MatrixSolver()
        id_conversions = []
        res = s.solve_packing(polys,3,3,board, id_conversions)

        res = s.revert_ids(id_conversions, res)
        expected_res = [[2,2,2],
                        [3,2,3],
                        [3,3,3]]

        self.assertEqual(res, expected_res)

    def test_matrix_solver_partial_config2(self):
        p1 = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[0]["tiles"],
                                         matrix_polyominoes.POLYOMINOES[0]["poly_id"])
        p2 = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[3]["tiles"],
                                         matrix_polyominoes.POLYOMINOES[3]["poly_id"])
        polys = [p1,p2]
        s = matrix_solver.MatrixSolver()
        id_conversions = []
        solutions = s.count_packing(polys,3,3,None,id_conversions)

        self.assertEqual(len(solutions),4)

        sample_solution = [[4,1,1],
                           [4,4,1],
                           [4,1,1]]

        sample_solution_found = False

        for sol in solutions:
            s.revert_ids(id_conversions, sol)
            print(sol)
            if sol == sample_solution:
                sample_solution_found = True

        self.assertTrue(sample_solution_found)

    # do not uncomment this test in the main branch it takes too long to execute and will cause version control
    # issues
    '''
    def test_sover_full_board_with_piece_palced(self):
        #a 11X5 board with a piece with ID 4 on it:
        board = [[0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,4,0,0,0,0,0,0,0,0],
                 [0,4,4,0,0,0,0,0,0,0,0],
                 [0,0,4,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0]]

        # get every piece
        mps = matrix_polyominoes.POLYOMINOES
        #remove piece with ID 4 as it's already placed
        mps.remove(matrix_polyominoes.POLYOMINOES[3])

        #create polyomino objects from each piece
        polys = []
        for mp in mps:
            polys.append(matrix_polyominoes.Polyomino(mp["tiles"],mp["poly_id"]))

        #create a solver object
        s = matrix_solver.MatrixSolver()

        #list to store ID conversions from the solver
        id_conversions = []

        #call the solver
        solution = s.solve_packing(polys, 11, 5, board, id_conversions)

        #revert piece ID's to originals
        solution = s.revert_ids(id_conversions, solution)

        print("list representation of final solution:")         
        print(solution)
    '''

    # do not uncomment this test in the main branch it takes too long to execute and will cause version control
    # issues
    '''
    def test_all_solutions_empty_board(self):
        # a 11X5 board with a piece with ID 4 on it:


        s = matrix_solver.MatrixSolver()

        # get every piece
        mps = matrix_polyominoes.POLYOMINOES

        # create polyomino objects from each piece
        polys = []
        for mp in mps:
            polys.append(matrix_polyominoes.Polyomino(mp["tiles"], mp["poly_id"]))

        solution = s.count_packing(polys, 11, 5)
    '''

    def test_matrix_solver_gen(self):
        polys = []
        for p in matrix_polyominoes.POLYOMINOES:
            poly = matrix_polyominoes.Polyomino(p["tiles"],p["poly_id"])
            polys.append(poly)
        s = matrix_solver.MatrixSolver()
        #next is used to get the first solution from a generator function
        rows = next(s.generate_packing_solutions(polys, 11, 5), None)

        if rows is None:
            print("no solutions!")
        else:
            # Have to now print packing separately from the solver solving function now it's a generator
            sol = s.print_packing(rows, 11, 5)

        # ensure the size of the solution is correct
        self.assertEqual(len(sol), 5)
        self.assertEqual(len(sol[0]), 11)

        board_has_empty_space = False
        IDs_found = set()

        for y in sol:
            for x in y:
                if x == 0:
                    board_has_empty_space = True
                else:
                    IDs_found.add(x)

        expectedIDs = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
        self.assertFalse(board_has_empty_space)
        self.assertEqual(IDs_found, expectedIDs)

    def test_matrix_solver2_gen(self):
        tiles1 = [[1,0,0],
                  [1,1,0],
                  [1,0,0]]
        tiles2 = [[0,2,2],
                  [0,0,2],
                  [0,2,2]]
        poly1 = matrix_polyominoes.Polyomino(tiles1,1)
        poly2 = matrix_polyominoes.Polyomino(tiles2,2)
        polys = [poly1,poly2]
        s = matrix_solver.MatrixSolver()
        # next is used to get the first solution from a generator function
        rows = next(s.generate_packing_solutions(polys, 3, 3), None)

        if rows is None:
            print("no solutions!")
        else:
            # Have to now print packing separately from the solver solving function now it's a generator
            sol = s.print_packing(rows, 3, 3)

        expected_res = [[1, 2, 2],
                        [1, 1, 2],
                        [1, 2, 2]]

        self.assertEqual(sol, expected_res)

    def test_matrix_solver_partial_config_gen(self):
        p = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[0]["tiles"], 3)
        polys = [p]
        board = [[2,2,2],
                 [0,2,0],
                 [0,0,0]]
        s = matrix_solver.MatrixSolver()
        id_conversions = []

        rows = next(s.generate_packing_solutions(polys, 3, 3, board, id_conversions), None)

        if rows is None:
            print("no solutions!")
        else:
            # Have to now print packing separately from the solver solving function now it's a generator
            sol = s.print_packing(rows, 3, 3)

            sol_reverted = s.revert_ids(id_conversions, sol)

        expected_res = [[2, 2, 2],
                        [3, 2, 3],
                        [3, 3, 3]]

        self.assertEqual(sol, expected_res)

    def test_generator_solver_all_gen(self):
        p1 = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[0]["tiles"],
                                          matrix_polyominoes.POLYOMINOES[0]["poly_id"])
        p2 = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[3]["tiles"],
                                          matrix_polyominoes.POLYOMINOES[3]["poly_id"])
        polys = [p1, p2]
        board = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]
        s = matrix_solver.MatrixSolver()
        id_conversions = []
        solution_count = 0

        sample_solution = [[4, 1, 1],
                           [4, 4, 1],
                           [4, 1, 1]]

        sample_solution_found = False

        for rows in s.generate_packing_solutions(polys, 3, 3, None, id_conversions):
            # Have to now print packing separately from the solver solving function now it's a generator
            sol = s.print_packing(rows, 3, 3)

            sol_reverted = s.revert_ids(id_conversions, sol)
            if sol_reverted != None:
                solution_count += 1
                if sol_reverted == sample_solution:
                    sample_solution_found = True

        self.assertEqual(solution_count, 4)

        self.assertTrue(sample_solution_found)

# do not uncomment this test in the main branch it takes too long to execute and will cause version control
# issues
'''
     def test_sover_full_board_with_piece_palced_gen(self):
         #a 11X5 board with a piece with ID 4 on it:
         board = [[0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,4,0,0,0,0,0,0,0,0],
                  [0,4,4,0,0,0,0,0,0,0,0],
                  [0,0,4,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0]]

         # get every piece
         mps = matrix_polyominoes.POLYOMINOES
         #remove piece with ID 4 as it's already placed
         mps.remove(matrix_polyominoes.POLYOMINOES[3])

         #create polyomino objects from each piece
         polys = []
         for mp in mps:
             polys.append(matrix_polyominoes.Polyomino(mp["tiles"],mp["poly_id"]))

         #create a solver object
         s = matrix_solver.MatrixSolver()

         #list to store ID conversions from the solver
         id_conversions = []

         rows = next(s.generate_packing_solutions(polys, 11, 5, board, id_conversions), None)

         if rows is None:
             print("no solutions!")
         else:
             # Have to now print packing separately from the solver solving function now it's a generator
             sol = s.print_packing(rows, 11, 5)

             sol_reverted = s.revert_ids(id_conversions, sol)
             print("list representation of final solution:")
             print(sol_reverted)
'''

# do not uncomment this test in the main branch it takes too long to execute and will cause version control
# issues
'''
     def test_all_solutions_empty_board_gen(self):
         # a 11X5 board with a piece with ID 4 on it:
         board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


         # solution = s.count_packing(polys, 11, 5, board, id_conversions)

         s = matrix_solver.MatrixSolver()

         # get every piece
         mps = matrix_polyominoes.POLYOMINOES

         # create polyomino objects from each piece
         polys = []
         for mp in mps:
             polys.append(matrix_polyominoes.Polyomino(mp["tiles"], mp["poly_id"]))

         solution_count = 0

         for rows in s.generate_packing_solutions(polys, 11, 5):
             # Have to now print packing separately from the solver solving function now it's a generator
             sol = s.print_packing(rows, 11, 5)

             if sol != None:
                 solution_count += 1
                 print("list representation of solution " + str(solution_count) + ":")
                 print(sol)

         if solution_count == 0:
             print("no solutions!")
'''




