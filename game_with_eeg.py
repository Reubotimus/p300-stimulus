from cmath import inf
import pygame
import random
import time
import explorepy
import argparse
from MockExplore import MockExplore
from Character import Character

# SETUP GLOBAL CONSTANT
# Time in s between each row / column
STIMULUS_INTERVAL = 1 / 16
# Time that a row is intensified for
INTENSIFICATION_DURATION = STIMULUS_INTERVAL * 0.5
# Number of times each row and column will be cycled through before a break
N_CYCLES_IN_EPOCH = 5
# Determines if the break is automatic or epoch is reinitiated by user pressing space
AUTO_EPOCH = False
# Break time in seconds between epochs
BREAK_TIME = 4
DISPLAYED_CHARS = "123456789".upper()
MATRIX_DIMENSIONS = (3, 3)
FONT_SIZE = 120
INTENSE = False
# SCREEN_SIZE = (1280, 750)
SCREEN_SIZE = (1600, 900)
FPS = 60


# WARNING !!!!!!!!!
# WARNING: We used the int() type caster in the explore.setMarker. This can cause issues in the future if we use letters.
# Letter -> Mapping can be used in the future.
# WARNING !!!!!!!!!


def parse_arguments():
    parser = argparse.ArgumentParser(description="Example code for marker generation")
    parser.add_argument("-n", "--name", dest="name", type=str, help="Name of the device.")
    parser.add_argument(
        "-f",
        "--filename",
        dest="filename",
        default="eeg_output",
        type=str,
        help="Name of the output files.",
    )
    parser.add_argument(
        "-m",
        "--mock",
        dest="mock",
        default=False,
        type=bool,
        help="Use a mock Mentalab Explore device.",
    )
    args = parser.parse_args()
    return args


def create_explore_object(args):
    args = parse_arguments()
    # Create an Explore object
    if args.mock:
        explore = MockExplore(log=True)
    else:
        explore = explorepy.Explore()
    explore.connect(device_name=args.name)
    explore.record_data(file_name=args.filename, file_type="csv", do_overwrite=True, block=False)
    return explore


def init_char_array(starting_x_pos, char_surface_size, explore):
    font = pygame.font.Font("HelveticaBold.ttf", FONT_SIZE)
    # Initialises all the characters to be shown on screen, saves each character in their group
    # each group is either a row or column
    chars = []
    # groups = [[] for i in range(MATRIX_DIMENSIONS[0] + MATRIX_DIMENSIONS[1])]
    i = 1
    row = 0
    col = 0
    pos = [starting_x_pos, 0]
    # pos2 = (starting_x_pos, 0)
    for char in DISPLAYED_CHARS:
        chars.append(Character(char, tuple(pos), char_surface_size, font, INTENSE, explore))
        # groups[row].append(i - 1)
        # groups[col + MATRIX_DIMENSIONS[0]].append(i - 1)
        if i % MATRIX_DIMENSIONS[0] == 0 and i != 0:
            pos[0] = starting_x_pos
            pos[1] += char_surface_size
            col = 0
            row += 1
        else:
            pos[0] += char_surface_size
            col += 1
        i += 1
    random.shuffle(chars)
    return chars


def check_user_event(explore, epoch_on, n_cycles):
    for event in pygame.event.get():
        # exits program if user presses exit
        if event.type == pygame.QUIT:
            explore.stop_recording()
            pygame.quit()
            exit()
        # restarts epoch if user presses space
        if not AUTO_EPOCH and not epoch_on and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            epoch_on = True
            n_cycles = 0
    return epoch_on, n_cycles


def main():
    args = parse_arguments()
    explore = create_explore_object(args)

    # finds derived values
    char_surface_size = min((SCREEN_SIZE[0] / MATRIX_DIMENSIONS[0], SCREEN_SIZE[1] / MATRIX_DIMENSIONS[1]))
    starting_x_pos = (SCREEN_SIZE[0] - char_surface_size * MATRIX_DIMENSIONS[0]) / 2

    # Initialises the pygame screen
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    chars = init_char_array(starting_x_pos, char_surface_size, explore)

    # starts game loop
    group_num = 0
    time_since_intensification = time.time()
    row_intensified = False
    epoch_on = True
    n_cycles = 0
    time_end_epoch = inf
    while True:
        # defines the time of the frame so that function does not need to be called often
        time_of_frame = time.time()

        # checks user events to exit program or restart epoch
        epoch_on, n_cycles = check_user_event(explore, epoch_on, n_cycles)

        # restarts epoch if on automatic and enough time has passed
        if AUTO_EPOCH and not epoch_on and time_of_frame - time_end_epoch > BREAK_TIME:
            epoch_on = True
            n_cycles = 0

        if epoch_on:
            # intensifies new group of chars and puts them on the screen
            if time_of_frame - time_since_intensification > STIMULUS_INTERVAL:
                # shuffles groups and starts again if all groups have been intensified
                if group_num == MATRIX_DIMENSIONS[0] * MATRIX_DIMENSIONS[1]:
                    # ensures that the intensified row / col is not flashed consecutively
                    shuffled = False
                    last_char = chars[group_num - 1]
                    while not shuffled:
                        random.shuffle(chars)
                        if last_char != chars[0]:
                            shuffled = True
                    group_num = 0
                    n_cycles += 1
                else:
                    # intensifies new char
                    chars[group_num].intensify()
                    group_num += 1

                # refreshes and puts all characters on screen
                screen.fill("black")
                for char in chars:
                    screen.blit(char.surface, char.screen_position)
                row_intensified = True
                time_since_intensification = time.time()
                # ends epoch if completed n_cycles in epoch
                if n_cycles >= N_CYCLES_IN_EPOCH:
                    epoch_on = False
                    time_end_epoch = time.time()

        # darkens rows / cols after they have been on longer then intensification durantion
        if row_intensified and time_of_frame - time_since_intensification > INTENSIFICATION_DURATION:
            # darkens char
            chars[group_num - 1].darken()
            # refreshes and puts all characters on screen
            screen.fill("black")
            for char in chars:
                screen.blit(char.surface, char.screen_position)
            row_intensified = False

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
