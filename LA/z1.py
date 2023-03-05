from re import split, search, sub
from math import inf
from copy import deepcopy


def get_opponent_symbol(symbol):
    if symbol == 'O':
        return 'X'
    elif symbol == 'X':
        return 'O'


def count_possibilities_to_win(symbol, state):
    possibilities = 0

    if symbol == f'X':
        regex1 = f'X'
        regex2 = f'XX'
        regex3 = f'X XX'
        regex4 = f'XX X'
        regex5 = f'XX XX'
        regex6 = f'X X'
    else:
        regex1 = f'O'
        regex2 = f'OO'
        regex3 = f'O OO'
        regex4 = f'OO O'
        regex5 = f'OO OO'
        regex6 = f'O O'

    position = search(state, regex1)

    if position is not None:
        if position.start() == 0 or position.start() == 4:
            possibilities += 1
        else:
            possibilities += 2

    position = search(state, regex2)

    if position is not None:
        possibilities += 1

    position = search(state, regex3)

    if position is not None:
        if position.start() == 0:
            possibilities += 1
        else:
            possibilities += 2

    position = search(state, regex4)

    if position is not None:
        if position.start() == 0:
            possibilities += 2
        else:
            possibilities += 1

    position = search(state, regex5)

    if position is not None:
        possibilities += 1

    position = search(state, regex6)

    if position is not None:
        if position.start() == 0 or position.start() == 2:
            possibilities += 1
        else:
            possibilities += 2

    return possibilities


def count_opponents_symbols(opponent_symbol, state):
    opponent_symbols_count = 0

    for symbol in state:
        if symbol == opponent_symbol:
            opponent_symbols_count += 1

    return opponent_symbols_count


def get_opponent_symbol_position(opponent_symbol, state):
    for i in range(0, 5):
        if state[i] == opponent_symbol:
            return i


def check_for_win_possibilities_in_rows(symbol, game_state):
    possibilities_count = 0

    for i in range(0, 5):
        row_as_string = ''.join(game_state[i])

        possibilities_count += count_possibilities_to_win(symbol, row_as_string)

    return possibilities_count


def check_for_win_possibilities_in_columns(symbol, game_state):
    possibilities_count = 0
    for i in range(0, 5):
        column_as_string = f''
        for j in range(0, 5):
            column_as_string += game_state[j][i]

        possibilities_count += count_possibilities_to_win(symbol, column_as_string)

    return possibilities_count


def check_for_win_possibilities_in_diagonals(symbol, game_state):
    diagonal_as_string = f''
    possibilities_count = 0

    for i in range(0, 5):
        diagonal_as_string += game_state[i][i]

    possibilities_count += count_possibilities_to_win(symbol, diagonal_as_string)

    diagonal_as_string = f''

    for i in range(4, -1, -1):
        diagonal_as_string += game_state[i][4 - i]

    possibilities_count += count_possibilities_to_win(symbol, diagonal_as_string)

    return possibilities_count


def check_for_double_symbol_in_upper_diagonal(diagonal_state, symbol):
    if symbol == 'X':
        regex = f'XX'
    else:
        regex = f'OO'

    position = search(regex, diagonal_state)

    if position == 1:
        return True

    return False


def check_for_win_in_upper_diagonals(symbol, game_state):
    opponent_symbol = get_opponent_symbol(symbol)

    possibilities_count = 0
    opponent_symbol_count = 0

    diagonal_state = f''

    for i in range(1, 5):
        if game_state[i][i - 1] == opponent_symbol:
            opponent_symbol_count += 1

        diagonal_state += game_state[i][i - 1]

    if opponent_symbol_count <= 0 and not check_for_double_symbol_in_upper_diagonal(diagonal_state, symbol):
        possibilities_count += 1

    opponent_symbol_count = 0
    diagonal_state = f''

    for i in range(0, 4):
        if game_state[i][i + 1] == opponent_symbol:
            opponent_symbol_count += 1

        diagonal_state += game_state[i][i + 1]

    if opponent_symbol_count <= 0 and not check_for_double_symbol_in_upper_diagonal(diagonal_state, symbol):
        possibilities_count += 1

    opponent_symbol_count = 0
    diagonal_state = f''

    for i in range(3, -1, -1):
        if game_state[i][3 - i] == opponent_symbol:
            opponent_symbol_count += 1

        diagonal_state += game_state[i][3 - i]

    if opponent_symbol_count <= 0 and not check_for_double_symbol_in_upper_diagonal(diagonal_state, symbol):
        possibilities_count += 1

    opponent_symbol_count = 0
    diagonal_state = f''

    for i in range(4, 0, -1):
        if game_state[i][4 - i + 1] == opponent_symbol:
            opponent_symbol_count += 1

        diagonal_state += game_state[i][4 - i + 1]

    if opponent_symbol_count <= 0 and not check_for_double_symbol_in_upper_diagonal(diagonal_state, symbol):
        possibilities_count += 1

    return possibilities_count


