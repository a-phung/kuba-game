# Author: Andy Phung
# Date: 5/24/2021
# Description: Class KubaGame initializes a kuba game with two players and a game board. The game board consists of
#              8 white marbles for one player, 8 black marbles for another player, and 13 neutral red marbles. Players
#              take turns making valid moves until one player has captured 7 neutral red marbles, until one player
#              has captured all of the other player's marbles, or until one player has eliminated all legal moves for
#              the other player. When any of these win conditions have been met, that player is the winner.

class KubaGame:
    """Represents a KubaGame object with game mechanics."""
    def __init__(self, player1, player2):
        """
        Creates a KubaGame with players, a board, and a marble count.
        :param player1: A tuple containing the player name and the player's marble color (ex: ('PlayerA','W'))
        :param player2: A tuple containing the player name and the player's marble color (ex: ('PlayerB','B'))
        """
        self._player1 = player1
        self._player1_bank = [0, 0]
        self._player2 = player2
        self._player2_bank = [0, 0]
        self._current_player = None
        self._board = [["W", "W", "X", "X", "X", "B", "B"],
                       ["W", "W", "X", "R", "X", "B", "B"],
                       ["X", "X", "R", "R", "R", "X", "X"],
                       ["X", "R", "R", "R", "R", "R", "X"],
                       ["X", "X", "R", "R", "R", "X", "X"],
                       ["B", "B", "X", "R", "X", "W", "W"],
                       ["B", "B", "X", "X", "X", "W", "W"]]
        self._p1_prev_board = [["W", "W", "X", "X", "X", "B", "B"],
                               ["W", "W", "X", "R", "X", "B", "B"],
                               ["X", "X", "R", "R", "R", "X", "X"],
                               ["X", "R", "R", "R", "R", "R", "X"],
                               ["X", "X", "R", "R", "R", "X", "X"],
                               ["B", "B", "X", "R", "X", "W", "W"],
                               ["B", "B", "X", "X", "X", "W", "W"]]
        self._p2_prev_board = [["W", "W", "X", "X", "X", "B", "B"],
                               ["W", "W", "X", "R", "X", "B", "B"],
                               ["X", "X", "R", "R", "R", "X", "X"],
                               ["X", "R", "R", "R", "R", "R", "X"],
                               ["X", "X", "R", "R", "R", "X", "X"],
                               ["B", "B", "X", "R", "X", "W", "W"],
                               ["B", "B", "X", "X", "X", "W", "W"]]
        self._winner = None

    def get_current_turn(self):
        """Returns the player name whose turn it is. Otherwise, returns None if no player has made the first move."""
        return self._current_player

    def make_move(self, player_name, coordinates, direction):
        """
        Makes a move on the board through user input validation.
        :param player_name: The player's name as a string
        :param coordinates: A tuple containing the location of the marble that is to be moved (ex: (row, column)).
        :param direction: A direction that the player wants to push the marble. There are four valid directions:
                          "L" (Left), "R" (Right), "F" (Forward), and "B" (Backward)
        :return: True if the the move is valid. Otherwise, returns False if the move is invalid
        """
        # Validate player
        player1 = player_name == self._player1[0]
        player2 = player_name == self._player2[0]
        if player1 and self._current_player is None:
            self._current_player = player_name
        elif player2 and self._current_player is None:
            self._current_player = player_name
        elif player_name != self._current_player:
            return False

        if player1:
            player_marble = self._player1[1]
        elif player2:
            player_marble = self._player2[1]
        else:
            player_marble = None

        # Validate coordinates
        row, column = coordinates[0], coordinates[1]
        if not 0 <= row <= 6 or not 0 <= column <= 6:
            return False
        elif self._board[row][column] != player_marble:
            return False

        # Validate direction
        value = self.valid_direction(row, column, direction)
        if not value:
            return False

        # Make move
        move = []
        end_index, captured_marble = None, None

        # Make forward move
        if direction == "F":
            board_column = [rows[column] for rows in self._board]
            for square in range(row, -1, -1):
                if board_column[square] == "X":
                    end_index = square
                    break
            if end_index is not None:
                for square in range(len(board_column) - 1, -1, -1):
                    if square == row:
                        move = ["X"] + move
                        move = [board_column[square]] + move
                    elif square == end_index:
                        continue
                    else:
                        move = [board_column[square]] + move
            else:
                captured_marble = board_column[0]
                if captured_marble == player_marble:
                    return False
                for square in range(len(board_column) - 1, 0, -1):
                    if square == row:
                        move = ["X"] + move
                        move = [board_column[square]] + move
                    else:
                        move = [board_column[square]] + move
            # Replace column with move
            index = 0
            for row in self._board:
                row[column] = move[index]
                index += 1

        # Make backward move
        if direction == "B":
            board_column = [rows[column] for rows in self._board]
            for square in range(row, len(board_column)):
                if board_column[square] == "X":
                    end_index = square
                    break
            if end_index is not None:
                for square in range(0, len(board_column)):
                    if square == row:
                        move.append("X")
                        move.append(board_column[square])
                    elif square == end_index:
                        continue
                    else:
                        move.append(board_column[square])
            else:
                captured_marble = board_column[len(board_column) - 1]
                if captured_marble == player_marble:
                    return False
                for square in range(0, len(board_column) - 1):
                    if square == row:
                        move.append("X")
                        move.append(board_column[square])
                    else:
                        move.append(board_column[square])
            # Replace column with move
            index = 0
            for row in self._board:
                row[column] = move[index]
                index += 1

        # Make left move
        if direction == "L":
            board_row = self._board[row]
            for square in range(column, -1, -1):
                if board_row[square] == "X":
                    end_index = square
                    break
            if end_index is not None:
                for square in range(len(board_row) - 1, -1, -1):
                    if square == column:
                        move = ["X"] + move
                        move = [board_row[square]] + move
                    elif square == end_index:
                        continue
                    else:
                        move = [board_row[square]] + move
            else:
                captured_marble = board_row[0]
                if captured_marble == player_marble:
                    return False
                for square in range(len(board_row) - 1, 0, -1):
                    if square == column:
                        move = ["X"] + move
                        move = [board_row[square]] + move
                    else:
                        move = [board_row[square]] + move
            self._board[row] = move

        # Make right move
        if direction == "R":
            board_row = self._board[row]
            for square in range(column, len(board_row)):
                if board_row[square] == "X":
                    end_index = square
                    break
            if end_index is not None:
                for square in range(0, len(board_row)):
                    if square == column:
                        move.append("X")
                        move.append(board_row[square])
                    elif square == end_index:
                        continue
                    else:
                        move.append(board_row[square])
            else:
                captured_marble = board_row[len(board_row) - 1]
                if captured_marble == player_marble:
                    return False
                for square in range(0, len(board_row) - 1):
                    if square == column:
                        move.append("X")
                        move.append(board_row[square])
                    else:
                        move.append(board_row[square])
            self._board[row] = move

        # Check to see if move is valid; check ko rule
        if player1:
            if self._p1_prev_board == self._board:
                self._board = []
                for row in self._p2_prev_board:
                    self._board.append(list(row))
                return False
            else:
                self._p1_prev_board = []
                for row in self._board:
                    self._p1_prev_board.append(list(row))
        else:
            if self._p2_prev_board == self._board:
                self._board = []
                for row in self._p1_prev_board:
                    self._board.append(list(row))
                return False
            else:
                self._p2_prev_board = []
                for row in self._board:
                    self._p2_prev_board.append(list(row))

        # If a marble was captured, record marble, and evaluate win
        winner = None
        if captured_marble:
            winner = self.captured(captured_marble, player1, player2)

        if winner is not None:
            self._winner = winner
        elif player1:
            self._current_player = self._player2[0]
        else:
            self._current_player = self._player1[0]

        return True

    def valid_direction(self, row, column, direction):
        """
        Helper function for make_move to validate the direction of the player's move.
        :param row: The row number as an integer of the marble to be moved
        :param column: The column number as an integer of the marble to be moved
        :param direction: A valid direction as a char to move the marble
        :return: True if the direction is valid. Else, False if the direction is invalid.
        """
        forward1, back1, right1, left1 = row - 1, row + 1, column + 1, column - 1

        # Validate forward
        if direction == "F" and back1 != 7:
            if row == 0 or self._board[back1][column] != "X":
                return False

        # Validate backward
        if direction == "B" and forward1 != -1:
            if row == 6 or self._board[forward1][column] != "X":
                return False

        # Validate right
        if direction == "R" and left1 != -1:
            if column == 6 or self._board[row][left1] != "X":
                return False

        # Validate left
        if direction == "L" and right1 != 7:
            if column == 0 or self._board[row][right1] != "X":
                return False

        return True

    def captured(self, captured_marble, player1, player2):
        """
        Helper function for make_move to determine a winner from the move made.
        :param captured_marble: The color of the captured marble as a char ("W", "B", or "R")
        :param player1: True if the player is player1. Else, False if the player is player2.
        :param player2: False if the player is player1. Else, True if the player is player2.
        :return: Player's name if that player is the winner. Else, None if there is no winner.
        """
        if player1 and captured_marble == "R":
            self._player1_bank[0] += 1
        elif player1 and captured_marble == self._player2[1]:
            self._player1_bank[1] += 1
        elif player2 and captured_marble == "R":
            self._player2_bank[0] += 1
        else:
            self._player2_bank[1] += 1

        if self._player1_bank[0] == 7 or self._player1_bank[1] == 8:
            return self._player1[0]
        elif self._player2_bank[0] == 7 or self._player2_bank[1] == 8:
            return self._player2[0]
        else:
            return

    def get_winner(self):
        """Returns the name of the winning player."""
        return self._winner

    def get_captured(self, player_name):
        """Returns the number of Red marbles captured by the given player name. Else, returns None."""
        if player_name == self._player1[0]:
            return self._player1_bank[0]
        elif player_name == self._player2[0]:
            return self._player2_bank[0]
        else:
            return

    def get_marble(self, coordinates):
        """Returns the marble that is present at the coordinate location."""
        return self._board[coordinates[0]][coordinates[1]]

    def get_marble_count(self):
        """Returns the number of white, black, and red marbles as a tuple in the order (W,B,R)."""
        if self._player1[1] == "W":
            white_captured = self._player2_bank[1]
            black_captured = self._player1_bank[1]
        else:
            white_captured = self._player1_bank[1]
            black_captured = self._player2_bank[1]
        red_captured = self._player1_bank[0] + self._player2_bank[0]

        total_white = 8 - white_captured
        total_black = 8 - black_captured
        total_red = 13 - red_captured

        return total_white, total_black, total_red
