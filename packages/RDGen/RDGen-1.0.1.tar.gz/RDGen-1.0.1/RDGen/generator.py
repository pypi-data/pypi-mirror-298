# generator.py
import random
import math

def generate_rooms(num_rooms, min_width, max_width, min_height, max_height, grid_width, grid_height, buffer=1):
    """
    Generates non-overlapping rooms in a dungeon grid.

    Returns:
        grid (list of lists): The dungeon grid.
        rooms (list of dicts): Details of the rooms generated.
    """
    grid = [['W' for _ in range(grid_width)] for _ in range(grid_height)]
    rooms = []
    max_attempts = num_rooms * 5
    attempts = 0

    while len(rooms) < num_rooms and attempts < max_attempts:
        width = random.randint(min_width, max_width)
        height = random.randint(min_height, max_height)
        x = random.randint(buffer, grid_width - width - buffer)
        y = random.randint(buffer, grid_height - height - buffer)

        x0 = max(0, x - 1)
        y0 = max(0, y - 1)
        x1 = min(grid_width, x + width + 1)
        y1 = min(grid_height, y + height + 1)

        overlap = False
        for i in range(y0, y1):
            for j in range(x0, x1):
                if grid[i][j] != 'W':
                    overlap = True
                    break
            if overlap:
                break

        if not overlap:
            for i in range(y, y + height):
                for j in range(x, x + width):
                    grid[i][j] = '.'

            room = {
                'x': x,
                'y': y,
                'width': width,
                'height': height
            }
            rooms.append(room)

        attempts += 1

    if len(rooms) < num_rooms:
        print(f"Could only place {len(rooms)} out of {num_rooms} rooms due to space constraints.")

    return grid, rooms

def connect_rooms(grid, rooms, door_chance):

    # Precompute edge points for all rooms
    room_edges = [get_room_edge_points(room) for room in rooms]

    # Build the list of edges with distances between rooms
    edges = []
    for i in range(len(rooms)):
        for j in range(i + 1, len(rooms)):
            min_distance = None
            closest_points = None

            # Find the closest pair of edge points between room i and room j
            for point_a in room_edges[i]:
                for point_b in room_edges[j]:
                    distance = math.hypot(point_b[0] - point_a[0], point_b[1] - point_a[1])
                    if min_distance is None or distance < min_distance:
                        min_distance = distance
                        closest_points = (point_a, point_b)

            edges.append({
                'from': i,
                'to': j,
                'distance': min_distance,
                'points': closest_points
            })

    # Sort edges by distance (ascending)
    edges.sort(key=lambda e: e['distance'])

    # Initialize parent list for union-find
    parent = [i for i in range(len(rooms))]

    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]  # Path compression
            u = parent[u]
        return u

    def union(u, v):
        parent[find(u)] = find(v)

    # List to keep track of which edges are used in the MST
    mst_edges = []

    # Kruskal's algorithm to build the MST
    for edge in edges:
        u = edge['from']
        v = edge['to']
        if find(u) != find(v):
            # Connect the rooms using the closest edge points
            point_a, point_b = edge['points']
            create_tunnel(grid, point_a, point_b, door_chance)
            union(u, v)
            mst_edges.append(edge)  # Keep track of used edges

    # Optionally add extra corridors to create loops (omitted for brevity)

def create_tunnel(grid, start, end, door_chance):
    x1, y1 = start
    x2, y2 = end

    if random.choice([True, False]):
        path1, last_pos1 = create_h_corridor(grid, x1, x2, y1)
        path2, last_pos2 = create_v_corridor(grid, y1, y2, x2)
    else:
        path1, last_pos1 = create_v_corridor(grid, y1, y2, x1)
        path2, last_pos2 = create_h_corridor(grid, x1, x2, y2)

    # Place doors at the last positions adjacent to rooms
    if last_pos1:
        place_door(grid, last_pos1[0], last_pos1[1], door_chance)
    if last_pos2:
        place_door(grid, last_pos2[0], last_pos2[1], door_chance)

def create_h_corridor(grid, x1, x2, y):
    path = []
    step = 1 if x2 >= x1 else -1
    x = x1

    while x != x2 + step:
        if grid[y][x] == '.' and x != x1:
            break  # Stop if we reach a room ('.'), but not at the starting position
        else:
            if grid[y][x] == 'W':
                grid[y][x] = '#'  # Carve out corridor
            path.append((x, y))
        x += step

    last_x = x - step
    return path, (last_x, y)

def create_v_corridor(grid, y1, y2, x):
    path = []
    step = 1 if y2 >= y1 else -1
    y = y1

    while y != y2 + step:
        if grid[y][x] == '.' and y != y1:
            break  # Stop if we reach a room ('.'), but not at the starting position
        else:
            if grid[y][x] == 'W':
                grid[y][x] = '#'  # Carve out corridor
            path.append((x, y))
        y += step

    last_y = y - step
    return path, (x, last_y)

def place_door(grid, x, y, door_chance):
    if grid[y][x] == '#':  # Only place doors on corridors
        # Check adjacent tiles for a room
        adjacent_positions = [
            (x - 1, y),  # Left
            (x + 1, y),  # Right
            (x, y - 1),  # Up
            (x, y + 1)   # Down
        ]

        for adj_x, adj_y in adjacent_positions:
            if 0 <= adj_x < len(grid[0]) and 0 <= adj_y < len(grid):
                if grid[adj_y][adj_x] == '.':  # Adjacent to a room
                    if random.random() < door_chance:
                        grid[y][x] = '+'
                    break  # Only need to check one adjacent room

def get_room_edge_points(room):
    """
    Returns a list of edge points (x, y) for the given room.

    Parameters:
        room (dict): The room data with 'x', 'y', 'width', 'height'.

    Returns:
        edge_points (list): List of (x, y) tuples representing the room's edge tiles.
    """
    edge_points = []

    x_start = room['x']
    y_start = room['y']
    x_end = room['x'] + room['width'] - 1
    y_end = room['y'] + room['height'] - 1

    # Top and bottom edges
    for x in range(x_start, x_end + 1):
        edge_points.append((x, y_start))    # Top edge
        edge_points.append((x, y_end))      # Bottom edge

    # Left and right edges
    for y in range(y_start + 1, y_end):
        edge_points.append((x_start, y))   # Left edge
        edge_points.append((x_end, y))     # Right edge

    return edge_points