def get_positions_of_double_opponent_symbols(state, symbol):
    if symbol == 'O':
        regex1 = 'XX'
        regex2 = 'X X'
    elif symbol == 'X':
        regex1 = 'OO'
        regex2 = 'O O'

    positions1 = []
    positions2 = []

    state_copy = deepcopy(state)

    position = search(regex1, state_copy)

    while position is not None:
        positions1.append(position.start())
        state_copy = sub(regex1, '  ', state_copy)

        position = search(regex1, state_copy)

    position = search(regex2, state)

    while position is not None:
        positions2.append(position.start())
        state = sub(regex2, '   ', state)

        position = search(regex2, state)

    return positions1, positions2


def count_possibilities_from_position_lists(positions1, positions2):
    possibilities = 0

    for i in positions1:
        if i == 0 or i == 4:
            possibilities += 1
        else:
            possibilities += 2

    for _ in positions2:
        possibilities += 1

    return possibilities


def count_blocked_fields(symbol, game_state):
    blocked_fields = 0

    for i in range(0, 5):
        row_as_string = ' '.join(game_state[i])

        pos1, pos2 = get_positions_of_double_opponent_symbols(row_as_string, symbol)
        blocked_fields += count_possibilities_from_position_lists(pos1, pos2)

    for i in range(0, 5):
        column_as_string = f''
        for j in range(0, 5):
            column_as_string += game_state[j][i]

        pos1, pos2 = get_positions_of_double_opponent_symbols(column_as_string, symbol)
        blocked_fields += count_possibilities_from_position_lists(pos1, pos2)

    diagonal = f''

    for i in range(0, 5):
        diagonal += game_state[i][i]

    pos1, pos2 = get_positions_of_double_opponent_symbols(diagonal, symbol)
    blocked_fields += count_possibilities_from_position_lists(pos1, pos2)

    diagonal = f''

    for i in range(1, 5):
        diagonal += game_state[i][i - 1]

    pos1, pos2 = get_positions_of_double_opponent_symbols(diagonal, symbol)
    blocked_fields += count_possibilities_from_position_lists(pos1, pos2)

    diagonal = f''

    for i in range(0, 4):
        diagonal += game_state[i][i + 1]

    pos1, pos2 = get_positions_of_double_opponent_symbols(diagonal, symbol)
    blocked_fields += count_possibilities_from_position_lists(pos1, pos2)

    diagonal = f''

    for i in range(2, 5):
        diagonal += game_state[i][i - 2]

    pos1, pos2 = get_positions_of_double_opponent_symbols(diagonal, symbol)
    blocked_fields += count_possibilities_from_position_lists(pos1, pos2)

    diagonal = f''

    for i in range(0, 3):
        diagonal += game_state[i][i + 2]

    pos1, pos2 = get_positions_of_double_opponent_symbols(diagonal, symbol)
    blocked_fields += count_possibilities_from_position_lists(pos1, pos2)

    diagonal = f''

    for i in range(0, 5):
        diagonal += game_state[4 - i][i]

    pos1, pos2 = get_positions_of_double_opponent_symbols(diagonal, symbol)
    blocked_fields += count_possibilities_from_position_lists(pos1, pos2)

    diagonal = f''

    for i in range(3, -1, -1):
        diagonal += game_state[i][3 - i]

    pos1, pos2 = get_positions_of_double_opponent_symbols(diagonal, symbol)
    blocked_fields += count_possibilities_from_position_lists(pos1, pos2)

    diagonal = f''

    for i in range(4, 0, -1):
        diagonal += game_state[i][4 - i + 1]

    pos1, pos2 = get_positions_of_double_opponent_symbols(diagonal, symbol)
    blocked_fields += count_possibilities_from_position_lists(pos1, pos2)

    diagonal = f''

    for i in range(2, -1, -1):
        diagonal += game_state[i][2 - i]

    pos1, pos2 = get_positions_of_double_opponent_symbols(diagonal, symbol)
    blocked_fields += count_possibilities_from_position_lists(pos1, pos2)

    diagonal = f''

    for i in range(4, 1, -1):
        diagonal += game_state[i][4 - i + 2]

    pos1, pos2 = get_positions_of_double_opponent_symbols(diagonal, symbol)
    blocked_fields += count_possibilities_from_position_lists(pos1, pos2)

    return blocked_fields


