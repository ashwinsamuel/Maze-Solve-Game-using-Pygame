#!/usr/bin/env python
# coding: utf-8
import pygame as pygame
import math
from copy import deepcopy
import time

GREY = (128, 128, 128)
Block_Black = (0, 0, 0)
YELLOW = (255, 255, 0)
Orange = (185, 32, 56)
White = (255, 255, 255)
start_red = (255, 0, 0)
stop_green = (0, 255, 0)
size = 50
dimension = 750
blocksize = dimension // size;


def visual(dismaze, final_path, a):
    maze_visuzal(dismaze, final_path, a)




def maze_visuzal(dismaze, final_path, a):

    block = []
    mazen = pygame.display.set_mode((dimension, dimension))

    mazen.fill(White)
    block=[]
    block = make_maz(dismaze,final_path,block)
    started = True
    z=10
    while started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                started = False
        for s in final_path[0:len(final_path)-1]:
            started=False
            draw_main(block,mazen)
            time.sleep(.1)
            block[s[0]][s[1]].set_colour(GREY)
            pygame.display.update()
            pygame.display.flip()


def make_maz(dismaze,final_path,block):
    for i in range(size):
        block.append([])
        for j in range(size):
            r = dismaze[i][j]
            if r =='_':
                block[i].append(elements(i, j, White))

            if  r =='X':
                block[i].append(elements(i, j, Block_Black))

            if r == 'A':
                 block[i].append(elements(i, j, YELLOW))
            if r == 'S':
                block[i].append(elements(i, j, start_red))

            if r == 'T':
                block[i].append(elements(i, j, stop_green))

    return block


def draw_line(mazen):
    for i in range(size + 1):
        pygame.draw.line(mazen, GREY, (0, i * blocksize), (dimension, i * blocksize))
        for j in range(size + 1):
            pygame.draw.line(mazen, GREY, (j * blocksize, 0), (j * blocksize, dimension))


def draw_main(block,mazen):
    for k in block:
        for j in k:
            j.draw_block(mazen)

    draw_line(mazen)
    pygame.display.update()


class elements:
    def __init__(self, row, column, colour):
        self.colour = colour
        self.x = column
        self.y = row
        self.neighbour = []

    def get_pos(self):
        return self.row, self.column

    def is_blocked(self):
        return self.colour == Block_Black

    def set_block(self):
        self.colour = Block_Black

    def set_colour(self, colour):
        self.colour = colour

    def draw_block(self,mazen):
        pygame.draw.rect(mazen, self.colour, pygame.Rect(self.x * blocksize, self.y * blocksize, blocksize,  blocksize))


import random
import heapq

maze = []
agent_maze = []
maze_start = None
maze_target = None
maze = []
agent_maze = []


def make_maze():
    for i in range(size):
        maze.append([])
        agent_maze.append([])
        for j in range(size):
            # agent maze
            agent_maze[i].append("_")

            # actual maze
            r = random.randint(1, 10)
            if r <= 7:
                maze[i].append("_")
            else:
                maze[i].append("X")
    return maze, agent_maze


def IsCellBlocked(maze, cell):
    if maze[cell[0]][cell[1]] == "X":
        return True
    else:
        return False


def get_agent_maze_neighbours(cell):
    neighbours = []

    # Cell Below
    neighbour = (cell[0] + 1, cell[1])
    if cell[0] < size - 1 and not IsCellBlocked(agent_maze, neighbour):
        neighbours.append(neighbour)

    # Cell Above
    neighbour = (cell[0] - 1, cell[1])
    if cell[0] > 0 and not IsCellBlocked(agent_maze, neighbour):
        neighbours.append(neighbour)

    # Cell Left
    neighbour = (cell[0], cell[1] - 1)
    if cell[1] > 0 and not IsCellBlocked(agent_maze, neighbour):
        neighbours.append(neighbour)

    # Cell Right
    neighbour = (cell[0], cell[1] + 1)
    if cell[1] < size - 1 and not IsCellBlocked(agent_maze, neighbour):
        neighbours.append(neighbour)

    return neighbours


