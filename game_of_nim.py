from games import *

class GameOfNim(Game):
    ''' Two players take turns removing objects from distinct heaps or rows
        In each turn, a player must remove at least one object from the same row
        The winner is the player that takes the last object(s). '''
    
    # YOUR CODE GOES HERE
    def __init__(self, board=[]):
        """ Define goal state and initialize a problem """
        self.board = board
        moves = []
        r = 0
        for row in self.board:
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

        for row in state:
            if row != 0:
                n = 1
                while n <= row:
                    moves.append([r, n])
                    n += 1
            r += 1

        return moves
        
    def result(self, state, move):
        # move = (1,3), remove one from 1st row
        new_state = []
        moves = []
        i = 0
        r = 0
        
        for row in state[2]:
            if move[0] == i:
                new_state.append(row - move[1])
            else:
                new_state.append(row)
            i += 1

        for row in new_state:
            if row != 0:
                n = 1
                while n <= row:
                    moves.append([r, n])
                    n += 1
            r += 1

        return new_state, moves     

    def terminal_test(self, state):
        r = 0
        if r == len(state[0]):
            return True
        else:
            while r < len(state[0]):
                if r == len(state[0]):
                    return True
                else:
                    r += 1