from Data import FlashCardManager,FlashCard
import json
import os

class CardList :
    def __init__(self):
        self.cnt = 1
        self.List_Managers = []
        Base_list = FlashCardManager.FlashCardManager("New List")
        Base_list.id = 1
        Base_list.count = 0
        self.List_Managers.append(Base_list)
        self.card_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        

    def add_manager (self, manager):
        self.cnt += 1
        manager.id = self.cnt
        self.List_Managers.append(manager)
        
    def default_manager(self):
        Base_list = FlashCardManager.FlashCardManager("New List")
        Base_list.id = 1
        Base_list.count = 0
        self.List_Managers.append(Base_list)
        self.cnt = 1

    def remove_manager(self, id_del):
        for manager in self.List_Managers:
            if manager.id == id_del:
                self.List_Managers.remove(manager)
                break
        if len(self.List_Managers) == 0 :
            self.default_manager()
            


    def find_manager(self, id):
        for manager in self.List_Managers:
            if manager.id == id :
                return manager
        return None

            
    
    def load(self):
        self.List_Managers = []
        with open(os.path.join(self.card_path,"card.json"),"r",encoding="utf-8") as file:
            lists = json.load(file)
        temp1 = 0
        
        for list in lists :
            if list["id"] > temp1:
                temp1 = list["id"]
            Cards = []
            temp2 = 0
            
            for card in list["Cards"]:
                if card["id"] > temp2:
                    temp2 = card["id"]
                Temp_Card = FlashCard.FlashCard(card["word"],card["meaning"],card["phonetic"],card["example"])
                Temp_Card.id = card["id"]
                Cards.append(Temp_Card)
        
            Temp_list = FlashCardManager.FlashCardManager(list["name"])
            Temp_list.id = list["id"]
            Temp_list.Cards = Cards
            Temp_list.count = temp2
            self.List_Managers.append(Temp_list)
        self.cnt = temp1
        if len(self.List_Managers) == 0 :
            self.default_manager()
            
        
        
    
    def save(self):
        ListsSave = [] 
        
        for list in self.List_Managers:
            CardSave = []
            
            for card in list.Cards:
                data2 = {
                    "word" : card.word,
                    "meaning" : card.meaning,
                    "phonetic" : card.phonetic,
                    "example" : card.example,
                    "id" : card.id
                }
                CardSave.append(data2)
            
            data = {
                "name" : list.name,
                "id" : list.id,
                "Cards" : CardSave
            }
            ListsSave.append(data)

        with open(os.path.join(self.card_path,"card.json"),"w",encoding="utf-8") as file:
            json.dump(ListsSave,file,ensure_ascii=False, indent=4)
    
    
    