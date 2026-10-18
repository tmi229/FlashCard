from Data import CardList, FlashCardManager, FlashCard

Manager = CardList.CardList()

# Manager 1
List1 = FlashCardManager.FlashCardManager("Fruit")
Manager.add_manager(List1)

List1.add_card(FlashCard.FlashCard("apple", "quả táo", "/ˈæpəl/", "I eat an apple."))
List1.add_card(FlashCard.FlashCard("banana", "quả chuối", "/bəˈnænə/", "I eat a banana."))

# Manager 2
List2 = FlashCardManager.FlashCardManager("Animal")
Manager.add_manager(List2)

List2.add_card(FlashCard.FlashCard("cat", "con mèo", "/kæt/", "The cat is cute."))
List2.add_card(FlashCard.FlashCard("dog", "con chó", "/dɔːɡ/", "The dog is running."))

# Manager 3
List3 = FlashCardManager.FlashCardManager("Sport")
Manager.add_manager(List3)

List3.add_card(FlashCard.FlashCard("football", "bóng đá", "/ˈfʊtbɔːl/", "I play football."))
List3.add_card(FlashCard.FlashCard("tennis", "quần vợt", "/ˈtenɪs/", "She plays tennis."))

# Kiểm tra trước khi save
for manager in Manager.List_Managers:
    print(manager.id, manager.name, manager.count)
    for card in manager.Cards:
        print("   ", card.id, card.word)

Manager.save()

Manager2 = CardList.CardList()

Manager2.load()
for list in Manager2.List_Managers:
    for card in list.Cards:
        print(card.word)
        print(card.meaning)
        print(card.phonetic)
        print(card.example)
        print()