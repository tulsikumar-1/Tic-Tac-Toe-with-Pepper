#
# class for tic tac toe 3X3 architecture

DEBUG=True
class Tic:
    EMPTY = 0
    X = 1
    O = 2
    DRAW = 0

    def __init__(self):
        self.board = [
            [Tic.EMPTY, Tic.EMPTY, Tic.EMPTY,],
            [Tic.EMPTY, Tic.EMPTY, Tic.EMPTY,],
            [Tic.EMPTY, Tic.EMPTY, Tic.EMPTY,],
        ]
        # X starts first
        self.current_player = Tic.X
    
    def reset(self):
        self.board = [
            [Tic.EMPTY, Tic.EMPTY, Tic.EMPTY,],
            [Tic.EMPTY, Tic.EMPTY, Tic.EMPTY,],
            [Tic.EMPTY, Tic.EMPTY, Tic.EMPTY,],
        ]
        # X starts first
        self.current_player = Tic.X
        
    # get current player
    def get_current_player(self):
        return self.current_player
    
    # check if a space is empty
    def is_empty(self, row, col):
        return self.board[row][col] == Tic.EMPTY
    
    # get a copy of the board
    def get_board(self):
        return [row[:] for row in self.board]

    # make move
    def move(self, row, col):
        if DEBUG: print row
        if DEBUG: print col
        if col<3 and row<3:   
                if self.board[int(row)][int(col)] != Tic.EMPTY:
        	     return False 
		self.board[row][col] = self.current_player
		self.current_player = Tic.O if self.current_player == Tic.X else Tic.X
		return True
	return False	

    # check if game is over
    def get_game_over_and_winner(self):
        return get_game_over_and_winner(self.board)    # w/o `self.` it refers to the global method outside

    # highlights tiles in a tic to show on the tablet
    def get_tic_highlights_for_tablet(self):
        return get_tic_highlights_for_tablet(self.board)    # w/o `self.` it refers to the global method outside

    # check if a player may win next move
    def player_is_threatening(self, player):
        return player_is_threatening(self.board, player)    # w/o `self.` it refers to the global method outside
    
    # print class in a pretty way
    def __str__(self):
        s = ''
        for row in self.board:
            for cell in row:
                s += ' ' + ('X' if cell == Tic.X else 'O' if cell == Tic.O else ' ')
            s += '\n'
        return s
    
    def get_board_for_tablet(self):
        s = ''
        for row in self.board:
            for cell in row:
                s += ('X' if cell == Tic.X else 'O' if cell == Tic.O else '.')
        return s

# check if game is over
def get_game_over_and_winner(board):
    # check rows
    for row in board:
        if row[0] != Tic.EMPTY and row[0] == row[1] == row[2]:
            return True, row[0]
    # check columns
    for col in range(3):
        if board[0][col] != Tic.EMPTY and board[0][col] == board[1][col] == board[2][col]:
            return True, board[0][col]
    # check diagonals
    if board[0][0] != Tic.EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return True, board[0][0]
    if board[0][2] != Tic.EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return True, board[0][2]
    
    # no one wins yet
    for row in board:
        for cell in row:
            if cell == Tic.EMPTY:
                return False, None
                
    # there is a draw
    return True, Tic.DRAW

# highlight tic
def get_tic_highlights_for_tablet(board):
    hl_matrix = [
        [False, False, False],
        [False, False, False],
        [False, False, False],
    ]

    # check rows
    for row in range(3):
        if board[row][0] != Tic.EMPTY and board[row][0] == board[row][1] == board[row][2]:
            hl_matrix[row][0] = True
            hl_matrix[row][1] = True
            hl_matrix[row][2] = True
    # check columns
    for col in range(3):
        if board[0][col] != Tic.EMPTY and board[0][col] == board[1][col] == board[2][col]:
            hl_matrix[0][col] = True
            hl_matrix[1][col] = True
            hl_matrix[2][col] = True
    # check diagonals
    if board[0][0] != Tic.EMPTY and board[0][0] == board[1][1] == board[2][2]:
        hl_matrix[0][0] = True
        hl_matrix[1][1] = True
        hl_matrix[2][2] = True
    if board[0][2] != Tic.EMPTY and board[0][2] == board[1][1] == board[2][0]:
        hl_matrix[0][2] = True
        hl_matrix[1][1] = True
        hl_matrix[2][0] = True

    # generate tablet string
    s = ''
    for row in hl_matrix:
        for cell in row:
            s += ('H' if cell else '.')
    return s

# a player threatens a win if there is a row, col or diag where two spaces have its symbol and the third is empty.
# first an aux
def set_is_threatened(tile1, tile2, tile3, player):
    return (tile1 == tile2 == player and tile3 == Tic.EMPTY) or \
           (tile2 == tile3 == player and tile1 == Tic.EMPTY) or \
           (tile3 == tile1 == player and tile2 == Tic.EMPTY)
# then the real thing
def player_is_threatening(board, player):
    # check rows
    for row in board:
        if set_is_threatened(row[0], row[1], row[2], player):
            return True
    # check columns
    for col in range(3):
        if set_is_threatened(board[0][col], board[1][col], board[2][col], player):
            return True
    # check diagonals
    if set_is_threatened(board[0][0], board[1][1], board[2][2], player):
        return True
    if set_is_threatened(board[0][2], board[1][1], board[2][0], player):
        return True
    # no threats detected here
    return False


# test
if __name__ == "__main__":
    tic = Tic()

    print "Playing a match"
    # play a match
    while True:
        print tic
        row = int(input('row: '))
        col = int(input('col: '))
        if not tic.move(row, col):
            print 'invalid move'
        game_over, winner = tic.get_game_over_and_winner()
        if game_over:
            if winner == Tic.DRAW:
                print 'draw'
            else:
                print 'winner: ' + ('X' if winner == Tic.X else 'O')
            break
    print tic