def clear_agent_maze():
    start = tuple()
    for i in range(size):
        for j in range(size):
            if maze[i][j] == "S":
                agent_maze[i][j] = "S"
                start = (i, j)
            elif maze[i][j] == "T":
                agent_maze[i][j] = "T"
            else:
                agent_maze[i][j] = "_"

    # Block neighbours of start cell if blocked in original grid
    if start[0] > 0:
        agent_maze[start[0] - 1][start[1]] = maze[start[0] - 1][start[1]]
    if start[0] < size - 1:
        agent_maze[start[0] + 1][start[1]] = maze[start[0] + 1][start[1]]
    if start[1] > 0:
        agent_maze[start[0]][start[1] - 1] = maze[start[0]][start[1] - 1]
    if start[1] < size - 1:
        agent_maze[start[0]][start[1] + 1] = maze[start[0]][start[1] + 1]

    return agent_maze


def mark_blocked_cells(cell):
    if cell[0] > 0:
        agent_maze[cell[0] - 1][cell[1]] = maze[cell[0] - 1][cell[1]]
    if cell[0] < size - 1:
        agent_maze[cell[0] + 1][cell[1]] = maze[cell[0] + 1][cell[1]]
    if cell[1] > 0:
        agent_maze[cell[0]][cell[1] - 1] = maze[cell[0]][cell[1] - 1]
    if cell[1] < size - 1:
        agent_maze[cell[0]][cell[1] + 1] = maze[cell[0]][cell[1] + 1]

    return agent_maze


def main():
    cnt = 0
    backward = True

    for T in range(1):
        maze, agent_maze = make_maze()
        maze_start, maze_target = createstartstop()

        print("Original Maze: ")
        for i in maze:
            print(i)
        print("\nAgent Maze: ")
        for i in agent_maze:
            print(i)

        '''
        if astar(maze_start, maze_target, True):
            cnt += 1
            print("Test case ",T+1,": FOUND PATH WITH (smaller g)A*\n")
        else:
            print("Test case ",T+1,": Could not reach target!\n")
        '''

        agent_maze = clear_agent_maze()
        if astar(maze_start, maze_target, False):
            cnt += 1
            print("Test case ", T + 1, ": FOUND PATH WITH (greater g)A*\n")
        else:
            print("Test case ", T + 1, ": Could not reach target!\n")

        agent_maze = clear_agent_maze()
        if backward_astar(maze_start, maze_target):
            cnt += 1
            print("Test case ", T + 1, ": FOUND PATH WITH BACKWARD A*!")
        else:
            print("Test case ", T + 1, ": Could not reach target!")

        agent_maze = clear_agent_maze()
        if adaptive_astar(maze_start, maze_target):
            cnt += 1
            print("Test case ", T + 1, ": FOUND PATH WITH Adaptive A*\n")
        else:
            print("Test case ", T + 1, ": Could not reach target!\n")

    # print(cnt," / 100 PASSED",)


def manhattan_hueristic(src_node, dest_node):
    return abs(src_node[0] - dest_node[0]) + abs(src_node[1] - dest_node[1])


def heapify(heap_list, i):
    l = 2 * i + 1
    r = 2 * i + 2
    n = len(heap_list)

    if i > (n - 2) // 2:
        return

    if r == n or (heap_list[l] < heap_list[r]):
        smaller_child = l
    else:
        smaller_child = r

    if heap_list[i] > heap_list[smaller_child]:
        heap_list[i], heap_list[smaller_child] = heap_list[smaller_child], heap_list[i]
        heapify(heap_list, smaller_child)


def heap_pop(heap_list):
    n = len(heap_list)
    heap_list[0], heap_list[n - 1] = heap_list[n - 1], heap_list[0]
    best_ele = heap_list.pop()
    heapify(heap_list, 0)

    return best_ele


def heap_send_above(heap_list, i):
    parent = (i - 1) // 2

    while parent >= 0 and heap_list[i] < heap_list[parent]:
        heap_list[i], heap_list[parent] = heap_list[parent], heap_list[i]
        i = parent
        parent = (parent - 1) // 2


def heap_push(heap_list, heap_tuple):
    heap_list.append(heap_tuple)
    heap_send_above(heap_list, len(heap_list) - 1)


