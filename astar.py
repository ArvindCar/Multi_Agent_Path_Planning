import pygame
import sys
from queue import PriorityQueue
import random

# Define constants
WIDTH = 800
ROWS = 20
COLS = 20
OBSTACLES = [(5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (9, 7), (7, 5), (8, 5), (8, 6)]
GRID_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

DARK_RED = (150, 0, 0)
DARK_GREEN = (0, 150, 0) 
DARK_BLUE = (0, 0, 150)
DARK_CYAN = (0, 150, 150)
DARK_YELLOW = (150,150, 0)
DARK_MAGENTA = (150, 0, 150)

colors = ["GREEN", "BLUE", "RED", "CYAN", "YELLOW", "MAGENTA"]
colordict = {}
colordict["GREEN"] = GREEN
colordict["DARK_GREEN"] = DARK_GREEN
colordict["BLUE"] = BLUE
colordict["DARK_BLUE"] = DARK_BLUE
colordict["RED"] = RED
colordict["DARK_RED"] = DARK_RED
colordict["CYAN"] = CYAN
colordict["DARK_CYAN"] = DARK_CYAN
colordict["YELLOW"] = YELLOW
colordict["DARK_YELLOW"] = DARK_YELLOW
colordict["MAGENTA"] = MAGENTA
colordict["DARK_MAGENTA"] = DARK_MAGENTA

# Define the number of agents
NUM_AGENTS = 6

START_NODES = []
while len(START_NODES) < NUM_AGENTS:
    new_start_node = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
    if new_start_node not in START_NODES and new_start_node not in OBSTACLES:
        START_NODES.append(new_start_node)

END_NODES = []
while len(END_NODES) < NUM_AGENTS:
    new_end_node = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
    if new_end_node not in END_NODES and new_end_node not in START_NODES and new_end_node not in OBSTACLES:
        END_NODES.append(new_end_node)

# Define the grid graph class
class GridGraph:
    def __init__(self, rows, cols, obstacles):
        self.rows = rows
        self.cols = cols
        self.obstacles = set(obstacles)
        self.agent_positions = set()

    def neighbors(self, node):
        row, col = node
        neighbors = []
        if row > 0 and (row - 1, col) not in self.obstacles and (row - 1, col) not in self.agent_positions:
            neighbors.append((row - 1, col))
        if row < self.rows - 1 and (row + 1, col) not in self.obstacles and (row + 1, col) not in self.agent_positions:
            neighbors.append((row + 1, col))
        if col > 0 and (row, col - 1) not in self.obstacles and (row, col - 1) not in self.agent_positions:
            neighbors.append((row, col - 1))
        if col < self.cols - 1 and (row, col + 1) not in self.obstacles and (row, col + 1) not in self.agent_positions:
            neighbors.append((row, col + 1))
        return neighbors

    def cost(self, current, next_node):
        return 1  # Uniform cost for simplicity

# Define the A* algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next_node in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next_node)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                frontier.put(next_node, priority)
                came_from[next_node] = current

    return reconstruct_path(came_from, start, goal)

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    return path[::-1]

# Visualization functions
def draw_grid(screen, graph):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row, col) in graph.obstacles else BLACK
            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
            pygame.draw.rect(screen, WHITE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

# Modify draw_path function
def draw_path(screen, agents):
    for agent in agents:
        pygame.draw.rect(screen, colordict[agent.color], (agent.now[1] * GRID_SIZE, agent.now[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def draw_nodes(START_NODES, END_NODES):
    font = pygame.font.Font(None, 10)
    for (row, col) in START_NODES:
        text = font.render("START", True, (255, 255, 255))
        text_rect = text.get_rect(center=(col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))
        screen.blit(text, text_rect)

    for (row, col) in END_NODES:
        text = font.render("END", True, (255, 255, 255))
        text_rect = text.get_rect(center=(col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))
        screen.blit(text, text_rect)

def draw_start_end(screen, START_NODES, END_NODES, dark_colors):
    for start,end, dark_color in zip(START_NODES, END_NODES, dark_colors):
        pygame.draw.rect(screen, colordict[dark_color], (start[1] * GRID_SIZE, start[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, colordict[dark_color], (end[1] * GRID_SIZE, end[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    font = pygame.font.Font(None, 20)
    for (row, col) in START_NODES:
        text = font.render("START", True, (255, 255, 255))
        text_rect = text.get_rect(center=(col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))
        screen.blit(text, text_rect)

    for (row, col) in END_NODES:
        text = font.render("END", True, (255, 255, 255))
        text_rect = text.get_rect(center=(col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))
        screen.blit(text, text_rect)

class Agent:
    def __init__(self, graph, start, end, color, dark_color):
        self.graph = graph
        self.start = start
        self.end = end
        self.color = color
        self.dark_color = dark_color
        self.now = start
        self.next = start

    def find_path(self):
        return a_star(self.graph, self.start, self.end)
    
    def remove_obstacles(self):
        if self.now in self.graph.agent_positions:
            self.graph.agent_positions.remove(self.now)

    def add_obstacles(self):
        self.graph.agent_positions.add(self.now)


# Initialize Pygame
pygame.init()

# Create a Pygame screen
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Visualization")
clock = pygame.time.Clock()

# Create the grid graph
graph = GridGraph(ROWS, COLS, OBSTACLES)

# Create agents
agents = []
for i in range(NUM_AGENTS):
    agent_color = colors[i]
    agent_dark_color = "DARK_" + agent_color
    agent = Agent(graph, START_NODES[i], END_NODES[i], agent_color, agent_dark_color)
    agents.append(agent)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    draw_grid(screen, graph)
    draw_start_end(screen, START_NODES, END_NODES, ["DARK_"+color for color in colors])
    pygame.display.flip()
    clock.tick(0.5)

    max_path_length = max(len(agent.find_path()) for agent in agents)
    for step in range(max_path_length):
        for agent in agents:
            paths = agent.find_path()
            if step < len(paths):
                agent.next = paths[step]
                agent.add_obstacles()
        # Move agents to their next positions only if those positions are not occupied by other agents
        for agent in agents:
            agent.remove_obstacles()
            agent.now = agent.next
        # Draw the current positions of agents and obstacles
        draw_path(screen, agents)
        draw_start_end(screen, START_NODES, END_NODES, ["DARK_"+color for color in colors])
        pygame.display.flip()
        clock.tick(2)  # Adjust the speed of visualization

    clock.tick(0.4)

    # Quit Pygame
    pygame.quit()
    sys.exit()








# # Run Pygame event loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill(BLACK)
#     draw_grid(screen)
#     draw_start_end(screen, START_NODES, end_node, dark_colors=["DARK_" + color for color in colors])
#     pygame.display.flip()
#     clock.tick(0.5)
#     for i in range(3):
#     # Find paths using A*
#         paths = a_star(graph, START_NODES[i], end_node[i])
#         color = colors[i]
#         draw_path(screen, paths, color)
#         pygame.display.flip()
#         clock.tick(1)  # Adjust the speed of visualization

#     clock.tick(0.1)
#     # Quit Pygame
#     pygame.quit()
#     sys.exit()

