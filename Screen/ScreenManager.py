import pygame


class Screen_Manager:
    def __init__(self, menu, learn, quiz):
        self.menu = menu
        self.learn = learn
        self.quiz = quiz

        self.current_screen = self.menu

    def changescreen(self, screen_id):
        if screen_id == "learn":
            self.current_screen = self.learn
            self.learn.update_list()
            self.learn.update_nut_card()

        elif screen_id == "quiz":
            self.current_screen = self.quiz
            self.quiz.update_list()
            if hasattr(self.quiz, "shuffle_cards"):
                self.quiz.shuffle_cards()

        elif screen_id == "menu":
            self.current_screen = self.menu

        elif screen_id == "exit":
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_event(self, event):
        result = self.current_screen.handle_event(event)
        if result is not None and result != "out_box":
            self.changescreen(result)

    def update(self, dt):
        self.current_screen.update(dt)

    def draw(self, screen):
        self.current_screen.draw(screen)