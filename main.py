import imp
import time


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

# Student SHOULD implement this function to change current state to new state properly
def doit(move, state):
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


# 4 : r r r r r
# 3 : r . . . r
# 2 : b . . . r
# 1 : b . . . b
# 0 : b b b b b
#     0 1 2 3 4
# ======================================================================

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
        return

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

    print("Game Over")
    if curr_player == a:
        print("The Winner is:", student_b, 'red')
    else:
        print("The Winner is:", student_a, 'blue')


play("co_ganh", "co_ganh")
