import pygame

from abc import ABC,abstractmethod

class Widget(ABC):
    def __init__(self):
        self.widgets = []

    @abstractmethod
    def handle_event(self,event):
        for widget in self.widgets:
            widget.handle_event(event)

    @abstractmethod
    def update(self):
        for widget in self.widgets:
            widget.update()

    @abstractmethod
    def draw(self,screen):
        for widget in self.widgets:
            widget.draw(screen)