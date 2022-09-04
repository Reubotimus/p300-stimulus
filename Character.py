import pygame


class Character:
    def __init__(self, character, position, char_surface_size, font, intense, explore, grey=(50, 50, 50)):
        self.character = character
        self.character_image = font.render(character, True, grey)
        self.image_location = (
            (char_surface_size - self.character_image.get_width()) / 2,
            (char_surface_size - self.character_image.get_height()) / 2,
        )
        self.screen_position = position
        self.surface = pygame.Surface((char_surface_size, char_surface_size))
        self.surface.blit(self.character_image, self.image_location)
        self.intense = intense
        self.explore = explore
        self.font = font
        self.grey = grey

    def intensify(self):
        if self.intense == True:
            self.surface.fill("white")
            self.character_image = self.font.render(
                self.character, True, "black")
            self.surface.blit(self.character_image, self.image_location)
            self.explore.set_marker(code=int(self.character))
        else:
            self.surface.fill("black")
            self.character_image = self.font.render(
                self.character, True, "white")
            self.surface.blit(self.character_image, self.image_location)
            self.explore.set_marker(code=int(self.character))

    def darken(self):
        self.surface.fill("black")
        self.character_image = self.font.render(
            self.character, True, self.grey)
        self.surface.blit(self.character_image, self.image_location)
