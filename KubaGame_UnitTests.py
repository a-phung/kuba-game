import unittest
from KubaGame import KubaGame


class UnitTests(unittest.TestCase):
    def test_case1(self):
        """Test readme test cases."""
        game = KubaGame(("PlayerA", "W"), ("PlayerB", "B"))
        self.assertEqual(game.get_marble_count(), (8, 8, 13))  # returns (8,8,13)
        self.assertEqual(game.get_captured('PlayerA'), 0)  # returns 0
        self.assertEqual(game.get_current_turn(), None)  # returns None
        self.assertEqual(game.get_winner(), None)  # returns None
        self.assertTrue(game.make_move('PlayerA', (6, 5), 'F'))  # True
        # print(game.get_board())
        self.assertFalse(game.make_move('PlayerA', (6, 5), 'L'))  # Cannot make this move; returns False
        self.assertEqual(game.get_marble((5, 5)), "W")  # returns 'W'

    def test_case2(self):
        """Test complete game with 'playerA' win."""
        game = KubaGame(("PlayerA", "W"), ("PlayerB", "B"))
        self.assertTrue(game.make_move("PlayerA", (6, 6), "F"))
        self.assertTrue(game.make_move("PlayerB", (6, 0), "F"))
        self.assertTrue(game.make_move("PlayerA", (5, 6), "F"))
        self.assertTrue(game.make_move("PlayerB", (5, 0), "F"))
        self.assertTrue(game.make_move("PlayerA", (3, 6), "L"))
        self.assertEqual(game.get_captured("PlayerA"), 0)
        self.assertTrue(game.make_move("PlayerB", (6, 1), "F"))
        self.assertTrue(game.make_move("PlayerA", (3, 5), "L"))
        self.assertEqual(game.get_captured("PlayerA"), 1)
        self.assertTrue(game.make_move("PlayerB", (5, 1), "R"))
        self.assertTrue(game.make_move("PlayerA", (3, 4), "L"))
        self.assertTrue(game.make_move("PlayerB", (4, 0), "R"))
        self.assertTrue(game.make_move("PlayerA", (3, 3), "L"))
        self.assertTrue(game.make_move("PlayerB", (4, 1), "R"))
        self.assertTrue(game.make_move("PlayerA", (3, 2), "L"))
        self.assertTrue(game.make_move("PlayerB", (4, 2), "R"))
        self.assertTrue(game.make_move("PlayerA", (3, 1), "L"))
        self.assertTrue(game.make_move("PlayerB", (4, 3), "R"))
        self.assertEqual(game.get_captured("PlayerA"), 5)
        self.assertEqual(game.get_captured("PlayerB"), 2)
        self.assertEqual(game.get_winner(), None)
        self.assertEqual(game.get_current_turn(), "PlayerA")
        self.assertTrue(game.make_move("PlayerA", (0, 0), "R"))
        self.assertTrue(game.make_move("PlayerB", (0, 6), "B"))
        self.assertTrue(game.make_move("PlayerA", (0, 1), "R"))
        self.assertTrue(game.make_move("PlayerB", (1, 6), "B"))
        self.assertTrue(game.make_move("PlayerA", (0, 3), "B"))
        self.assertTrue(game.make_move("PlayerB", (2, 6), "B"))
        self.assertTrue(game.make_move("PlayerA", (1, 3), "B"))
        self.assertTrue(game.make_move("PlayerB", (3, 6), "B"))
        self.assertTrue(game.make_move("PlayerA", (2, 3), "B"))
        self.assertTrue(game.make_move("PlayerB", (4, 6), "B"))
        self.assertEqual(game.get_captured("PlayerA"), 5)
        self.assertEqual(game.get_captured("PlayerB"), 3)
        self.assertEqual(game.get_winner(), None)
        self.assertTrue(game.make_move("PlayerA", (3, 3), "B"))
        self.assertTrue(game.make_move("PlayerB", (0, 5), "L"))
        self.assertTrue(game.make_move("PlayerA", (4, 3), "B"))
        self.assertEqual(game.get_captured("PlayerA"), 7)
        self.assertEqual(game.get_marble_count(), (7, 7, 3))
        self.assertEqual(game.get_marble((3, 3)), "X")
        self.assertEqual(game.get_winner(), "PlayerA")

    def test_case3(self):
        """Test moves that try to raise exceptions."""
        game = KubaGame(("PlayerA", "B"), ("PlayerB", "W"))
        self.assertEqual(game.get_current_turn(), None)
        self.assertTrue(game.make_move("PlayerB", (0, 0), "R"))     # PlayerB moves first
        self.assertFalse(game.make_move("PlayerB", (6, 6), "F"))    # False - PlayerB moves again
        self.assertEqual(game.get_current_turn(), "PlayerA")
        self.assertFalse(game.make_move("PlayerA", (7, 6), "F"))    # Test row input out of range
        self.assertFalse(game.make_move("PlayerA", (-1, 0), "F"))   # Test row input out of range
        self.assertFalse(game.make_move("PlayerA", (6, 7), "F"))    # Test column input out of range
        self.assertFalse(game.make_move("PlayerA", (0, -1), "F"))   # Test column input out of range
        self.assertFalse(game.make_move("PlayerA", (-1, 7), "F"))   # Test both row and column input out of range
        self.assertFalse(game.make_move("PlayerA", (7, -1), "F"))   # Test both row and column input out of range
        self.assertTrue(game.make_move("PlayerA", (6, 0), "F"))
        self.assertEqual(game.get_current_turn(), "PlayerB")
        self.assertTrue(game.make_move("PlayerB", (1, 0), "R"))
        self.assertTrue(game.make_move("PlayerA", (4, 0), "B"))     # Move back
        self.assertTrue(game.make_move("PlayerB", (1, 1), "R"))
        self.assertTrue(game.make_move("PlayerA", (1, 6), "L"))
        self.assertFalse(game.make_move("PlayerB", (1, 1), "R"))    # False - Ko rule; board is unchanged
        self.assertEqual(game.get_current_turn(), "PlayerB")
        self.assertFalse(game.make_move("PlayerA", (0, 6), "L"))    # False - Not playerA's turn
        self.assertFalse(game.make_move("PlayerB", (0, 6), "L"))    # False - Wrong color marble
        self.assertFalse(game.make_move("PlayerB", (0, 2), "R"))    # False - Correct marble but invalid move
        self.assertFalse(game.make_move("PlayerB", (6, 5), "R"))    # False - Push own marble off board
        self.assertTrue(game.make_move("PlayerB", (5, 6), "L"))
        self.assertFalse(game.make_move("PlayerA", (0, 6), "F"))    # False - Push own single marble off board
        self.assertTrue(game.make_move("PlayerA", (0, 6), "B"))
        self.assertFalse(game.make_move("PlayerB", (5, 6), "L"))    # False - Invalid move
        self.assertFalse(game.make_move("PlayerB", (5, 6), "R"))    # False - Invalid move
        self.assertFalse(game.make_move("PlayerB", (5, 6), "D"))    # False - Invalid move
        # print(game.get_board())

    def test_case4(self):
        """Another move check."""
        game = KubaGame(("PlayerA", "W"), ("PlayerB", "B"))
        self.assertTrue(game.make_move("PlayerA", (6, 6), "F"))
        self.assertTrue(game.make_move("PlayerB", (0, 6), "B"))
        self.assertTrue(game.make_move("PlayerA", (4, 6), "L"))
        self.assertTrue(game.make_move("PlayerB", (1, 6), "B"))
        self.assertTrue(game.make_move("PlayerA", (4, 5), "L"))
        self.assertTrue(game.make_move("PlayerB", (2, 6), "B"))
        self.assertTrue(game.make_move("PlayerA", (4, 4), "L"))
        # print(game.get_board())
