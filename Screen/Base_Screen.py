from abc import ABC, abstractmethod


class base(ABC):

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self,dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass