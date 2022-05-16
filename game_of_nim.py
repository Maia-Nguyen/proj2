from games import *

class GameOfNim(Game):
    ''' Two players take turns removing objects from distinct heaps or rows
        In each turn, a player must remove at least one object from the same row
        The winner is the player that takes the last object(s). '''
    
    # YOUR CODE GOES HERE
    def __init__(self, board=[], to_move=1):
        """ Define goal state and initialize a problem """
        moves = []

        for idx, row in enumerate(board):
            for n in range(1, row + 1):
                moves.append([idx, n])


        self.initial = GameState(to_move=to_move, utility=0, board=board, moves=moves)

    def actions(self, state):
        moves = []

        for idx, row in enumerate(state.board):
            for n in range(1, row + 1):
                moves.append([idx, n])

        return moves
        
    def result(self, state, move):
        # move = (1,3), remove one from 1st row
        new_board = state.board.copy()
        moves = []
        
        new_board[move[0]] = state.board[move[0]] - move[1]

        for idx, row in enumerate(new_board):
                for n in range(1, row + 1):
                    moves.append([idx, n])

        return GameState(to_move=(state.to_move + 1) % 2, utility=0, board=new_board, moves=moves)   

    # The utility function determines which side the max is assigned to.
    def utility(self, state, player):
        if state.to_move == 1: # ' == 0 ' for prioritizing first player and ' == 1' for second player
            return 1
        else:
            return -1

    def terminal_test(self, state):
        for row in state.board:
            if row != 0:
                return False

        return True