def evaluation_function(current_player, game_state):
    opponent_symbol = get_opponent_symbol(current_player)

    number_of_blocked_fields = count_blocked_fields(current_player, game_state)

    possibilities_to_win_in_rows = check_for_win_possibilities_in_rows(current_player, game_state)
    possibilities_to_win_in_columns = check_for_win_possibilities_in_columns(current_player, game_state)
    possibilities_to_win_in_diagonals = check_for_win_possibilities_in_diagonals(current_player, game_state)
    possibilities_to_win_in_upper_diagonals = check_for_win_in_upper_diagonals(current_player, game_state)

    possibilities_to_win = possibilities_to_win_in_rows + possibilities_to_win_in_columns + possibilities_to_win_in_diagonals + possibilities_to_win_in_upper_diagonals

    opponent_win_in_rows = check_for_win_possibilities_in_rows(opponent_symbol, game_state)
    opponent_win_in_columns = check_for_win_possibilities_in_columns(opponent_symbol, game_state)
    opponent_win_in_diagonals = check_for_win_possibilities_in_diagonals(opponent_symbol, game_state)
    opponent_win_in_upper_diagonals = check_for_win_in_upper_diagonals(opponent_symbol, game_state)

    possibilities_to_win_for_opponent = opponent_win_in_rows + opponent_win_in_columns + opponent_win_in_diagonals + opponent_win_in_upper_diagonals

    return possibilities_to_win - possibilities_to_win_for_opponent + 0.7*number_of_blocked_fields


def check_if_move_is_possible(i, j, game_state):
    if game_state[i][j] == 'O' or game_state[i][j] == 'X':
        return False
    return True


def put_symbol(row, column, symbol, game_state):
    game_state[row][column] = symbol


def clear_symbol(row, column, game_state):
    game_state[row][column] = f''


def mini_max(machine_symbol, human_symbol, game_state, is_maximizing, search_depth):
    if search_depth == 0:
        maybe_winner = check_for_winner(game_state)

        if maybe_winner is not None:
            if maybe_winner == machine_symbol:
                return inf
            elif maybe_winner == human_symbol:
                return -inf

        if is_maximizing:
            return evaluation_function(machine_symbol, game_state)
        else:
            return evaluation_function(human_symbol, game_state)

    if is_maximizing:
        best_score = -inf

        for i in range(0, 5):
            for j in range(0, 5):
                if check_if_move_is_possible(i, j, game_state):
                    put_symbol(i, j, machine_symbol, game_state)

                    maybe_winner = check_for_winner(game_state)

                    if maybe_winner is not None:
                        if maybe_winner == human_symbol:
                            clear_symbol(i, j, game_state)
                            return -inf
                        elif maybe_winner == machine_symbol:
                            clear_symbol(i, j, game_state)
                            return inf

                    score = mini_max(machine_symbol, human_symbol, game_state, False, search_depth - 1)
                    clear_symbol(i, j, game_state)

                    best_score = max(score, best_score)

        return best_score

    else:
        best_score = inf

        for i in range(0, 5):
            for j in range(0, 5):
                if check_if_move_is_possible(i, j, game_state):
                    put_symbol(i, j, human_symbol, game_state)

                    maybe_winner = check_for_winner(game_state)

                    if maybe_winner is not None:
                        if maybe_winner == machine_symbol:
                            clear_symbol(i, j, game_state)
                            return inf
                        elif maybe_winner == human_symbol:
                            clear_symbol(i, j, game_state)
                            return -inf

                    score = mini_max(machine_symbol, human_symbol, game_state, True, search_depth - 1)
                    clear_symbol(i, j, game_state)

                    best_score = min(score, best_score)

        return best_score


