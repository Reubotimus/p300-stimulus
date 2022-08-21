import pygame
import random
import time
import explorepy
import argparse

# adjustable variables
stimulus_interval = 0.175 # time in s between each row / column
intensification_duration = 0.1 # time that a row is intensified for
n_cycles_in_epoch = 10 # number of times each row and column will be cycled through before a break
auto_epoch = True # determines if the break is automatic or epoch is reinitiated by user pressing space
break_time = 2 # break time between epochs
displayed_chars = "123456789".upper()
matrix_dimensions = (3,3)
font_size = 90
grey = (50,50,50)
intense = False
screen_size = (1280, 750)

# We create the parser and explorer to record the data from the new EEG device 


# WARNING !!!!!!!!!
# WARNING: We used the int() type caster in the explore.setMarker. This can Cause an issue in the future if you use letters. Letter -> Mapping can be used in the future
# WARNING !!!!!!!!!

parser = argparse.ArgumentParser(description="Example code for marker generation")
parser.add_argument("-n", "--name", dest="name", type=str, help="Name of the device.")
args = parser.parse_args()

# Create an Explore object
explore = explorepy.Explore()
explore.connect(device_name=args.name)
explore.record_data(file_name='test_event_gen', file_type='csv', do_overwrite=True, block=False)


# finds derived values
char_surface_size = min((screen_size[0]/matrix_dimensions[0], screen_size[1]/matrix_dimensions[1]))
starting_x_pos = (screen_size[0]-char_surface_size*matrix_dimensions[0])/2

# Initialises the pygame screen
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
font = pygame.font.Font('HelveticaBold.ttf', font_size)


# creates class for characters being displayed on speller
class Character:

    def __init__(self, character, position):
        self.charater = character
        self.character_image = font.render(character, True, grey)
        self.image_location = ((char_surface_size-self.character_image.get_width())/2, (char_surface_size-self.character_image.get_height())/2)
        self.screen_position = position
        self.surface = pygame.Surface((char_surface_size,char_surface_size))
        self.surface.blit(self.character_image, self.image_location)
    
    def intensify(self):
        if intense == True:
            self.surface.fill('white')
            self.character_image = font.render(self.charater, True, 'black')
            self.surface.blit(self.character_image, self.image_location)
            explore.set_marker(code=int(self.charater))
        else:
            self.surface.fill('black')
            self.character_image = font.render(self.charater, True, 'white')
            self.surface.blit(self.character_image, self.image_location)
            explore.set_marker(code= int(self.charater) )
    
    def darken(self):
        self.surface.fill('black')
        self.character_image = font.render(self.charater, True, grey)
        self.surface.blit(self.character_image, self.image_location)


# Initialises all the characters to be shown on screen, saves each character in their group
# each group is either a row or column
chars = []
groups = [[] for i in range(matrix_dimensions[0]+matrix_dimensions[1])]
i = 1
row = 0
col = 0
pos = [starting_x_pos, 0]
for char in displayed_chars:
    chars.append(Character(char, tuple(pos)))
    groups[row].append(i-1)
    groups[col+matrix_dimensions[0]].append(i-1)
    if i % matrix_dimensions[0] == 0 and i != 0:
        pos[0] = starting_x_pos
        pos[1] += char_surface_size
        col = 0
        row += 1
    else:
        pos[0] += char_surface_size
        col += 1
    i += 1
random.shuffle(chars)

# starts game loop
group_num = 0
time_since_intensification = time.time()
row_intensified = False
epoch_on = True
n_cycles = 0
while True:
    # defines the time of the frame so that function does not need to be called often
    time_of_frame = time.time()
    
    # checks user events
    for event in pygame.event.get():
        # exits program if user presses exit
        if event.type == pygame.QUIT:
            explore.stop_recording()
            pygame.quit()
            exit()
        # restarts epoch if user presses space
        if not auto_epoch and not epoch_on and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            epoch_on = True
            n_cycles = 0
    
    # restarts epoch if on automatic and enough time has passed
    if auto_epoch and not epoch_on and time_of_frame - time_end_epoch > break_time:
        epoch_on = True
        n_cycles = 0

    
    if epoch_on:
        # intensifies new group of chars and puts them on the screen
        if time_of_frame - time_since_intensification > stimulus_interval:
            # shuffles groups and starts again if all groups have been intensified
            if group_num == matrix_dimensions[0]*matrix_dimensions[1]:
                # ensures that the intensified row / col is not flashed consecutively
                shuffled = False
                last_char = chars[group_num - 1]
                while not shuffled:
                    random.shuffle(chars)
                    if last_char != chars[0]:
                        shuffled = True
                group_num = 0
                n_cycles += 1
            # intensifies new char
            chars[group_num].intensify()

            # refreshes and puts all characters on screen
            screen.fill('black')
            for char in chars:
                screen.blit(char.surface, char.screen_position)
            group_num += 1
            row_intensified = True
            time_since_intensification = time.time()
            # ends epoch if completed n_cycles in epoch
            if n_cycles > n_cycles_in_epoch:
                epoch_on = False
                time_end_epoch = time.time()
            
        
    # darkens rows / cols after they have been on longer then intensification durantion
    if row_intensified and time_of_frame - time_since_intensification > intensification_duration:
        # darkens char
        chars[group_num - 1].darken()
        # refreshes and puts all characters on screen
        screen.fill('black')
        for char in chars:
            screen.blit(char.surface, char.screen_position)
        row_intensified = False
        
        

    pygame.display.update()
    clock.tick(60)