def astar(maze_start, maze_target, is_smaller_g):
    # counter for call of ComputePath
    counter = 0
    expanded_cnt = 0
    final_path = []

    search = {(row, col): 0 for row in range(size) for col in range(size)}

    # updating neighbours
    path_tracker = {}

    # creating heap
    open_list_heap = []
    open_list_exists = {}
    closed_list = {}

    # cost dictionaries
    path_cost = {}
    heuristic_cost = {}
    final_cost = {}

    stack = []

    start_node = maze_start

    while start_node != maze_target:
        counter += 1

        # Clear open and closed lists
        open_list_heap.clear()
        open_list_exists.clear()
        closed_list.clear()

        path_cost[start_node] = 0
        search[start_node] = counter
        path_cost[maze_target] = float("inf")
        search[maze_target] = counter

        heuristic_cost[start_node] = manhattan_hueristic(start_node, maze_target)
        final_cost[start_node] = path_cost[start_node] + heuristic_cost[start_node]

        if is_smaller_g:
            open_list_exists[start_node] = (final_cost[start_node], path_cost[start_node], start_node)
            heap_push(open_list_heap, (final_cost[start_node], path_cost[start_node], start_node))
        else:
            open_list_exists[start_node] = (final_cost[start_node], -path_cost[start_node], start_node)
            heap_push(open_list_heap, (final_cost[start_node], -path_cost[start_node], start_node))

        # COMPUTE PATH
        print("---------------------------------------A* Call: ", counter)
        min_node = open_list_heap[0][2]
        while path_cost[maze_target] > final_cost[min_node]:
            # pop the top node
            heap_tuple = heap_pop(open_list_heap)
            current_node = heap_tuple[2]

            closed_list[current_node] = True
            expanded_cnt += 1
            # DEBUG print("\nExpanding ",current_node)
            # DEBUG print("path_cost[current_node] ",path_cost[current_node])

            for cell in get_agent_maze_neighbours(current_node):
                # DEBUG print("Neighbour ",cell)

                if search[cell] < counter:
                    search[cell] = counter
                    path_cost[cell] = float("inf")

                temp_path_cost = path_cost[current_node] + 1
                if temp_path_cost < path_cost[cell]:
                    path_cost[cell] = temp_path_cost
                    heuristic_cost[cell] = manhattan_hueristic(cell, maze_target)
                    final_cost[cell] = path_cost[cell] + heuristic_cost[cell]

                    # add neighbour to Open List
                    if cell in open_list_exists:
                        # DEBUG print(cell," in open list already\n")
                        # if neighbour already exists, then delete and add new if new has better f
                        for i, tup in enumerate(open_list_heap):
                            if tup == open_list_exists[cell]:
                                if is_smaller_g:
                                    tup_new = (final_cost[cell], path_cost[cell])
                                else:
                                    tup_new = (final_cost[cell], -path_cost[cell])

                                if tup_new < (tup[0], tup[1]):
                                    open_list_heap[i] = (tup_new[0], tup_new[1], cell)
                                    heap_send_above(open_list_heap, i)
                                    open_list_exists[cell] = (tup_new[0], tup_new[1], cell)
                                    path_tracker[cell] = current_node

                                break
                    elif cell not in closed_list:
                        # DEBUG print(cell," not in closed list\n")
                        # if doesnt exist then check in closed list if already expanded. If not, add to open list.
                        if is_smaller_g:
                            tup_new = (final_cost[cell], path_cost[cell])
                        else:
                            tup_new = (final_cost[cell], -path_cost[cell])

                        heap_push(open_list_heap, (tup_new[0], tup_new[1], cell))
                        open_list_exists[cell] = (tup_new[0], tup_new[1], cell)
                        path_tracker[cell] = current_node
                        # DEBUG print("[Outside]Open list Heap: " ,open_list_heap,"\n")
            if open_list_heap:
                min_node = open_list_heap[0][2]
            else:
                print("Cannot reach target")
                return False

        stack.clear()
        path_cell = maze_target
        while path_cell != start_node:
            stack.append(path_cell)
            path_cell = path_tracker[path_cell]

        # move till a block is encountered
        print(start_node)
        while start_node != maze_target and stack:
            if not IsCellBlocked(maze, stack[-1]):
                start_node = stack.pop()
                final_path.append(start_node)
                agent_maze = mark_blocked_cells(start_node)
                print(" -> ", start_node)
            else:
                newly_blocked_cell = stack.pop()
                agent_maze[newly_blocked_cell[0]][newly_blocked_cell[1]] = "X"
                stack.clear()

        if start_node == maze_target:
            print("[-------TARGET REACHED--------]")

            print("\nAgent Maze: ")
            for i in agent_maze:
                print(i)
            dismaze = deepcopy(maze)
            for j in final_path:
                if dismaze[j[0]][j[1]] != 'T':
                    dismaze[j[0]][j[1]] = 'A'
            print("\nAgent Maze With Path: ")
            for k in dismaze:
                print(k)
            pygame.display.set_caption("A* Forward Algorithm")
            visual(dismaze, final_path, 0)
            print("\nA* Final Path(len = ", len(final_path), "): ", final_path)
            print("\nA* Counter = ", counter)
            print("\nA* Expanded cells count = ", expanded_cnt)

            return True
        else:
            print("[-------Continuing to next A*--------]")


