from games import *

class GameOfNim(Game):
    ''' Two players take turns removing objects from distinct heaps or rows
        In each turn, a player must remove at least one object from the same row
        The winner is the player that takes the last object(s). '''
    
    # YOUR CODE GOES HERE
    def __init__(self, board=[]):
        """ Define goal state and initialize a problem """
        moves = []
        r = 0
        for row in board:
            if row != 0:
                n = 1
                while n <= row:
                    moves.append([r, n])
                    n += 1
            r += 1

        self.initial = GameState(to_move=1, utility=0, board=board, moves=moves)   

    def actions(self, state):
        moves = []
        r = 0

        for row in state.board:
            if row != 0:
                n = 1
                while n <= row:
                    moves.append([r, n])
                    n += 1
            r += 1

        return moves
        
    def result(self, state, move):
        # move = (1,3), remove one from 1st row
        new_board = state.board.copy()
        moves = []
        r = 0
        
        new_board[move[0]] = state.board[move[0]] - move[1]

        for row in new_board:
            if row != 0:
                n = 1
                while n <= row:
                    moves.append([r, n])
                    n += 1
            r += 1

        return GameState(to_move=(state.to_move + 1) % 2, utility=0, board=new_board, moves=moves)   

    def utility(self, state, player):
        if player == 1:
            return 1
        else:
            return -1

    def terminal_test(self, state):
        for row in state.board:
            if row != 0:
                return False

        return True