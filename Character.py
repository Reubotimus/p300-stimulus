import pygame


class Character:
    def __init__(self, character, position, char_surface_size, font, flash_type, explore, grey=(50, 50, 50)):
        self.character = character
        self.character_image = font.render(character, True, grey)
        self.image_location = (
            (char_surface_size[0] - self.character_image.get_width()) / 2,
            (char_surface_size[1] - self.character_image.get_height()) / 2,
        )
        self.screen_position = position
        self.surface = pygame.Surface(char_surface_size)
        self.surface.blit(self.character_image, self.image_location)
        self.flash_type = flash_type
        self.explore = explore
        self.font = font
        self.grey = grey
        self.character_box_surface = pygame.Surface(self.character_image.get_size())
        self.character_box_surface.fill("white")

    def intensify(self):
        # Flash character only
        if self.flash_type == 0:
            self.surface.fill("black")
            self.character_image = self.font.render(self.character, True, "white")
        # Flash surface area of character
        if self.flash_type == 1:
            self.surface.fill("white")
            self.character_image = self.font.render(self.character, True, "black")
        # Flash character box area (small area around character)
        if self.flash_type == 2:
            self.surface.fill("black")
            self.character_image = self.font.render(self.character, True, "black")
            self.surface.blit(self.character_box_surface, self.image_location)

        self.surface.blit(self.character_image, self.image_location)
        self.explore.set_marker(code=int(self.character))

    def darken(self):
        self.surface.fill("black")
        self.character_image = self.font.render(self.character, True, self.grey)
        self.surface.blit(self.character_image, self.image_location)
