import pygame as pg

pg.init()


class Scene:
    def __init__(self):
        self.redirect = None
        self.redirect_delay = 0
        self.deactivate_fade = False
        self.allow_keydown = True
        self.fade_delay = 0

    def input(self):
        """
        Defines inputs taken from the player
        """
        pass

    def redraw(self):
        """
        Defines what to redraw onto the screen each iteration
        """
        pass

    def pre_event(self):
        """
        Defines what to do before other events occur (input, redraw)
        """
        pass

    def end_pre_event(self):
        """
        Defines the condition to end pre_event (save extra running time)
        """
        return True

    def reset_attr(self):
        """
        Defines what to reset when a scene finishes work
        """
        self.redirect = None
        self.allow_keydown = False

    def update(self, is_transitioning: bool):
        """
        Defines what to update every frame
        """
        if not self.end_pre_event():
            self.pre_event()

        if not is_transitioning:
            self.input()
        self.redraw()
