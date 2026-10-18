import pygame
import os
import json
from AudioManager import AudioManager


from UI import BButton 
from Screen import Menu,Learn,Quiz,ScreenManager
from Data import FlashCardManager,CardList
from UI.Theme import Theme


pygame.init()
pygame.display.set_caption("Flashcard Master - Học Từ Vựng Thông Minh")
screen = pygame.display.set_mode((1400, 720))
clock = pygame.time.Clock()
screen.fill(Theme.BG)
running = True


list_card_manager = CardList.CardList()

if os.path.exists(os.path.join(list_card_manager.card_path,"card.json")):
    list_card_manager.load()

else:
    list_card_manager.save()
    
audio = AudioManager()
menu = Menu.MenuScreen(audio)
learn = Learn.LearnScreen(list_card_manager,audio)
learn.update_nut_card()
learn.update_list()
quiz = Quiz.QuizScreen(list_card_manager,audio)
quiz.update_list()
manager = ScreenManager.Screen_Manager(menu,learn,quiz)

while running :
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        manager.handle_event(event)      

    manager.update(dt)
    
    screen.fill(Theme.BG)
    manager.draw(screen)            
                                                            
    
    pygame.display.flip()

list_card_manager.save()

pygame.quit()