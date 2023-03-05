from random import shuffle

NUMBER_OF_PUZZLE_ROWS = 4
NUMBER_OF_PUZZLE_COLUMNS = 4
GOAL_STATE = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.state == other.state

    def print_node_state(self):
        puzzle_string = '—' * 13 + '\n'
        for i in range(NUMBER_OF_PUZZLE_ROWS):
            for j in range(NUMBER_OF_PUZZLE_COLUMNS):
                puzzle_string += '│{0: >2}'.format(str(self.state[i][j]))
                if j == NUMBER_OF_PUZZLE_COLUMNS - 1:
                    puzzle_string += '│\n'

        puzzle_string += '—' * 13 + '\n'
        print(puzzle_string)


def compute_solution_length(end_node):
    path_length = 0
    current_node = end_node

    while current_node is not None:
        current_node = current_node.parent
        path_length += 1

    return path_length


def print_solution(end_node):
    list_of_nodes = []
    current_node = end_node

    while current_node is not None:
        list_of_nodes.append(current_node)
        current_node = current_node.parent

    list_of_nodes.reverse()

    for node in list_of_nodes:
        node.print_node_state()


def get_number_of_inversions(state):
    flatten_state_copy = [number for sublist in state for number in sublist if number != 0]

    n = len(flatten_state_copy)
    inversions_count = 0

    for i in range(0, n):
        for j in range(i + 1, n):
            if flatten_state_copy[i] > flatten_state_copy[j]:
                inversions_count += 1

    return inversions_count


def get_element_coordinates(element, board):
    for i in range(0, NUMBER_OF_PUZZLE_ROWS):
        for j in range(0, NUMBER_OF_PUZZLE_COLUMNS):
            if board[i][j] == element:
                return i, j

    return None, None


def check_instance_solvability(puzzle_instance):
    empty_place_x, empty_place_y = get_element_coordinates(0, puzzle_instance)

    row_number_from_bottom = NUMBER_OF_PUZZLE_ROWS - empty_place_y
    inversions_count = get_number_of_inversions(puzzle_instance)

    if (inversions_count % 2 == 0 and row_number_from_bottom % 2 != 0) or (
            inversions_count % 2 != 0 and row_number_from_bottom % 2 == 0):
        return True

    return False


def swap_elements(state, x, y, dx, dy):
    state_copy = [list(sublist) for sublist in state]

    state_copy[x][y], state_copy[x + dx][y + dy] = state_copy[x + dx][y + dy], state_copy[x][y]

    return state_copy


def get_node_neighbours(current_node):
    neighbours_list = []

    current_state = current_node.state
    empty_x, empty_y = get_element_coordinates(0, current_state)

    if empty_x > 0:
        new_state = swap_elements(current_state, empty_x, empty_y, -1, 0)

        new_node = Node(new_state, current_node)
        neighbours_list.append(new_node)
    if empty_x < NUMBER_OF_PUZZLE_ROWS - 1:
        new_state = swap_elements(current_state, empty_x, empty_y, 1, 0)

        new_node = Node(new_state, current_node)
        neighbours_list.append(new_node)
    if empty_y > 0:
        new_state = swap_elements(current_state, empty_x, empty_y, 0, -1)

        new_node = Node(new_state, current_node)
        neighbours_list.append(new_node)
    if empty_y < NUMBER_OF_PUZZLE_COLUMNS - 1:
        new_state = swap_elements(current_state, empty_x, empty_y, 0, 1)

        new_node = Node(new_state, current_node)
        neighbours_list.append(new_node)

    return neighbours_list


def heuristic_misplaced_elements(state):
    number_of_misplaced_elements = 0

    for i in range(0, NUMBER_OF_PUZZLE_ROWS):
        for j in range(0, NUMBER_OF_PUZZLE_COLUMNS):
            if state[i][j] != GOAL_STATE[i][j]:
                number_of_misplaced_elements += 1

    return number_of_misplaced_elements


def heuristic_manhattan_distance(state):
    sum_of_taxicab_distances = 0

    for i in range(0, NUMBER_OF_PUZZLE_ROWS):
        for j in range(0, NUMBER_OF_PUZZLE_COLUMNS):
            number = state[i][j]

            correct_x, correct_y = get_element_coordinates(number, GOAL_STATE)

            sum_of_taxicab_distances += (abs(i - correct_x) + abs(j - correct_y))

    return sum_of_taxicab_distances


def generate_example_instance():
    flag = False
    example_node = None

    while not flag:
        state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15]]

        for i in range(1, len(state)):
            shuffle(state[i])

        state[3].append(0)

        example_node = Node(state, None)

        flag = check_instance_solvability(state)

    return example_node