def backward_astar(maze_start, maze_target):
    # counter for call of ComputePath
    counter = 0
    final_path = []
    expanded_cnt = 0

    search = {(row, col): 0 for row in range(size) for col in range(size)}

    # updating neighbours
    path_tracker = {}

    # creating heap
    open_list_heap = []
    open_list_exists = {}
    closed_list = {}

    # cost dictionaries
    path_cost = {}
    heuristic_cost = {}
    final_cost = {}

    start_node = maze_start

    while start_node != maze_target:
        counter += 1

        # Clear open and closed lists
        open_list_heap.clear()
        open_list_exists.clear()
        closed_list.clear()

        path_cost[maze_target] = 0
        search[maze_target] = counter
        path_cost[start_node] = float("inf")
        search[start_node] = counter

        heuristic_cost[maze_target] = manhattan_hueristic(maze_target, start_node)
        final_cost[maze_target] = path_cost[maze_target] + heuristic_cost[maze_target]

        heap_push(open_list_heap, (final_cost[maze_target], -path_cost[maze_target], maze_target))
        open_list_exists[maze_target] = (final_cost[maze_target], -path_cost[maze_target], maze_target)

        # COMPUTE PATH
        print("---------------------------------------Backward A* Call: ", counter)
        # DEBUGprint("Start node: ",start_node)
        min_node = open_list_heap[0][2]
        while path_cost[start_node] > final_cost[min_node]:
            # pop the top node
            heap_tuple = heap_pop(open_list_heap)
            current_node = heap_tuple[2]

            closed_list[current_node] = True  # could also use counter
            expanded_cnt += 1
            # DEBUGprint("\nExpanding ",current_node)
            # DEBUGprint("path_cost[current_node] ",path_cost[current_node])

            for cell in get_agent_maze_neighbours(current_node):
                # DEBUGprint("Neighbour ",cell)

                if search[cell] < counter:
                    search[cell] = counter
                    path_cost[cell] = float("inf")

                temp_path_cost = path_cost[current_node] + 1
                if temp_path_cost < path_cost[cell]:
                    path_cost[cell] = temp_path_cost
                    heuristic_cost[cell] = manhattan_hueristic(cell, start_node)
                    final_cost[cell] = path_cost[cell] + heuristic_cost[cell]

                    # add neighbour to Open List
                    if cell in open_list_exists:
                        # DEBUGprint(cell," in open list already\n")
                        # if neighbour already exists, then delete and add new if new has better f
                        for i, tup in enumerate(open_list_heap):
                            if tup == open_list_exists[cell]:
                                if (final_cost[cell], path_cost[cell]) < (tup[0], tup[1]):
                                    open_list_heap[i] = (final_cost[cell], -path_cost[cell], cell)
                                    open_list_exists[cell] = (final_cost[cell], -path_cost[cell], cell)
                                    heap_send_above(open_list_heap, i)
                                    path_tracker[cell] = current_node
                                break
                    elif cell not in closed_list:
                        # DEBUGprint(cell," not in closed list\n")
                        # if doesnt exist then check in closed list if already expanded. If not, add to open list.
                        heap_push(open_list_heap, (final_cost[cell], -path_cost[cell], cell))
                        open_list_exists[cell] = (final_cost[cell], -path_cost[cell], cell)

                        # DEBUGprint("New cell f,g,h: ", final_cost[cell], path_cost[cell], heuristic_cost[cell])
                        # DEBUGprint("Open list Heap: " ,open_list_heap,"\n")

                        path_tracker[cell] = current_node
            if open_list_heap:
                min_node = open_list_heap[0][2]
            else:
                print("Cannot reach start")
                return False

        # move till a block is encountered
        print(start_node)
        while start_node != maze_target:
            start_node = path_tracker[start_node]
            agent_maze = mark_blocked_cells(start_node)
            if not IsCellBlocked(maze, start_node):
                final_path.append(start_node)
                print(" -> ", start_node)
            else:
                newly_blocked_cell = start_node
                agent_maze[newly_blocked_cell[0]][newly_blocked_cell[1]] = "X"
                start_node = final_path[-1]
                break

        if start_node == maze_target:
            print("[-------TARGET REACHED--------]")

            print("\nAgent Maze: ")
            for i in agent_maze:
                print(i)
            dismaze1 = deepcopy(maze)
            v = 0
            for j in final_path:
                if dismaze1[j[0]][j[1]] != 'T':
                    dismaze1[j[0]][j[1]] = 'A'
            print("\nAgent Maze With Path: ")
            for k in dismaze1:
                print(k)
            pygame.display.set_caption("A* Backward Algorithm")
            visual(dismaze1, final_path, 1)
            print("\nBackward A* Final Path(len = ", len(final_path), "): ", final_path)
            print("\nBackward A* Counter = ", counter)
            print("\nBackward A* expanded cells count = ", expanded_cnt)

            return True
        else:
            print("[-------Continuing to next Backward A*--------]")


