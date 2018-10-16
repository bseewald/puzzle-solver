import argparse
import timeit
import resource
from collections import deque
from NodeState import NodeState


# BSF implementation
def puzzle_solver(start_state):

    puzzle_size = len(start_state)
    puzzle_side_size = int(puzzle_size ** 0.5)

    nodes_expanded = 0
    max_search_depth = 0

    # Success!
    goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Vertex S
    nodes = NodeState(start_state, None, None, 0, 0)

    # ENQUEUE(Q, s)
    queue = deque([nodes])
    explored_nodes = set()

    while queue:
        # DEQUEUE(Q)
        node = queue.popleft()
        explored_nodes.add(node.map)

        # is final state ?    
        if node.state == goal_state:
            return node.cost

        neighbors, nodes_expanded = expand_neighbors(node, nodes_expanded, puzzle_size, puzzle_side_size)

        for neighbor in neighbors:
            if neighbor.map not in explored_nodes:
                queue.append(neighbor)
                if neighbor.depth > max_search_depth:
                    max_search_depth += 1


def expand_neighbors(node, nodes_expanded, puzzle_size, puzzle_side_size):

    neighbors = list()
    # Only four movements possible: up, down, left, right
    for i in range(1, 5):
        neighbors.append(NodeState(move(node.state, i, puzzle_size, puzzle_side_size),
                                   node,
                                   i,
                                   node.depth + 1,
                                   node.cost + 1))

    nodes = [neighbor for neighbor in neighbors if neighbor.state]
    nodes_expanded += 1
    return nodes, nodes_expanded


def move(state, position, puzzle_size, puzzle_side_size):

    new_state = state[:]

    # Index for blank space
    index = new_state.index(0)

    if position == 1:  # Up
        if index not in range(0, puzzle_side_size):
            temp = new_state[index - puzzle_side_size]
            new_state[index - puzzle_side_size] = new_state[index]
            new_state[index] = temp
            return new_state
        else:
            return None

    if position == 2:  # Down
        if index not in range(puzzle_size - puzzle_side_size, puzzle_size):
            temp = new_state[index + puzzle_side_size]
            new_state[index + puzzle_side_size] = new_state[index]
            new_state[index] = temp
            return new_state
        else:
            return None

    if position == 3:  # Left
        if index not in range(0, puzzle_size, puzzle_side_size):
            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp
            return new_state
        else:
            return None

    if position == 4:  # Right
        if index not in range(puzzle_side_size - 1, puzzle_size, puzzle_side_size):
            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp
            return new_state
        else:
            return None


def is_puzzle_solvable(start_state):

    inversions = 0
    for i in range(0, len(start_state) - 1):
        for j in range(i+1, len(start_state)):
            # Check if a larger number exists after the current place in the array
            if start_state[i] != 0 and start_state[j] != 0 and start_state[i] > start_state[j]:
                inversions += 1
    return inversions % 2 == 0


def read_initial_state_from_file(initial_state_file):

    start_state = []

    st_file = open(initial_state_file, "r")
    initial_state = st_file.readline()

    st = initial_state.split(",")

    for number in st:
        start_state.append(int(number))

    return start_state


def export_information(time):

    # TODO: time em segundos ?
    results_file = open('./testes/performance.txt', 'w')

    results_file.write("\nrunning_time: " + format(time, '.8f'))
    results_file.write("\nmax_ram_usage_in_MB: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.8f'))
    results_file.close()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('initial_state_file', help="File with input state. Example: 1,2,5,3,4,0,6,7,8")
    parser.add_argument('final_cost_file', help="File with final cost. Example: 'custo_total: 3'")
    args = parser.parse_args()

    # read initial state from input
    start_state = read_initial_state_from_file(args.initial_state_file)

    # start time
    start = timeit.default_timer()

    # If inversions is even, the puzzle is solvable
    inversions = is_puzzle_solvable(start_state)
    if not inversions:
        print "Puzzle is not solvable"
        return

    final_cost_result = puzzle_solver(start_state)

    # stop time
    stop = timeit.default_timer()

    # more information about the solution
    export_information(stop-start)

    # write file with final cost
    ft_file = open(args.final_cost_file, "w")
    ft_file.write("custo_total: " + str(final_cost_result))
    ft_file.close()


if __name__ == '__main__':
    main()
