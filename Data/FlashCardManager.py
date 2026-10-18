import json
from Data import FlashCard

class FlashCardManager:

    def __init__(self,name):
        self.name = name
        self.Cards = []
        self.count = 0
        self.id = 0

    def add_card(self, card):
        self.count += 1
        card.id = self.count
        self.Cards.append(card)
        

    def remove_card(self, card):
        self.Cards.remove(card)

    def find_card(self, word):
        for card in self.Cards:
            if card.word == word:
                return card
        return None  

    def save(self):
        CardsSave = [] 
        for card in self.Cards:
            data = {
                "word" : card.word,
                "meaning" : card.meaning,
                "phonetic" : card.phonetic,
                "example" : card.example,
                "id" : card.id
            }
            CardsSave.append(data)

        with open("card.json","w") as file:
            json.dump(CardsSave,file)

    def load(self):
        self.Cards = []
        with open("card.json", "r") as file:
            cards = json.load(file)
        temp = 0
        for card in cards:
            if card["id"] > temp :
                temp = card["id"]
            Temp_Card = FlashCard.FlashCard(card["word"],card["meaning"],card["phonetic"],card["example"])
            Temp_Card.id = card["id"]
            self.Cards.append(Temp_Card)
        self.count = temp