def adaptive_astar(maze_start, maze_target):
    # counter for call of ComputePath
    counter = 0
    final_path = []
    expanded_cnt = 0

    search = {(row, col): 0 for row in range(size) for col in range(size)}

    # updating neighbours
    path_tracker = {}

    # creating heap
    open_list_heap = []
    open_list_exists = {}
    closed_list = {}
    previously_expanded = {}

    # cost dictionaries
    path_cost = {}
    heuristic_cost = {}
    final_cost = {}

    stack = []

    start_node = maze_start

    while start_node != maze_target:
        counter += 1

        # Clear open and closed lists
        open_list_heap.clear()
        open_list_exists.clear()
        closed_list.clear()

        path_cost[start_node] = 0
        search[start_node] = counter
        path_cost[maze_target] = float("inf")
        search[maze_target] = counter

        if start_node not in previously_expanded:
            heuristic_cost[start_node] = manhattan_hueristic(start_node, maze_target)
        final_cost[start_node] = path_cost[start_node] + heuristic_cost[start_node]

        heap_push(open_list_heap, (final_cost[start_node], -path_cost[start_node], start_node))
        open_list_exists[start_node] = (final_cost[start_node], -path_cost[start_node], start_node)

        # COMPUTE PATH
        print("-----------------------------------Adaptive A* Call: ", counter)
        min_node = open_list_heap[0][2]
        while path_cost[maze_target] > final_cost[min_node]:
            # pop the top node
            heap_tuple = heap_pop(open_list_heap)
            current_node = heap_tuple[2]

            closed_list[current_node] = True
            expanded_cnt += 1
            # DEBUGprint("\nExpanding ",current_node)
            # DEBUGprint("path_cost[current_node] ",path_cost[current_node])

            for cell in get_agent_maze_neighbours(current_node):
                # DEBUGprint("Neighbour ",cell)

                if search[cell] < counter:
                    search[cell] = counter
                    path_cost[cell] = float("inf")

                temp_path_cost = path_cost[current_node] + 1
                if temp_path_cost < path_cost[cell]:
                    path_cost[cell] = temp_path_cost
                    if cell not in previously_expanded:
                        heuristic_cost[cell] = manhattan_hueristic(cell, maze_target)
                    final_cost[cell] = path_cost[cell] + heuristic_cost[cell]

                    # add neighbour to Open List
                    if cell in open_list_exists:
                        # DEBUGprint(cell," in open list already\n")
                        # if neighbour already exists, then delete and add new if new has better f
                        for i, tup in enumerate(open_list_heap):
                            if tup == open_list_exists[cell]:
                                if (final_cost[cell], path_cost[cell]) < (tup[0], tup[1]):
                                    open_list_heap[i] = (final_cost[cell], -path_cost[cell], cell)
                                    open_list_exists[cell] = (final_cost[cell], -path_cost[cell], cell)
                                    heap_send_above(open_list_heap, i)
                                    path_tracker[cell] = current_node
                                break
                    elif cell not in closed_list:
                        # DEBUGprint(cell," not in closed list\n")
                        # if doesnt exist then check in closed list if already expanded. If not, add to open list.
                        heap_push(open_list_heap, (final_cost[cell], -path_cost[cell], cell))
                        open_list_exists[cell] = (final_cost[cell], -path_cost[cell], cell)

                        # DEBUGprint("Open list Heap: " ,open_list_heap,"\n")

                        path_tracker[cell] = current_node
            if open_list_heap:
                min_node = open_list_heap[0][2]
            else:
                print("Cannot reach target")
                return False

        # Adaptive A* update for new heuristic for cells in closed list
        for cell in closed_list:
            previously_expanded[cell] = True
            heuristic_cost[cell] = path_cost[maze_target] - path_cost[cell]

        # Path tracking
        stack.clear()
        path_cell = maze_target
        while path_cell != start_node:
            stack.append(path_cell)
            path_cell = path_tracker[path_cell]

        # move till a block is encountered
        print(start_node)
        while start_node != maze_target and stack:
            if not IsCellBlocked(maze, stack[-1]):
                start_node = stack.pop()
                final_path.append(start_node)
                agent_maze = mark_blocked_cells(start_node)
                print(" -> ", start_node)
            else:
                newly_blocked_cell = stack.pop()
                agent_maze[newly_blocked_cell[0]][newly_blocked_cell[1]] = "X"
                stack.clear()

        if start_node == maze_target:
            print("[-------TARGET REACHED--------]")

            print("\nAgent Maze: ")
            for i in agent_maze:
                print(i)
            dismaze3 = deepcopy(maze)

            v = 0
            for j in final_path:
                if dismaze3[j[0]][j[1]] != 'T':
                    dismaze3[j[0]][j[1]] = 'A'
            print("\nAgent Maze With Path: ")
            for k in dismaze3:
                print(k)
            pygame.display.set_caption("A* Adaptive Algorithm")
            visual(dismaze3, final_path, 0)
            print("\nAdaptive A* Final Path(len = ", len(final_path), "): ", final_path)
            print("\nAdaptive A* Counter = ", counter)
            print("\nAdaptive A* expanded cells count = ", expanded_cnt)

            return True
        else:
            print("[-------Continuing to next Adaptive A*--------]")


