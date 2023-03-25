"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    tmp = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                tmp += 1
            if board[i][j] == O:
                tmp -= 1
    return X if tmp == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    ret = []
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                ret.append((i, j))
    return ret


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    x, y = action
    if x < 0 or x > 2 or y < 0 or y > 2 or board[x][y] is not EMPTY:
        raise ValueError
    nb = copy.deepcopy(board)
    p = player(board)
    nb[x][y] = p
    return nb


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for p in [X, O]:
        diag, rdig = True, True
        for i in range(3):
            flag = True
            for j in range(3):
                if board[i][j] != p:
                    flag = False
                    break
            if flag:
                return p
            flag = True
            for j in range(3):
                if board[j][i] != p:
                    flag = False
                    break
            if flag:
                return p
            if board[i][i] != p:
                diag = False
                # break
            if board[i][2-i] != p:
                rdig = False
                # break
        if diag or rdig:
            return p
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return len(actions(board)) == 0 or winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if not terminal(board):
        return 0
    return 1 if winner(board) == X else -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    def next_player(role):
        return O if role == X else X
    
    def next_mode(mode):
        return 'min' if mode == 'max' else 'max'
    
    def dfs(board, role, mode):
        if terminal(board):
            return [utility(board), None]
        
        steps = actions(board)
        sc, a = None, None
        for s in steps:
            nb = result(board, s)
            score = dfs(nb, next_player(role), next_mode(mode))[0]

            if mode == 'max':
                if sc is None or score > sc:
                    sc = score
                    a = s
                    if sc == 1:
                        return [sc, a]
            else:
                if sc is None or score < sc:
                    sc = score
                    a = s
                    if sc == -1:
                        return [sc, a]
        
        return [sc, a]
    
    p = player(board)
    if p == X:
        return dfs(board, p, 'max')[1]
    else:
        return dfs(board, p, 'min')[1]