def solve_puzzle(initial_node, heuristic_function=1):
    if heuristic_function == 1:
        heuristic_evaluation = heuristic_manhattan_distance(initial_node.state)

        initial_node.f = heuristic_evaluation
        initial_node.h = heuristic_evaluation
    else:
        heuristic_evaluation = heuristic_misplaced_elements(initial_node.state)

        initial_node.f = heuristic_evaluation
        initial_node.h = heuristic_evaluation

    open_list = [initial_node]
    closed_list = []
    number_of_visited_states = 0

    while open_list:
        open_list.sort()

        current_node = open_list.pop(0)

        if current_node.state == GOAL_STATE:
            return True, number_of_visited_states, current_node

        if current_node in closed_list:
            continue

        for neighbour_node in get_node_neighbours(current_node):

            if neighbour_node in closed_list:
                continue

            if heuristic_function == 1:
                heuristic_evaluation = heuristic_manhattan_distance(neighbour_node.state)

                neighbour_node.h = heuristic_evaluation
                neighbour_node.f = neighbour_node.h
            else:
                heuristic_evaluation = heuristic_misplaced_elements(neighbour_node.state)

                neighbour_node.h = heuristic_evaluation
                neighbour_node.f = neighbour_node.h

            open_list.append(neighbour_node)

        closed_list.append(current_node)
        number_of_visited_states += 1

    return False, None, None


def print_heuristic_stats(heuristic_stats):
    first_heuristic_usages = heuristic_stats['first'][0]
    second_heuristic_usages = heuristic_stats['second'][0]

    if first_heuristic_usages == 0:
        print(f'> Nie użyto pierwszej heurystyki (suma odległości Manhattan)...')
    else:
        visited_states_avg = heuristic_stats['first'][1]/first_heuristic_usages
        path_length_avg = heuristic_stats['first'][2]/first_heuristic_usages

        print(f'> Wyniki dla pierwszej heurystyki: ')
        print(f' \n')

        print(f'> Liczba użyć (1): {first_heuristic_usages}')
        print(f'> Średnia liczba odwiedzonych stanów (1): {visited_states_avg}')
        print(f'> Średnia długość ścieżki do rozwiązania (1): {path_length_avg}')

    if second_heuristic_usages == 0:
        print(f'> Nie użyto drugiej heurystyki (liczba elementów nie na miejscu)...')
    else:
        visited_states_avg = heuristic_stats['second'][1] / second_heuristic_usages
        path_length_avg = heuristic_stats['second'][2] / second_heuristic_usages

        print(f'> Wyniki dla drugiej heurystyki: ')
        print(f' \n')

        print(f'> Liczba użyć (2): {second_heuristic_usages}')
        print(f'> Średnia liczba odwiedzonych stanów (2): {visited_states_avg}')
        print(f'> Średnia długość ścieżki do rozwiązania (2): {path_length_avg}')


def main():
    heuristic_stats = {'first': [0, 0, 0], 'second': [0, 0, 0]}

    print(f'> Witaj w programie do rozwiązywania piętnastki ! s - rozwiąż wygenerowany egzemplarz zagadki, e - zakończ')

    while True:
        command = str(input(f'> Komenda: '))

        if command == 's':
            example_node = generate_example_instance()

            print(f'> Wygenerowany egzemplarz zagadki: ')

            example_node.print_node_state()

            heuristic_function = int(input(f'> Wybierz funkcje heurystyczną (1, 2): '))

            result, visited_states, end = None, None, None

            print(f'> Rozwiązuje...')

            if heuristic_function == 1:
                result, visited_states, end = solve_puzzle(example_node)

                heuristic_stats['first'][0] += 1
                heuristic_stats['first'][1] += visited_states
            elif heuristic_function == 2:
                result, visited_states, end = solve_puzzle(example_node, 2)

                heuristic_stats['second'][0] += 1
                heuristic_stats['second'][1] += visited_states

            if result:
                path_length = compute_solution_length(end)

                if heuristic_function == 1:
                    heuristic_stats['first'][2] += path_length
                elif heuristic_function == 2:
                    heuristic_stats['second'][2] += path_length

                print(f'> Znalezione rozwiązanie: ')

                print_solution(end)

                print(f'> A* - liczba odwiedzonych stanów: {visited_states}')
                print(f'> A* - długość ścieżki do rozwiązania : {compute_solution_length(end)}')

            else:
                print(f'> Nie udało się znaleźć rozwiązania...')

        elif command == 'e':
            print(f'> Koniec ! Wypisuje statystyki dotyczące poszczególnych heurystyk...')
            print(f'\n')
            print_heuristic_stats(heuristic_stats)
            break
        else:
            print(f'> Nieznany symbol ! Spróbuj ponownie...')


main()
