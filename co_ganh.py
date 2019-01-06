SIZE = 5

NEXT_STEP_ODD = [(-1, 0), (0, -1), (0, 1), (1, 0)]

NEXT_STEP_EVEN = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

CORNER_POSITION = [(0, 0), (4, 4), (0, 4), (4, 0)]

NOTHING = -1

ROW = 0

COLUMN = 1

ROW_COLUMN = 2

ROW_COLUMN_CROSS = 3


def list_possible_next_position(state, current_position):
    if state[current_position[0]][current_position[1]] == '.':
        return []
    list_possible = []
    total = current_position[0] + current_position[1]
    if total % 2 == 0:
        steps = NEXT_STEP_EVEN
    else:
        steps = NEXT_STEP_ODD

    for step in steps:
        x = current_position[0] + step[0]
        y = current_position[1] + step[1]
        if 0 <= x < SIZE and 0 <= y < SIZE and state[x][y] == '.':
            list_possible.append((x, y))

    return list_possible


# ======================== Evaluation =========================================
def is_corner(x, y):
    for corner in CORNER_POSITION:
        if (x, y) == corner:
            return True
    return False


def can_ganh(x, y):
    if is_corner(x, y):
        return NOTHING
    if x == 0 or x == 4:
        return ROW
    elif y == 0 or y == 4:
        return COLUMN
    elif abs(x - y) == 1:
        return ROW_COLUMN
    else:
        return ROW_COLUMN_CROSS


def evaluate_ganh_by_column(state, x, y):
    if state[x - 1][y] == state[x + 1][y] and state[x - 1][y] != state[x][y]:
        return 10
    return 0


def evaluate_ganh_by_row(state, x, y):
    if state[x][y - 1] == state[x][y + 1] and state[x][y - 1] != state[x][y]:
        return 10
    return 0


def evaluate_ganh_by_cross(state, x, y):
    point = 0
    if state[x + 1][y - 1] == state[x - 1][y + 1] and state[x + 1][y - 1] != state[x][y]:
        point += 10
    if state[x - 1][y - 1] == state[x + 1][y + 1] and state[x - 1][y - 1] != state[x][y]:
        point += 10
    return point


def evaluate_ganh(state, x, y):
    point = 0
    if can_ganh(x, y) == NOTHING:
        point += 0
    elif can_ganh(x, y) == COLUMN:
        point += evaluate_ganh_by_column(state, x, y)
    elif can_ganh(x, y) == ROW:
        point += evaluate_ganh_by_row(state, x, y)
    elif can_ganh(x, y) == ROW_COLUMN:
        point += evaluate_ganh_by_column(state, x, y)
        point += evaluate_ganh_by_row(state, x, y)
    elif can_ganh(x, y) == ROW_COLUMN_CROSS:
        point += evaluate_ganh_by_column(state, x, y)
        point += evaluate_ganh_by_row(state, x, y)
        point += evaluate_ganh_by_cross(state, x, y)
    return point


def evaluate_chet(state, x, y):
    point = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '.':
                continue
            if state[i][j] != state[x][y] and list_possible_next_position(state, (i, j)) == []:
                point += 5
    return point


def evaluate(state, x, y):
    return evaluate_ganh(state, x, y) + evaluate_chet(state, x, y)


# params is
# state: current state
# x, y: coordinate of current position
def get_max_evaluate(state, x, y):
    next_positions = list_possible_next_position(state, (x, y))
    max_evaluation = 0
    for pos in next_positions:
        max_evaluation = max(max_evaluation, evaluate(state, pos[0], pos[1]))
    return max_evaluation


# params is
# state: current state
# x, y: coordinate of current position
def get_new_position(state, x, y):
    next_positions = list_possible_next_position(state, (x, y))
    max_position = (0, 0)
    max_evaluation = 0
    for pos in next_positions:
        if evaluate(state, pos[0], pos[1]) > max_evaluation:
            max_evaluation = evaluate(state, pos[0], pos[1])
            max_position = pos
    return max_position


def get_all_chessman(state, color):
    list_chessman = []
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == color:
                list_chessman.append((i, j))
    return list_chessman


def get_max_chessman(state, color):
    list_chessman = get_all_chessman(state, color)
    if len(list_chessman) == 0:
        return color
    max_evaluate = 0
    max_chessman = list_chessman[0]
    for chessman in list_chessman:
        if get_max_evaluate(state, chessman[0], chessman[1]) > max_evaluate:
            max_evaluate = get_max_evaluate(state, chessman[0], chessman[1])
            max_chessman = chessman
    return max_chessman


# ======================== Class Player =======================================
class Player:

    # student do not allow to change two first functions
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str

    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples:
    # [(row1, col1), (row2, col2)] with:
    # (row1, col1): current position of selected piece
    # (row2, col2): new position of selected piece
    def next_move(self, state):
        max_chessman = get_max_chessman(state, self.str)
        if max_chessman == self.str:
            return
        new_position = get_new_position(state, max_chessman[0], max_chessman[1])
        result = [max_chessman, new_position]
        return result