def createstartstop():
    # Cannot reach target example: return (0,0),(4,4)
    # adaptive a* example: return (4,2),(4,4)
    k = 0
    while True:
        start_row = 0
        start_col = k

        maze_start = (start_row, start_col)
        if IsCellBlocked(maze, maze_start):
            k += 1
            continue
        else:
            maze[start_row][start_col] = "S"
            agent_maze[start_row][start_col] = "S"

            # Block neighbours of start cell if blocked in original grid
            if start_row > 0:
                agent_maze[start_row - 1][start_col] = maze[start_row - 1][start_col]
            if start_row < size - 1:
                agent_maze[start_row + 1][start_col] = maze[start_row + 1][start_col]
            if start_col > 0:
                agent_maze[start_row][start_col - 1] = maze[start_row][start_col - 1]
            if start_col < size - 1:
                agent_maze[start_row][start_col + 1] = maze[start_row][start_col + 1]

            break
    print("Start: ", start_row, ",", start_col)

    k = size - 1
    while True:
        stop_row = size - 1
        stop_col = k

        maze_target = (stop_row, stop_col)
        if IsCellBlocked(maze, maze_target):
            k -= 1
            continue
        else:
            maze[stop_row][stop_col] = "T"
            agent_maze[stop_row][stop_col] = "T"
            break
    print("Stop: ", stop_row, ",", stop_col)

    return maze_start, maze_target


main()