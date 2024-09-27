# main.py

from RDGen import generate_rooms, connect_rooms

from colorama import init, Fore, Style


def main():
    # Define your parameters
    num_rooms = 10
    min_width = 5
    max_width = 10
    min_height = 5
    max_height = 10
    grid_width = 50
    grid_height = 50
    door_chance = 0.5

    # Generate the dungeon
    grid, rooms = generate_rooms(
        num_rooms, min_width, max_width, min_height, max_height, grid_width, grid_height
    )

    # Connect the rooms
    connect_rooms(grid, rooms, door_chance)

    # Visualization code...
    # Initialize colorama
    init()

    # Print the grid with colors
    for row in grid:
        line = ''
        for cell in row:
            if cell == '.':
                line += Fore.WHITE + '.' + Style.RESET_ALL  # Rooms (floor)
            elif cell == '#':
                line += Fore.WHITE + '.' + Style.RESET_ALL  # Corridors
            elif cell == '+':
                line += Fore.YELLOW + '+' + Style.RESET_ALL  # Doors
            elif cell == 'W':
                line += Fore.GREEN + '#' + Style.RESET_ALL  # Walls
            else:
                line += ' '  # Should not occur
        print(line)

if __name__ == '__main__':
    main()