def machine_move(machine_symbol, human_symbol, game_state, searching_depth):
    r, c = None, None
    best_score = -inf

    for i in range(0, 5):
        for j in range(0, 5):
            if check_if_move_is_possible(i, j, game_state):
                put_symbol(i, j, machine_symbol, game_state)
                score = mini_max(machine_symbol, human_symbol, game_state, True, searching_depth)
                clear_symbol(i, j, game_state)

                if score >= best_score:
                    best_score, r, c = score, i, j

    put_symbol(r, c, machine_symbol, game_state)


def check_for_tie(game_state):
    for i in range(0, 5):
        if '' in game_state[i]:
            return False
    return True


def check_if_symbol_wins_or_looses(symbols, symbol_to_check):
    if symbol_to_check == f'O':
        groups = split('X| ', symbols)
    else:
        groups = split('O| ', symbols)

    for group in groups:
        if group == '':
            continue
        elif len(group) == 3:
            if symbol_to_check == 'O':
                return 'X'
            elif symbol_to_check == 'X':
                return 'O'
        elif len(group) == 4:
            return symbol_to_check

    return None


def check_for_winner_in_rows(game_state, symbol_to_check):
    for i in range(0, 5):
        symbols = f''
        for j in range(0, 5):
            if game_state[i][j] == '':
                symbols += f' '
            else:
                symbols += game_state[i][j]

        answer = check_if_symbol_wins_or_looses(symbols, symbol_to_check)

        if answer is not None:
            return answer

    return None


def check_for_winner_in_columns(game_state, symbol_to_check):
    for i in range(0, 5):
        symbols = f''
        for j in range(0, 5):
            if game_state[j][i] == '':
                symbols += f' '
            else:
                symbols += game_state[j][i]

        answer = check_if_symbol_wins_or_looses(symbols, symbol_to_check)

        if answer is not None:
            return answer

    return None


def check_for_winner_in_diagonals(game_state, symbol_to_check):
    symbols = f''

    for i in range(0, 5):
        if game_state[i][i] == '':
            symbols += f' '
        else:
            symbols += game_state[i][i]

    answer = check_if_symbol_wins_or_looses(symbols, symbol_to_check)

    if answer is not None:
        return answer

    symbols = f''

    for i in range(1, 5):
        if game_state[i][i - 1] == '':
            symbols += f' '
        else:
            symbols += game_state[i][i - 1]

    answer = check_if_symbol_wins_or_looses(symbols, symbol_to_check)

    if answer is not None:
        return answer

    symbols = f''

    for i in range(0, 4):
        if game_state[i][i + 1] == '':
            symbols += f' '
        else:
            symbols += game_state[i][i + 1]

    answer = check_if_symbol_wins_or_looses(symbols, symbol_to_check)

    if answer is not None:
        return answer

    symbols = f''

    for i in range(2, 5):
        if game_state[i][i - 2] == '':
            symbols += f' '
        else:
            symbols += game_state[i][i - 2]

    answer = check_if_symbol_wins_or_looses(symbols, symbol_to_check)

    if answer is not None:
        return answer

    symbols = f''

    for i in range(0, 3):
        if game_state[i][i + 2] == '':
            symbols += f' '
        else:
            symbols += game_state[i][i + 2]

    answer = check_if_symbol_wins_or_looses(symbols, symbol_to_check)

    if answer is not None:
        return answer

    symbols = f''

    for i in range(0, 5):
        if game_state[4 - i][i] == '':
            symbols += f' '
        else:
            symbols += game_state[4 - i][i]

    answer = check_if_symbol_wins_or_looses(symbols, symbol_to_check)

    if answer is not None:
        return answer

    symbols = f''

    for i in range(3, -1, -1):
        if game_state[i][3 - i] == '':
            symbols += f' '
        else:
            symbols += game_state[i][3 - i]

    answer = check_if_symbol_wins_or_looses(symbols, symbol_to_check)

    if answer is not None:
        return answer

    symbols = f''

    for i in range(4, 0, -1):
        if game_state[i][4 - i + 1] == '':
            symbols += f' '
        else:
            symbols += game_state[i][4 - i + 1]

    answer = check_if_symbol_wins_or_looses(symbols, symbol_to_check)

    if answer is not None:
        return answer

    symbols = f''

    for i in range(2, -1, -1):
        if game_state[i][2 - i] == '':
            symbols += f' '
        else:
            symbols += game_state[i][2 - i]

    answer = check_if_symbol_wins_or_looses(symbols, symbol_to_check)

    if answer is not None:
        return answer

    symbols = f''

    for i in range(4, 1, -1):
        if game_state[i][4 - i + 2] == '':
            symbols += f' '
        else:
            symbols += game_state[i][4 - i + 2]

    answer = check_if_symbol_wins_or_looses(symbols, symbol_to_check)

    if answer is not None:
        return answer

    return None


