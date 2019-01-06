import imp
import time
from co_ganh import is_chet


# ======================================================================


def board_print(board, move=[], num=0):
    print("====== The current board(", num, ")is (after move): ======")
    if move:
        print("move = ", move)
    for i in [4, 3, 2, 1, 0]:
        print(i, ":", end=" ")
        for j in range(5):
            print(board[i][j], end=" ")
        print()
    print("   ", 0, 1, 2, 3, 4)
    print("")


def board_copy(board):
    new_board = [[]] * 5
    for i in range(5):
        new_board[i] = [] + board[i]
    return new_board


# ======================================================================
CORNER_POSITION = [(0, 0), (4, 4), (0, 4), (4, 0)]


# Check game over and return winner if true
def game_over(state):
    r = 0
    b = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 'b':
                b += 1
            elif state[i][j] == 'r':
                r += 1
    if r == 0:
        return 'b'
    elif b == 0:
        return 'r'
    else:
        return 'not'


# swap state between current position and new position
# move[0] is current position
# move[1] is new position
def swap_position(state, move):
    t = state[move[0][0]][move[0][1]]
    state[move[0][0]][move[0][1]] = state[move[1][0]][move[1][1]]
    state[move[1][0]][move[1][1]] = t


# check corner position
def is_corner(pos):
    for corner in CORNER_POSITION:
        if pos == corner:
            return True
    return False


# "ganh" by column
def ganh_by_column(state, move):
    (x, y) = move[1]
    if state[x - 1][y] != '.' and state[x - 1][y] == state[x + 1][y] and state[x - 1][y] != state[x][y]:
        print("ganh_by_column")
        state[x - 1][y] = state[x][y]
        state[x + 1][y] = state[x][y]
    return


# "ganh" by row
def ganh_by_row(state, move):
    (x, y) = move[1]
    if state[x][y - 1] != '.' and state[x][y - 1] == state[x][y + 1] and state[x][y - 1] != state[x][y]:
        print("ganh_by_row")
        state[x][y - 1] = state[x][y]
        state[x][y + 1] = state[x][y]
    return


# "ganh" by cross
def ganh_by_cross(state, move):
    (x, y) = move[1]
    # "ganh" by cross \
    if state[x + 1][y - 1] != '.' and state[x + 1][y - 1] == state[x - 1][y + 1] and state[x + 1][y - 1] != state[x][y]:
        print("ganh by cross \\")
        state[x + 1][y - 1] = state[x][y]
        state[x - 1][y + 1] = state[x][y]
    # "ganh" by cross /
    if state[x - 1][y - 1] != '.' and state[x - 1][y - 1] == state[x + 1][y + 1] and state[x - 1][y - 1] != state[x][y]:
        print("ganh by cross /")
        state[x - 1][y - 1] = state[x][y]
        state[x + 1][y + 1] = state[x][y]
    return


# change color if "ganh"
def change_color_if_ganh(state, move):
    if is_corner(move[1]):
        return
    (x, y) = move[1]
    if x == 0 or x == 4:
        ganh_by_row(state, move)
    elif y == 0 or y == 4:
        ganh_by_column(state, move)
    elif abs(x - y) == 1:
        ganh_by_row(state, move)
        ganh_by_column(state, move)
    else:
        ganh_by_column(state, move)
        ganh_by_row(state, move)
        ganh_by_cross(state, move)
    return


# change color if "chet"
def change_color_if_chet(state, move):
    (x, y) = move[1]
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != '.' and state[i][j] != state[x][y] and is_chet(state, i, j):
                print("chet ", i, j)
                state[i][j] = state[x][y]
    return


# ======================================================================

# Student SHOULD implement this function to change current state to new state properly
def doit(move, state):
    swap_position(state, move)
    change_color_if_ganh(state, move)
    change_color_if_chet(state, move)
    new_state = board_copy(state)
    return new_state


# ======================================================================

Initial_Board = [
    ['b', 'b', 'b', 'b', 'b'], \
    ['b', '.', '.', '.', 'b'], \
    ['b', '.', '.', '.', 'r'], \
    ['r', '.', '.', '.', 'r'], \
    ['r', 'r', 'r', 'r', 'r'], \
    ]

# Initial_Board = [
#     ['b', '.', '.', '.', '.'], \
#     ['r', 'b', '.', '.', '.'], \
#     ['b', '.', '.', '.', '.'], \
#     ['.', '.', '.', '.', '.'], \
#     ['.', '.', '.', '.', 'b'], \
#     ]


# 4 : r r r r r
# 3 : r . . . r
# 2 : b . . . r
# 1 : b . . . b
# 0 : b b b b b
#     0 1 2 3 4
# ======================================================================

def play(student_a, student_b, start_state=Initial_Board):
    player_a = imp.load_source(student_a, student_a + ".py")
    player_b = imp.load_source(student_b, student_b + ".py")

    a = player_a.Player('b')
    b = player_b.Player('r')

    curr_player = a
    state = start_state

    board_num = 0

    board_print(state)

    while True:
        print("It is ", curr_player, "'s turn")

        start = time.time()
        move = curr_player.next_move(state)
        elapse = time.time() - start

        # print(move)

        if not move:
            break

        print("The move is : ", move, end=" ")
        print(" (in %.2f ms)" % (elapse * 1000), end=" ")
        if elapse > 3.0:
            print(" ** took more than three second!!", end=" ")
            break
        print()
        # check_move
        state = doit(move, state)

        board_num += 1
        board_print(state, num=board_num)

        if curr_player == a:
            curr_player = b
        else:
            curr_player = a
        #
        # if board_num == 4:
        #     break

    print("Game Over")
    if curr_player == a:
        print("The Winner is:", student_b, 'red')
    else:
        print("The Winner is:", student_a, 'blue')


play("co_ganh", "co_ganh")