def check_for_winner(game_state):
    x_answer = check_for_winner_in_rows(game_state, 'X')
    o_answer = check_for_winner_in_rows(game_state, 'O')

    if x_answer is not None:
        return x_answer
    elif o_answer is not None:
        return o_answer

    x_answer = check_for_winner_in_columns(game_state, 'X')
    o_answer = check_for_winner_in_columns(game_state, 'O')

    if x_answer is not None:
        return x_answer
    elif o_answer is not None:
        return o_answer

    x_answer = check_for_winner_in_diagonals(game_state, 'X')
    o_answer = check_for_winner_in_diagonals(game_state, 'O')

    if x_answer is not None:
        return x_answer
    elif o_answer is not None:
        return o_answer

    return None


def display_board(game_state):
    board_as_string = f''
    row_as_string = f''

    for i in range(0, 5):
        board_as_string += f'--- ' * 5
        board_as_string += f'\n'

        for j in range(0, 5):
            if game_state[i][j] == '':
                symbol = f'-'
            else:
                symbol = game_state[i][j]

            if j == 4:
                row_as_string += f'| {symbol} |'
                continue

            row_as_string += f'| {symbol} '

        board_as_string += row_as_string
        board_as_string += f'\n'
        row_as_string = f''

    board_as_string += f'--- ' * 5

    print(board_as_string)
    print(f'\n')


def main():
    game_board = [['' for _ in range(0, 5)] for _ in range(0, 5)]
    machine_symbol = None
    human_player_symbol = str(input(f'> Witaj w programie do grania w kółko i krzyżyk ! Wybierz symbol (O/X): '))
    winner = None

    while True:
        if human_player_symbol == 'O' or human_player_symbol == 'X':
            break
        else:
            human_player_symbol = str(input(f'> Wprowadzono nieprawidłowy symbol. Spróbuj jeszcze raz (O/X): '))

    if human_player_symbol == f'O':
        machine_symbol = f'X'
        print(f'> Jesteś {human_player_symbol}, więc ja jestem X !')
    elif human_player_symbol == f'X':
        machine_symbol = f'O'
        print(f'> Jesteś {human_player_symbol}, więc ja jestem O !')

    searching_depth = int(input(f'> Podaj głębokość drzewa przeszukiwań: '))

    print(f'> Rozpoczynamy grę !')

    display_board(game_board)

    if human_player_symbol == 'X':
        print(f'> Podaj swój ruch: ')
        row = int(input(f'> Wiersz (0-4): '))
        column = int(input(f'> Kolumna (0-4): '))

        put_symbol(row, column, human_player_symbol, game_board)

        display_board(game_board)

    while True:
        machine_move(machine_symbol, human_player_symbol, game_board, searching_depth)

        display_board(game_board)

        winner = check_for_winner(game_board)
        is_tie = check_for_tie(game_board)

        if winner is not None:
            print(f'> Koniec ! Zwycięzcą jest {winner}')
            break

        if is_tie:
            print('f> Koniec ! Jest remis...')
            break

        print(f'> Podaj swój ruch: ')
        row = int(input(f'> Wiersz (0-4): '))
        column = int(input(f'> Kolumna (0-4): '))

        put_symbol(row, column, human_player_symbol, game_board)

        display_board(game_board)

        winner = check_for_winner(game_board)
        is_tie = check_for_tie(game_board)

        if winner is not None:
            print(f'> Koniec ! Zwycięzcą jest {winner}')
            break
        if is_tie:
            print('f> Koniec ! Jest remis...')
            break


main()
